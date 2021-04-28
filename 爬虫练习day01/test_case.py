import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By



class TestCase(unittest.TestCase):

    def test_01_login(self):
        # 打开浏览器

        driver = webdriver.chrome




