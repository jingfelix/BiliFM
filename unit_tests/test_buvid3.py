import unittest
from unittest.mock import Mock, call, patch

import requests

from bilifm.audio import Audio
from bilifm.util import AudioQualityEnums, _fetch_buvid3, get_buvid3, request


class TestBuvid3(unittest.TestCase):
    def setUp(self):
        _fetch_buvid3.cache_clear()
        self.addCleanup(_fetch_buvid3.cache_clear)
        self.response = Mock()
        self.response.json.return_value = {"data": {"b_3": "test-buvid3"}}

    @patch("bilifm.util.time.sleep")
    @patch("bilifm.util.requests.get")
    def test_retries_then_caches_success(self, get, sleep):
        get.side_effect = [requests.Timeout(), requests.Timeout(), self.response]
        self.assertEqual(get_buvid3(), "test-buvid3")
        self.assertEqual(get_buvid3(), "test-buvid3")
        self.assertEqual(get.call_count, 3)
        self.assertEqual(sleep.call_args_list, [call(0.5), call(1.0)])
        self.assertTrue(all(c.kwargs["timeout"] == 10 for c in get.call_args_list))

    @patch("bilifm.util.time.sleep")
    @patch("bilifm.util.requests.get")
    def test_exhausted_retries_do_not_cache_failure(self, get, sleep):
        get.side_effect = [requests.Timeout()] * 3 + [self.response]
        self.assertEqual(get_buvid3(), "")
        self.assertEqual(get.call_count, 3)
        self.assertEqual(_fetch_buvid3.cache_info().currsize, 0)
        self.assertEqual(get_buvid3(), "test-buvid3")
        self.assertEqual(get.call_count, 4)
        self.assertEqual(sleep.call_args_list, [call(0.5), call(1.0)])

    @patch("bilifm.util.time.sleep")
    @patch("bilifm.util.requests.get")
    def test_invalid_responses_are_retried(self, get, sleep):
        http_error = Mock()
        http_error.raise_for_status.side_effect = requests.HTTPError("HTTP 503")
        invalid_json = Mock()
        invalid_json.json.side_effect = requests.exceptions.JSONDecodeError(
            "Invalid JSON", "", 0
        )
        invalid_responses = [http_error, invalid_json]
        for payload in [{}, {"data": None}] + [
            {"data": {"b_3": value}} for value in ["", None, 123]
        ]:
            response = Mock()
            response.json.return_value = payload
            invalid_responses.append(response)

        for response in invalid_responses:
            with self.subTest(response=response):
                _fetch_buvid3.cache_clear()
                get.reset_mock()
                sleep.reset_mock()
                get.side_effect = [response, self.response]
                self.assertEqual(get_buvid3(), "test-buvid3")
                self.assertEqual(get.call_count, 2)
                sleep.assert_called_once_with(0.5)
        http_error.json.assert_not_called()

    @patch("bilifm.util.time.sleep")
    @patch("bilifm.util.requests.get")
    def test_audio_sends_cookie_after_retry(self, get, sleep):
        video = Mock()
        video.json.return_value = {
            "data": {"title": "Demo", "pages": [{"cid": 1, "part": "Demo"}]}
        }
        get.side_effect = [requests.Timeout(), self.response, video]
        audio = Audio("BV1234567890", AudioQualityEnums.k64)
        self.assertEqual(audio.title, "Demo")
        self.assertEqual(
            get.call_args.kwargs["headers"]["Cookie"], "buvid3=test-buvid3"
        )
        sleep.assert_called_once_with(0.5)

    @patch("bilifm.util.requests.request")
    @patch("bilifm.util.requests.get")
    def test_request_sends_anonymous_cookie(self, get, send):
        get.return_value = self.response
        request("get", "https://api.example.test")
        self.assertEqual(send.call_args.kwargs["cookies"], {"buvid3": "test-buvid3"})

    @patch("bilifm.util.requests.request")
    @patch("bilifm.util.requests.get")
    def test_request_preserves_explicit_user_cookies(self, get, send):
        for cookies in [{"buvid3": "user-buvid3", "SESSDATA": "test-session"}, {}]:
            with self.subTest(cookies=cookies):
                request("get", "https://api.example.test", cookies=cookies)
                self.assertIs(send.call_args.kwargs["cookies"], cookies)
        get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
