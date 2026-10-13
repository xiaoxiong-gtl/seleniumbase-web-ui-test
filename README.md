# Web UI 自动化测试框架（基于 SeleniumBase）

基于 **SeleniumBase**（对 Selenium + pytest 的工程化封装）搭建的 Web UI 自动化测试框架，
目标站点为公开电商演示站 [saucedemo.com](https://www.saucedemo.com/)，
覆盖**登录 → 浏览商品 → 排序 → 加购 → 购物车 → 结算 → 下单成功**的完整业务链路。

## 技术栈

| 组件 | 版本 | 作用 |
|---|---|---|
| Python | 3.14.0 | 运行环境 |
| SeleniumBase | 4.55.2 | 框架基础，封装 Selenium + pytest |
| Selenium | 4.50.0 | 底层 WebDriver |
| pytest | 9.1.1 | 用例组织与运行 |
| pytest-html | 4.0.2 | 可视化测试报告 |
| pytest-xdist | 3.8.0 | 多进程并行执行 |

## 目录结构

```
.
├── practice/
│   ├── pages/                  # 页面对象层（POM）
│   │   ├── base_page.py        #   基类：封装等待与元素操作
│   │   ├── login_page.py       #   登录页
│   │   ├── inventory_page.py   #   商品列表页
│   │   ├── cart_page.py        #   购物车页
│   │   └── checkout_page.py    #   结算流程页
│   ├── conftest.py             # fixture：登录态复用
│   ├── testdata.py             # 测试数据集中管理
│   ├── test_login.py           # 登录用例（含参数化异常场景）
│   ├── test_inventory.py       # 商品展示与排序用例
│   ├── test_cart.py            # 购物车用例
│   └── test_checkout.py        # 结算用例（端到端 + 必填校验）
├── pytest.ini                  # pytest 配置
└── requirements.txt
```

## 运行方式

```bash
# 1. 安装依赖
python -m venv .venv-test
.venv-test/Scripts/python.exe -m pip install -r requirements.txt

# 2. 跑全部用例（无头模式，适合 CI）
.venv-test/Scripts/python.exe -m pytest practice/ --headless

# 3. 跑单个模块
.venv-test/Scripts/python.exe -m pytest practice/test_checkout.py --headless

# 4. 并行加速（4 个进程）
.venv-test/Scripts/python.exe -m pytest practice/ --headless -n 4
```



## 设计要点

**1. POM（Page Object Model）**
页面元素定位与业务操作封装在 `pages/` 下的 Page 类中，用例层只调用业务方法
（如 `login()`、`add_to_cart()`），不出现任何选择器。页面改版时只改 Page 类一处，用例不动。

**2. 显式等待替代硬等待**
`BasePage` 统一封装 `wait_for_element_visible` / `wait_for_element_clickable`，
按条件轮询而非 `sleep` 死等，解决页面异步渲染导致的偶发失败（flaky case）。

**3. fixture 管理登录态**
`conftest.py` 在 SeleniumBase 的 `sb` fixture（负责浏览器生命周期）之上再封一层
`logged_in`，需要登录态的用例直接依赖它，避免每条用例重复走一遍登录流程。

**4. 数据驱动**
测试数据集中在 `testdata.py`；同时用 `@pytest.mark.parametrize` 对
密码错误 / 账号锁定 / 用户名为空、以及结算页三类必填项缺失做参数化，
用一份代码覆盖多个等价类与边界值。

**5. 定位策略**
优先使用站点官方提供给自动化的 `data-test` 属性，而不是易变的 `class`。
（踩过的坑：站点的 class 值带尾随空格 `"inventory_item_name "`，
`@class='inventory_item_name'` 这种精确匹配会查不到元素。）

**6. 失败自动截图与报告**
用例失败时 SeleniumBase 自动保存现场截图到 `latest_logs/`，
配合 pytest-html 生成可视化报告 `reports/report.html`，便于快速定位问题。

## 测试结果

```
# 串行
15 passed in 73.80s

# 四进程并行（pytest-xdist -n 4）
15 passed in 24.32s
```

> 并行加速比约 **3.0×**（73.80s → 24.32s）。瓶颈主要在浏览器启动开销，
> 因此用例规模越大，并行的收益越明显；4 进程是本机的收益拐点，再往上加收益递减。

| 模块 | 用例数 | 覆盖内容 |
|---|---|---|
| test_login.py | 4 | 正常登录；密码错误 / 账号锁定 / 用户名为空（参数化） |
| test_inventory.py | 5 | 商品列表展示；价格升/降序、名称排序；加购角标 |
| test_cart.py | 2 | 商品带入购物车；移除商品 |
| test_checkout.py | 4 | 端到端下单链路；收货信息三类必填校验（参数化） |

## 持续集成（每日定时回归）

已接入两套 CI，步骤等价，任选其一即可：

| 方案 | 配置文件 | 触发方式 | 说明 |
|---|---|---|---|
| GitHub Actions | `.github/workflows/regression.yml` | 每日 09:17（北京）/ push / PR / 手动 | 真跑，构建结果在仓库 Actions 页可见 |
| Jenkins | `Jenkinsfile` | 每日 `H 1 * * *` | 声明式流水线，报告展示依赖 HTML Publisher 插件 |

流水线步骤：**检出代码 → 安装依赖 → 确认浏览器 → Chrome 无头 + 4 进程并行执行 → 上传测试报告与失败截图**。


失败通知：GitHub Actions 的定时任务失败时，会自动向仓库所有者发送邮件。

## 后续可扩展

- 接入 Allure 报告，展示每一步操作与断言详情
- 引入 Chrome / Edge 多浏览器矩阵（`strategy.matrix`），横向扩大多环境覆盖
- 增加用例覆盖率统计，量化接口与页面的覆盖情况
