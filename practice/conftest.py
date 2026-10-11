"""pytest 全局 fixture。

分层说明：
1. 浏览器生命周期 —— 由 SeleniumBase 自带的 sb fixture 负责，
   每条用例一个干净的浏览器实例，用完自动关闭（含失败截图）。
2. 登录态复用 —— 本文件在 sb 之上再封一层 logged_in：
   需要「已登录」的用例直接依赖它，不必每条用例重复 open + login。
   这既省时间（少一次完整登录流程），也让用例只表达业务意图。
"""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from testdata import PASSWORD, STANDARD_USER


@pytest.fixture
def login_page(sb):
    """已打开、未登录的登录页对象。"""
    return LoginPage(sb).open()


@pytest.fixture
def logged_in(sb):
    """已登录状态，返回商品列表页对象 —— 供绝大多数用例复用。

    注意：logged_in 依赖 sb，同一条用例里再注入 sb 拿到的是同一个浏览器实例，
    所以可以在 logged_in 上操作后，用 sb 构造别的页面对象继续走流程。
    """
    LoginPage(sb).open().login(STANDARD_USER, PASSWORD)
    return InventoryPage(sb).wait_ready()
