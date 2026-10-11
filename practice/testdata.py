"""测试数据集中管理。

账号、密码、商品名等易变数据抽到一处，
用例层只引用常量，改数据不用翻遍用例 —— 这也是「数据驱动」的基础。
"""

# ---------------- 站点 ----------------
BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"

# ---------------- 账号 ----------------
STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"

# ---------------- 商品 ----------------
BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"

# ---------------- 预期值 ----------------
EXPECTED_PRODUCT_COUNT = 6  # 商品列表页商品总数
