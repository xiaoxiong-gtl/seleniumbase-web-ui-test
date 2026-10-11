"""结算流程用例：端到端下单 + 收货信息必填校验。"""
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from testdata import BACKPACK, BIKE_LIGHT


def test_e2e_place_order(sb, logged_in):
    """端到端链路：登录 → 加购 → 购物车 → 结算 → 下单成功。

    这条用例覆盖完整用户路径，是回归时的「冒烟用例」——
    它一挂说明主流程断了，优先排查。
    """
    # 1. 加购两件商品（登录态由 logged_in fixture 提供）
    logged_in.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)

    # 2. 进入购物车并结算
    logged_in.go_to_cart()
    cart = CartPage(sb).wait_ready()
    assert cart.item_count() == 2
    cart.checkout()

    # 3. 填写收货信息
    checkout = CheckoutPage(sb).wait_ready()
    checkout.fill_shipping_info("Ze", "Keng", "430000")

    # 4. 订单确认页：总价应包含两件商品
    total = checkout.total_text()
    assert total.startswith("Total:"), f"总价文案异常：{total}"

    # 5. 完成下单
    checkout.finish()

    # 6. 断言下单成功
    assert checkout.complete_message() == "Thank you for your order!"
    assert "/checkout-complete.html" in sb.get_current_url()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, error_fragment",
    [
        ("", "Keng", "430000", "First Name is required"),    # 名未填
        ("Ze", "", "430000", "Last Name is required"),       # 姓未填
        ("Ze", "Keng", "", "Postal Code is required"),       # 邮编未填（边界值）
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code"],
)
def test_checkout_required_field_validation(
    sb, logged_in, first_name, last_name, postal_code, error_fragment
):
    """收货信息必填校验：缺任意一项都应拦截并给出提示。"""
    logged_in.add_to_cart(BACKPACK)
    logged_in.go_to_cart()

    cart = CartPage(sb).wait_ready()
    cart.checkout()

    checkout = CheckoutPage(sb).wait_ready()
    checkout.fill_shipping_info(first_name, last_name, postal_code)

    assert checkout.has_error(), "预期出现必填校验提示，但没有出现"
    assert error_fragment in checkout.error_message()
    assert "/checkout-step-one.html" in sb.get_current_url()
