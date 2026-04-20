import os
import tempfile
import unittest
from unittest.mock import patch

from bilifm.audio import Audio
from bilifm.util import AudioQualityEnums


class FakeResponse:
    def __init__(self, payload=None, content=b"", status_code=200):
        self.payload = payload
        self.content = content
        self.status_code = status_code
        self.headers = {"content-length": str(len(content))}

    def json(self):
        return self.payload

    def iter_content(self, chunk_size=8192):
        yield self.content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class TestAudioDownload(unittest.TestCase):
    def build_audio(self, parts):
        audio = Audio.__new__(Audio)
        audio.bvid = "BV1234567890"
        audio.title = "Demo"
        audio.playUrl = "https://api.example.test/playurl"
        audio.part_list = [part for _, part in parts]
        audio.cid_list = [cid for cid, _ in parts]
        audio.headers = {}
        audio.audio_quality = AudioQualityEnums.k64.quality_id
        audio.request_delay = 0
        audio.play_url_retries = 2
        audio.retry_delay = 0
        return audio

    def test_retries_when_dash_is_missing_temporarily(self):
        audio = self.build_audio([("1", "Part-1")])
        play_url_responses = [
            FakeResponse({"code": 0, "message": "OK", "data": {"v_voucher": "x"}}),
            FakeResponse(
                {
                    "code": 0,
                    "message": "OK",
                    "data": {
                        "dash": {
                            "audio": [
                                {
                                    "id": AudioQualityEnums.k64.quality_id,
                                    "baseUrl": "https://audio.example.test/1",
                                }
                            ]
                        }
                    },
                }
            ),
        ]

        def fake_get(url, **kwargs):
            if url == audio.playUrl:
                return play_url_responses.pop(0)
            return FakeResponse(content=b"audio")

        with tempfile.TemporaryDirectory() as directory:
            cwd = os.getcwd()
            os.chdir(directory)
            try:
                with patch("bilifm.audio.get_signed_params", side_effect=lambda p: p):
                    with patch("bilifm.audio.requests.get", side_effect=fake_get):
                        audio.download()

                self.assertEqual(play_url_responses, [])
                self.assertTrue(os.path.exists("Demo.mp3"))
            finally:
                os.chdir(cwd)

    def test_existing_part_is_skipped_without_stopping_download(self):
        audio = self.build_audio([("1", "Part-1"), ("2", "Part-2")])
        requested_params = []

        def fake_get(url, **kwargs):
            if url == audio.playUrl:
                requested_params.append(kwargs["params"])
                return FakeResponse(
                    {
                        "code": 0,
                        "message": "OK",
                        "data": {
                            "dash": {
                                "audio": [
                                    {
                                        "id": AudioQualityEnums.k64.quality_id,
                                        "baseUrl": "https://audio.example.test/2",
                                    }
                                ]
                            }
                        },
                    }
                )
            return FakeResponse(content=b"audio")

        with tempfile.TemporaryDirectory() as directory:
            cwd = os.getcwd()
            os.chdir(directory)
            try:
                with open("Demo-Part-1.mp3", "wb") as f:
                    f.write(b"already downloaded")

                with patch("bilifm.audio.get_signed_params", side_effect=lambda p: p):
                    with patch("bilifm.audio.requests.get", side_effect=fake_get):
                        audio.download()

                self.assertEqual([params["cid"] for params in requested_params], ["2"])
                self.assertTrue(os.path.exists("Demo-Part-2.mp3"))
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
