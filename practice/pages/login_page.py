"""saucedemo 登录页。"""
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    PAGE_READY = "#login-button"

    # ---- 元素定位（对外隐藏，用例层不需要知道这些选择器）----
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "h3[data-test='error']"

    # ---------------- 业务操作 ----------------
    def login(self, username, password):
        """填写账号密码并提交。不关心结果，供用例自行断言。"""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    # ---------------- 读取 / 断言辅助 ----------------
    def error_message(self):
        """返回登录失败提示文案（如「用户名和密码不匹配」）。"""
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
