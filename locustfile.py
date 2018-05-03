from locust import HttpLocust, TaskSet


def parse_response(response):
    try:
        return response.json()
    except:
        print("Failed response: "+ str(response.status_code)+" text: "+str(response.raw))

def api_popularity_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/api/popularity/kubernetes", headers=headers)
    response = parse_response(response)


def api_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/api/kubernetes", headers=headers)
    response = parse_response(response)


def api_activity_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/api/activity/kubernetes", headers=headers)
    response = parse_response(response)

def api_db_popularity_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/db/popularity/kubernetes", headers=headers)
    response = parse_response(response)


def api_db_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/db/kubernetes", headers=headers)
    response = parse_response(response)


def api_db_activity_kubernetes(l):
    headers = {'content-type': 'application/json'}
    response = l.client.get("/db/activity/kubernetes", headers=headers)
    response = parse_response(response)


def test(l):
    l.client.get("/test")

class UserBehavior(TaskSet):
    tasks = {test: 1,
             api_popularity_kubernetes: 2,
             api_kubernetes: 3,
             api_activity_kubernetes: 4,
             api_db_popularity_kubernetes: 5,
             api_db_kubernetes: 6,
             api_db_activity_kubernetes: 7}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000