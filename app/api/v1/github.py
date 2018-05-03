import cPickle
import requests
import time
import cache
from flask import current_app
from flask import jsonify
from dateutil import parser

import database
from models import  Github
from . import api

db = database.db
r = cache.redis_store


redis_latest = "latest_500"
redis_top = "top_500"
redis_activity = "activity_500"


@api.route("/test")
def hello_world():
    current_app.logger.info("Testing application!!")
    return "Oh, Hello World"\


@api.route("/update_cache")
def parse_github():
    current_app.logger.info("Getting github data")
    data = query_github()
    parse_github_raw_data(data)
    update_cache()
    return "update_cache"

@api.route("/bootstrap_db")
def bootstrap_db():
    database.init_db_if_exist()
    return "bootstrap_db"


@api.route("/health")
def health():
    current_app.logger.info("Testing application!!")
    return "ok"


@api.route("/api/kubernetes")
def get_kubernetes_repos():
    return request_response(cache_find_500_github_acc())


@api.route("/api/popularity/kubernetes")
def get_popular_kubernetes_repos():
    return request_response(cache_find_top_github_acc())


@api.route("/api/activity/kubernetes")
def get_sorted_repos():
    return request_response(cache_find_activities_github())

@api.route("/db/kubernetes")
def get_db_kubernetes_repos():
    return request_response(to_json_list(db_find_500_github_acc()))


@api.route("/db/popularity/kubernetes")
def get_db_popular_kubernetes_repos():
    return request_response(to_json_list(db_find_top_github_acc()))


@api.route("/db/activity/kubernetes")
def get_db_sorted_repos():
    return request_response(to_json_list(db_find_top_activity_github_acc()))


def request_response(results):
    if results:
        results = jsonify(results)
    else:
        results = jsonify([])
    return results

def query_github():
    url="https://api.github.com/search/repositories"
    headers = {'Content-type': 'application/json', 'Accept': 'application/vnd.github.mercy-preview+json'}
    query = "topic:kubernetes"
    payload = {"q":query,"per_page":100, "page":1}

    r = requests.get(url, params=payload, headers=headers)
    response_header = r.headers
    pages = parse_pagantion_link(response_header["Link"])
    check_rate_limit(response_header)

    data_json = r.json()["items"]

    if pages > 2:
        for page in range(2, pages + 1):
            print("parsing page:"+str(page))
            payload["page"] = page
            r = requests.get(url, params=payload, headers=headers)
            r_json = r.json()
            if "items" in r_json:
                data_json += r_json["items"]
            else:
                current_app.logger.debug(r.text)
            check_rate_limit(r.headers)
    print("found entries: "+str(len(data_json)))
    return data_json

def check_rate_limit(response_header):
    if 0 == int(response_header["X-RateLimit-Remaining"]):
        print("Exceeded rate limit for github, sleeping for 60s")
        time.sleep(10)

def parse_pagantion_link(link):
    last = 0
    if "&page=" in link:
        list = link.split(';')
        last  = int(list[1].split("&page=")[1].split(">")[0])
    return last


def create_update_github_acc(name, full_name,
                      html_url, language, updated_at,
                      pushed_at, stargazers_count, github_acc):

    github_acc.name = name
    github_acc.full_name = full_name
    github_acc.html_url = html_url
    github_acc.language = language
    github_acc.updated_at = parser.parse(updated_at)
    github_acc.pushed_at = parser.parse(pushed_at)
    github_acc.stargazers_count = stargazers_count
    return github_acc


def parse_github_raw_data(data):
    parsed_acc_list = []
    for entry in data:

        existing_account = find_github_acc(entry["id"])
        if existing_account:
            github_acc = existing_account
        else:
            github_acc = Github(entry["id"])

        github_acc = create_update_github_acc(
            entry["name"], entry["full_name"],
            entry["html_url"], entry["language"],
            entry["updated_at"], entry["pushed_at"],
            entry["stargazers_count"], github_acc)

        github_acc = write_github_acc(github_acc)
        parsed_acc_list.append(github_acc)

    return parsed_acc_list


def write_github_acc(github_acc):
    current_app.logger.debug("Writing user: "+str(github_acc.full_name))
    db.session.add(github_acc)
    db.session.commit()
    return github_acc



def find_github_acc(id):
    github_acc = db.session.query(Github).get(id)
    if github_acc is None:
        current_app.logger.debug(" - Github acc not in DB")
    else:
        current_app.logger.debug(" - Github acc found in DB: "+str(github_acc.id))
    return github_acc


def cache_find_500_github_acc():
    r_cache = r.get(redis_latest)
    results = None
    if r_cache:
        results = cPickle.loads(r_cache)
    return results


def cache_find_top_github_acc():
    r_cache = r.get(redis_top)
    results = None
    if r_cache:
        results = cPickle.loads(r_cache)
    return results


def cache_find_activities_github():
    r_cache = r.get(redis_activity)
    results = None
    if r_cache:
        results = cPickle.loads(r_cache)
    return results


def db_find_500_github_acc():
    return db.session.query(Github).limit(500).all()


def db_find_top_github_acc():
    return db.session.query(Github).order_by(Github.stargazers_count.desc()).limit(500)


def db_find_top_activity_github_acc():
    return db.session.query(Github).order_by(Github.updated_at.desc()).limit(500)

def to_json_list(data):
    json_list = []
    for entry in data:
        json_list.append(entry.as_json())
    return json_list


def update_cache():
    current_app.logger.debug(" - Updating redis cache")

    r.pipeline().\
        delete(redis_latest).\
        delete(redis_activity).\
        delete(redis_top).execute()

    pipe = r.pipeline()
    pipe.set(redis_latest, cPickle.dumps(to_json_list(db_find_500_github_acc())))
    pipe.set(redis_top, cPickle.dumps(to_json_list(db_find_top_github_acc())))
    pipe.set(redis_activity, cPickle.dumps(to_json_list(db_find_top_activity_github_acc())))
    pipe.execute()
