from datetime import datetime
import unittest

import requests

from . import config

class ShortenRequester(object):
	def __init__(self):
		self.host = "http://nginx:80"
		self.shorten_url = self.host + "/urls"
		self.resolve_url = self.host + "/"

	def create(self, url: str) -> (str, int):
		response = requests.post(self.shorten_url, json={"url": url})
		data = response.json()
		return data.get("short_url"), response.status_code

	def resolve(self, url: str) -> (str, int):
		response = requests.get(self.resolve_url + url)
		data = response.json()
		return data.get("url"), response.status_code

class TestShortenAndResolve(unittest.TestCase):
	URL = "https://www.google.com/search?q="
	SUCCESS_CODE = 200
	NOT_FOUND_CODE = 404
	FAIL_CODE = 500

	def setUp(self) -> None:
		self.shorten_requester = ShortenRequester()
		self.short_url_prefix = config.get_site_url()

	def _generate_url(self, suffix: str = None) -> str:
		url = self.URL + str(datetime.now().timestamp())
		if suffix is not None:
			url += "+" + suffix
		return url

	def _assert_and_get_short_key(self, short_url: str, status_code: int) -> str:
		self.assertEqual(status_code, self.SUCCESS_CODE, "Not success (200) status code returned for create.")
		self.assertIsNotNone(short_url, "'short_url' not found in the create response.")
		self.assertEqual(self.short_url_prefix, short_url[:len(self.short_url_prefix)], "Short url don't have required prefix.")
		short_key = short_url[len(self.short_url_prefix):]
		self.assertNotEqual(short_key, "", "short_key is empty in short_url")
		return short_key

	def _assert_resolve(self, resolved_url: str, status_code: int, init_url: str = None) -> None:
		self.assertEqual(status_code, self.SUCCESS_CODE, "Not success (200) status code returned fpr resolve.")
		self.assertIsNotNone(resolved_url, "'url' not found in the resolve response.")
		if init_url is not None:
			self.assertEqual(init_url, resolved_url, "Initial url and resolved urls are not same.")

	def test_create(self):
		short_url, status_code = self.shorten_requester.create(self._generate_url())
		self._assert_and_get_short_key(short_url, status_code)

	def test_create_and_resolve(self):
		url = self._generate_url()
		short_url, status_code = self.shorten_requester.create(url)
		short_key = self._assert_and_get_short_key(short_url, status_code)

		resolved_url, status_code = self.shorten_requester.resolve(short_key)
		self._assert_resolve(resolved_url, status_code, init_url=url)

	def test_create_two_times(self):
		url = self._generate_url()

		short_url_1, status_code_1 = self.shorten_requester.create(url)
		self._assert_and_get_short_key(short_url_1, status_code_1)

		short_url_2, status_code_2 = self.shorten_requester.create(url)
		self._assert_and_get_short_key(short_url_2, status_code_2)

	def test_unordered_create_and_resolve(self):
		url_1 = self._generate_url(suffix="1")
		short_url_1, status_code_1 = self.shorten_requester.create(url_1)
		short_key_1 = self._assert_and_get_short_key(short_url_1, status_code_1)

		url_2 = self._generate_url(suffix="2")
		short_url_2, status_code_2 = self.shorten_requester.create(url_2)
		short_key_2 = self._assert_and_get_short_key(short_url_2, status_code_2)

		url_3 = self._generate_url(suffix="3")
		short_url_3, status_code_3 = self.shorten_requester.create(url_3)
		short_key_3 = self._assert_and_get_short_key(short_url_3, status_code_3)

		resolved_url_2, status_code_2 = self.shorten_requester.resolve(short_key_2)
		self._assert_resolve(resolved_url_2, status_code_2, init_url=url_2)

		resolved_url_1, status_code_1 = self.shorten_requester.resolve(short_key_1)
		self._assert_resolve(resolved_url_1, status_code_1, init_url=url_1)

		resolved_url_3, status_code_3 = self.shorten_requester.resolve(short_key_3)
		self._assert_resolve(resolved_url_3, status_code_3, init_url=url_3)

	def test_create_not_valid_url(self):
		url = "iamaninvalidurl"

		_, status_code = self.shorten_requester.create(url)
		self.assertNotEqual(status_code, self.SUCCESS_CODE, "Success (200) status code returned.")

	def test_resolve_not_found_short_url(self):
		short_key = "not_found+" + str(datetime.now().timestamp())

		_, status_code = self.shorten_requester.resolve(short_key)
		self.assertEqual(status_code, self.NOT_FOUND_CODE, "Not 'not found' (404) status code returned for invalid short key.")
