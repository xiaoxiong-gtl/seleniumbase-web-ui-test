"""saucedemo 商品列表页（登录后的首页）。"""
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"
    PAGE_READY = "#inventory_container"

    # ---- 元素定位 ----
    ITEM = "div.inventory_item"
    ITEM_NAME = "div.inventory_item_name"
    ITEM_PRICE = "div.inventory_item_price"
    SORT_SELECT = "select[data-test='product-sort-container']"
    CART_BADGE = "span.shopping_cart_badge"
    CART_LINK = "a.shopping_cart_link"

    # 按商品名定位「加入购物车」按钮的 XPath 模板：
    # 找到名字匹配的那个商品卡片，再取它内部的加购按钮。
    #
    # 这里用 data-test 而不是 class 做匹配，原因：
    # 站点的 class 是 "inventory_item_name "（带尾随空格），
    # @class='inventory_item_name' 这种精确匹配会匹配不到；
    # 而 data-test 是站点官方留给自动化测试的稳定钩子，且不受样式改版影响。
    _ADD_BUTTON_BY_NAME = (
        "//div[@data-test='inventory-item']"
        "[.//div[@data-test='inventory-item-name' and normalize-space()='{name}']]"
        "//button[contains(@data-test, 'add-to-cart')]"
    )

    # ---------------- 业务操作 ----------------
    def add_to_cart(self, product_name):
        """把指定商品加入购物车。"""
        self.click(self._ADD_BUTTON_BY_NAME.format(name=product_name))
        return self

    def sort_by(self, option_text):
        """按下拉选项排序，如 'Price (low to high)'。"""
        self.select_by_text(self.SORT_SELECT, option_text)
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return self

    # ---------------- 读取 ----------------
    def product_names(self):
        return self.texts_of(self.ITEM_NAME)

    def product_prices(self):
        """返回商品价格（float 列表），供排序断言用。"""
        return [self._to_float(t) for t in self.texts_of(self.ITEM_PRICE)]

    def cart_count(self):
        """购物车角标数量；没加东西时角标不存在，返回 0。"""
        if not self.is_visible(self.CART_BADGE, timeout=2):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def item_count(self):
        return self.count_of(self.ITEM)

    @staticmethod
    def _to_float(price_text):
        """'$29.99' -> 29.99"""
        return float(price_text.replace("$", "").strip())
