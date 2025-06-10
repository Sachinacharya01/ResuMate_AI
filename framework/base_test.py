import pytest
from framework.logger import get_logger

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Setting up test: {self.__class__.__name__}")
        yield
        self.logger.info(f"Tearing down test: {self.__class__.__name__}")
