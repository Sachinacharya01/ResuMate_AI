import pytest
from utils import parser
from framework.base_test import BaseTest

class TestParser(BaseTest):

    def test_parse_resume_text(self, sample_resume_text):
        self.logger.info("Testing resume parsing...")
        parsed = parser.parse_resume(sample_resume_text)
        self.logger.debug(f"Parsed output: {parsed}")
        
        assert isinstance(parsed, dict)
        assert "skills" in parsed  # ✅ use lowercase key
        assert "python" in parsed["tokens"]  # ✅ optional keyword check
