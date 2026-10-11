"""登录功能用例：正常登录 + 异常场景（参数化）。

参数化把「同一套步骤、不同数据」的用例写成一份代码，
覆盖 正常 / 密码错误 / 账号锁定 / 用户名为空 四类等价类，
比复制四遍用例更好维护 —— 这就是面试常问的「数据驱动」。
"""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata import BASE_URL, LOCKED_USER, PASSWORD, STANDARD_USER


def test_login_success(sb):
    """正常用户 + 正确密码 → 进入商品列表页。"""
    LoginPage(sb).open().login(STANDARD_USER, PASSWORD)
    InventoryPage(sb).wait_ready()

    assert "/inventory.html" in sb.get_current_url()


@pytest.mark.parametrize(
    "username, password, error_fragment",
    [
        (STANDARD_USER, "wrong_password", "do not match"),   # 密码错误
        (LOCKED_USER, PASSWORD, "locked out"),               # 账号被锁定
        ("", PASSWORD, "Username is required"),              # 用户名为空（边界值）
    ],
    ids=["wrong_password", "locked_out_user", "empty_username"],
)
def test_login_failure(sb, username, password, error_fragment):
    """异常场景：均应停留在登录页并给出对应错误提示。"""
    page = LoginPage(sb).open()
    page.login(username, password)

    assert page.has_error(), "预期出现错误提示，但没有出现"
    assert error_fragment in page.error_message()
    assert sb.get_current_url() == BASE_URL, "登录失败不应跳转页面"
