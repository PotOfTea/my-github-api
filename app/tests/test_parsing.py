import unittest
from unittest import TestCase

from dateutil import parser
from mock import patch

from app.api.v1.github import create_update_github_acc, get_kubernetes_repos, cache_find_500_github_acc, \
    parse_github_raw_data
from models import Github

id = "1"
name = "test-acc"
full_name = "full test acc"
html_url = "test_html_url"
language = "test-language"
updated_at = "2018-05-01T17:01:50Z"
pushed_at = "2018-05-01T17:01:50Z"
stargazers_count = 1

class TestGithub(TestCase):

    def test_create_update_github_acc(self):
        tmp_acc = create_update_github_acc(
            name, full_name, html_url,
            language, updated_at, pushed_at,
            stargazers_count, Github(id))
        validate_acc(tmp_acc)

    def test_parse_github_raw_data(self):
        tmp_acc = generate_github_acc()
        data = []
        data.append(get_acc_raw_data())
        with patch("app.api.v1.github.find_github_acc", return_value = tmp_acc ):
            with patch("app.api.v1.github.write_github_acc", return_value = tmp_acc):
                parsed_data = parse_github_raw_data(data)
                assert len(parsed_data) == 1
                validate_acc(parsed_data[0])

def validate_acc(tmp_acc):
    assert tmp_acc.id == id
    assert tmp_acc.name == name
    assert tmp_acc.full_name == full_name
    assert tmp_acc.language == language
    assert tmp_acc.updated_at == parser.parse(updated_at)
    assert tmp_acc.pushed_at == parser.parse(pushed_at)
    assert tmp_acc.stargazers_count == stargazers_count

def get_acc_raw_data():
    entry = {}
    entry["id"] = id
    entry["name"] = name
    entry["full_name"] = full_name
    entry["html_url"]  = html_url
    entry["language"] = language
    entry["updated_at"] = updated_at
    entry["pushed_at"] = pushed_at
    entry["stargazers_count"] = stargazers_count
    return entry

def generate_github_acc():
    entry = get_acc_raw_data()
    return Github(entry["id"])

if __name__ == '__main__':
    unittest.main()