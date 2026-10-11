from seleniumbase import BaseCase


class DemoTest(BaseCase):
    def test_open_page(self):
        """最小冒烟用例：打开本地 HTML 并断言标题"""
        self.open("data:text/html,<h1 id='t'>hello-seleniumbase</h1>")
        self.assert_text("hello-seleniumbase", "#t")
