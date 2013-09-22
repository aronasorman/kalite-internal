import json

from django.test import TestCase

from dashboard.models import News
from dashboard.github import save_event

class IssueTestCase(TestCase):

    def setUp(self):
        self.events = {}
        with open('fle-internal-news.json', 'r') as f:
            rawdata = f.read()
            self.events['fle-internal'] = json.loads(rawdata)
            self.issue_events = [e for e in self.events['fle-internal'] if e['type'] == 'IssuesEvent']

    def test_saved_event_has_correct_action_in_title(self):
        event = self.issue_events[0]
        for action in ['opened', 'closed', 'reopened']:
            event['payload']['action'] = action
            news = save_event(event)
            self.assertRegexpMatches(news.title, action)

    def test_saved_event_has_actor_in_title(self):
        event = self.issue_events[0]
        news = save_event(event)
        self.assertRegexpMatches(news.title, event['actor']['login'])

    def test_saved_event_has_issue_in_title(self):
        event = self.issue_events[0]
        news = save_event(event)
        self.assertRegexpMatches(news.title, str(event['payload']['issue']['number']))

    def test_saved_event_should_have_link(self):
        event = self.issue_events[0]
        news = save_event(event)
        url = event['payload']['issue']['html_url']
        self.assertEquals(news.link, url)

class IssueCommentTestCase(TestCase):

    def setUp(self):
        self.events = {}
        with open('fle-internal-news.json', 'r') as f:
            rawdata = f.read()
            self.events['fle-internal'] = json.loads(rawdata)
            self.issue_events = [e for e in self.events['fle-internal'] if e['type'] == 'IssueCommentEvent']

    def test_can_save_event(self):
        event = self.issue_events[0]
        news = save_event(event)
        self.assertIsInstance(news, News)
        self.assertTrue(news.pk, 'Object not saved yet')
