"""购物车用例：商品带入、移除。"""
from pages.cart_page import CartPage
from testdata import BACKPACK, BIKE_LIGHT


def test_cart_contains_added_items(sb, logged_in):
    """列表页加入的商品，应原样出现在购物车中。"""
    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    logged_in.go_to_cart()

    cart = CartPage(sb).wait_ready()
    assert cart.item_count() == 2
    assert BACKPACK in cart.item_names()
    assert BIKE_LIGHT in cart.item_names()


def test_remove_item_from_cart(sb, logged_in):
    """从购物车移除一件后，应只剩一件。"""
    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
    logged_in.go_to_cart()

    cart = CartPage(sb).wait_ready()
    cart.remove_first_item()
    assert cart.item_count() == 1
