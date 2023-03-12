import allure


class TestDemo:

    def setup_class(self):
        with allure.step("类前置"):
            pass

    def teardown_class(self):
        with allure.step("类后置"):
            ...

    def setup_method(self):
        with allure.step("方法前置"):
            ...

    def teardown_method(self):
        with allure.step("方法后置"):
            ...

    def test_success(self):
        ...

    def test_failed(self):
        assert 1 + 1 == 0, "1+1 不等于 0"

    def test_01(self):
        with allure.step("123"):
            pass
