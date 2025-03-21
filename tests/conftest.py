import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_openai():
    """Mock OpenAI client"""
    mock = MagicMock()
    mock.chat.completions.create.return_value.choices[0].message.content = (
        "✅ Style Issues:\n"
        "- [Line 5] Missing docstring\n"
        "🚀 Code Improvements:\n"
        "- [Line 10] Use list comprehension\n"
        "📝 Documentation:\n"
        "- Add type hints\n"
        "🔧 Code Fixes:\n"
        "```python\n"
        "def calculate_sum(numbers: List[int]) -> int:\n"
        "    \"\"\"Calculate sum of numbers.\"\"\"\n"
        "    return sum(numbers)\n"
        "```"
    )
    return mock

@pytest.fixture
def mock_azure_openai():
    """Mock Azure OpenAI client"""
    mock = MagicMock()
    mock.chat.completions.create.return_value.choices[0].message.content = (
        "✅ Style Issues:\n"
        "- [Line 5] Missing docstring\n"
        "🚀 Code Improvements:\n"
        "- [Line 10] Use list comprehension\n"
    )
    return mock

@pytest.fixture
def sample_python_file(tmp_path):
    """Create a sample Python file for testing"""
    file_content = """
def calculate_sum(x):
    total = 0
    for i in range(len(x)):
        total = total + x[i]
    return total
"""
    file_path = tmp_path / "sample.py"
    file_path.write_text(file_content)
    return file_path

@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample config file for testing"""
    config_content = """
ai_review:
  model: gpt-4o
  use_azure: false
  language: en
"""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(config_content)
    return config_path
