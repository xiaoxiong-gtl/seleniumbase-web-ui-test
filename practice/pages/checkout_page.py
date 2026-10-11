"""saucedemo 结算流程页（信息填写 + 订单确认 + 下单成功）。

结算是一个多步流程，这里用一个类覆盖三个页面，
因为它们同属「下单」这一条业务链，拆开反而让用例层更啰嗦。
"""
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    URL = "https://www.saucedemo.com/checkout-step-one.html"
    PAGE_READY = "#continue"

    # ---- 填写收货信息页 ----
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    ERROR_MESSAGE = "h3[data-test='error']"

    # ---- 订单确认页 ----
    SUMMARY_TOTAL = "div.summary_total_label"
    FINISH_BUTTON = "#finish"

    # ---- 下单成功页 ----
    COMPLETE_HEADER = "h2.complete-header"

    # ---------------- 业务操作 ----------------
    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)
        return self

    def finish(self):
        """在订单确认页点击完成下单。"""
        self.click(self.FINISH_BUTTON)
        return self

    # ---------------- 读取 / 断言辅助 ----------------
    def total_text(self):
        """订单总价文案，如 'Total: $32.39'。"""
        return self.text_of(self.SUMMARY_TOTAL)

    def complete_message(self):
        return self.text_of(self.COMPLETE_HEADER)

    def error_message(self):
        """必填校验失败时的提示文案。"""
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
