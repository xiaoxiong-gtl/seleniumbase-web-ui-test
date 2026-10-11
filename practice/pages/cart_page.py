"""saucedemo 购物车页。"""
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.saucedemo.com/cart.html"
    PAGE_READY = "div.cart_footer"  # 页脚始终存在，空车时也能等到

    # ---- 元素定位 ----
    CART_ITEM = "div.cart_item"
    ITEM_NAME = "div.inventory_item_name"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING = "#continue-shopping"

    # ---------------- 业务操作 ----------------
    def remove_first_item(self):
        self.click(self.REMOVE_BUTTON)
        return self

    def checkout(self):
        """点击结算，进入填写收货信息页。"""
        self.click(self.CHECKOUT_BUTTON)
        return self

    # ---------------- 读取 ----------------
    def item_names(self):
        return self.texts_of(self.ITEM_NAME)

    def item_count(self):
        return self.count_of(self.CART_ITEM)
