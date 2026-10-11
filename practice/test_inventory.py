"""商品列表页用例：商品展示、排序、加入购物车。

全部依赖 logged_in fixture，用例里看不到任何登录代码和元素定位。
"""
from testdata import BACKPACK, BIKE_LIGHT, EXPECTED_PRODUCT_COUNT


def test_product_list_loaded(logged_in):
    """登录后应展示商品列表，且数量与预期一致。"""
    assert logged_in.item_count() == EXPECTED_PRODUCT_COUNT


def test_sort_price_low_to_high(logged_in):
    """按价格升序排序后，价格应单调不减。"""
    logged_in.sort_by("Price (low to high)")

    prices = logged_in.product_prices()
    assert prices == sorted(prices), f"价格未按升序排列：{prices}"


def test_sort_price_high_to_low(logged_in):
    """按价格降序排序后，价格应单调不增。"""
    logged_in.sort_by("Price (high to low)")

    prices = logged_in.product_prices()
    assert prices == sorted(prices, reverse=True), f"价格未按降序排列：{prices}"


def test_sort_name_a_to_z(logged_in):
    """按名称 A→Z 排序后，商品名应为字母升序。"""
    logged_in.sort_by("Name (A to Z)")

    names = logged_in.product_names()
    assert names == sorted(names)


def test_add_to_cart_updates_badge(logged_in):
    """加入两件商品后，购物车角标应为 2。"""
    assert logged_in.cart_count() == 0, "初始购物车应为空"

    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    assert logged_in.cart_count() == 2
