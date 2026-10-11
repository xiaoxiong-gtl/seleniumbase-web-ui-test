"""页面对象（Page Object）基类。

设计意图：把「元素定位」和「浏览器操作细节」收敛在这一层，
测试用例层只调用业务方法（如 login / add_to_cart），不出现任何选择器。
这样页面改版时只改 Page 类一处，用例代码不动 —— 即简历里写的「改版只改一处」。
"""


class BasePage:
    """所有 Page 类的父类。

    driver 传入的是 SeleniumBase 的 BaseCase 实例（也就是测试类自己），
    页面类通过它调用 SeleniumBase 封装好的浏览器能力，
    底层依然是原生 Selenium WebDriver，必要时可直接取 .driver.driver。
    """

    URL = None        # 子类覆盖：页面绝对地址
    PAGE_READY = None  # 子类覆盖：页面「加载完成」的标志元素

    def __init__(self, driver):
        self.driver = driver

    # ---------------- 导航 ----------------
    def open(self):
        """打开页面并等待其就绪。"""
        assert self.URL, f"{type(self).__name__} 未定义 URL"
        self.driver.open(self.URL)
        self.wait_ready()
        return self

    def wait_ready(self, timeout=10):
        """显式等待标志元素可见，替代硬编码 sleep。

        硬等待是「不管页面好没好都睡 N 秒」，既浪费时间又不稳定；
        显式等待是按条件轮询，元素一出现立刻继续，这是解决 flaky 用例的关键。
        """
        if self.PAGE_READY:
            self.driver.wait_for_element_visible(self.PAGE_READY, timeout=timeout)
        return self

    # ---------------- 元素操作 ----------------
    def click(self, selector, timeout=10):
        """等待元素可点击后再点，避免元素尚未就绪导致的偶发失败。"""
        self.driver.wait_for_element_clickable(selector, timeout=timeout)
        self.driver.click(selector)
        return self

    def type_text(self, selector, text, timeout=10):
        self.driver.wait_for_element_visible(selector, timeout=timeout)
        self.driver.type(selector, text)
        return self

    def select_by_text(self, selector, text, timeout=10):
        self.driver.wait_for_element_visible(selector, timeout=timeout)
        self.driver.select_option_by_text(selector, text)
        return self

    # ---------------- 读取 / 断言 ----------------
    def text_of(self, selector, timeout=10):
        self.driver.wait_for_element_visible(selector, timeout=timeout)
        return self.driver.get_text(selector)

    def texts_of(self, selector, timeout=10):
        """取一组元素的文本，返回列表。"""
        self.driver.wait_for_element_visible(selector, timeout=timeout)
        return [el.text for el in self.driver.find_elements(selector)]

    def is_visible(self, selector, timeout=2):
        """在 timeout 内元素是否出现，用于「存在 / 不存在」这类分支判断。

        注意要用「等待 + 捕获异常」实现，而不是 is_element_visible：
        后者是瞬时判断，页面还在渲染时会误判为不可见。
        """
        try:
            self.driver.wait_for_element_visible(selector, timeout=timeout)
            return True
        except Exception:
            return False

    def count_of(self, selector):
        return len(self.driver.find_elements(selector))

    def current_url(self):
        return self.driver.get_current_url()
