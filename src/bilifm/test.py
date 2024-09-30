import os
import unittest

from typing_extensions import Annotated

from .command import *
from .util import AudioQualityEnums, change_directory


class TestBiliFM(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cpwd = os.getcwd()
        change_directory("tests")

    @classmethod
    # 清理测试文件
    def tearDownClass(cls) -> None:
        change_directory(cls.cpwd)
        import shutil

        folder_name = "tests"
        try:
            shutil.rmtree(folder_name)
            print(f"文件夹 {folder_name} 已被删除。")
        except FileNotFoundError:
            print(f"文件夹 {folder_name} 不存在。")
        except Exception as e:
            print(f"删除文件夹 {folder_name} 时出错: {e}")

    def setUp(self):
        # 设置测试环境
        self.test_bv = "BV1yt4y1Q7SS"
        self.audioquality = AudioQualityEnums.k64
        self.test_fav = "69361944"  # 暂时没有找到比较好的测试fav
        self.test_cookies_path = ""
        self.media_id = "69361944"
        self.sid = "1855309"  # 需要找到一个较少的测试合集，不然测起来时间太久了
        self.uid = "261485584"  # 需要找到一个作品少的uid进行测试

    def test_bv_command(self):
        self.assertIsNone(bv(self.test_bv, None, self.audioquality))

    def test_uid_command(self):
        # self.assertIsNone(uid(self.uid, None, self.audioquality))
        pass

    def test_fav_command(self):
        # 需要cookies 感觉不太能测吧
        pass

    def test_season_command(self):
        # self.assertIsNone(season(self.uid, self.sid, None, self.audioquality))
        pass

    def test_series_command(self):
        # self.assertIsNone(series(self.uid, self.sid, None, self.audioquality))
        pass


if __name__ == "__main__":
    unittest.main()
