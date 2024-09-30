import os
import unittest

from .audio import Audio
from .util import AudioQualityEnums


class TestBiliFM(unittest.TestCase):
    def setUp(self):
        # 设置测试环境
        self.test_bv = "BV1yt4y1Q7SS"  # 测试用的BV号

    def test_bv_command(self):
        # bv命令的实现
        audio_quality = AudioQualityEnums.k192
        audio = Audio(self.test_bv, audio_quality)
        audio.download()
        # 验证音频文件是否下载
        self.assertTrue(os.path.exists(f"{audio.title}.mp3"))
        os.remove(f"{audio.title}.mp3")

    def test_uid_command(self):
        pass


if __name__ == "__main__":
    unittest.main()
