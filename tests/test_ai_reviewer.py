import pytest
from unittest.mock import patch, MagicMock
from ai_quality_ci.ai_reviewer import AIReviewer

def test_ai_reviewer_initialization():
    """Test AIReviewer initialization with default settings"""
    reviewer = AIReviewer()
    assert reviewer.model == "gpt-4o"
    assert not reviewer.use_azure
    assert reviewer.language == "en"

def test_ai_reviewer_custom_settings():
    """Test AIReviewer initialization with custom settings"""
    reviewer = AIReviewer(model="gpt-3.5-turbo", use_azure=True, language="pt-BR")
    assert reviewer.model == "gpt-3.5-turbo"
    assert reviewer.use_azure
    assert reviewer.language == "pt-BR"

def test_prepare_prompt(sample_python_file):
    """Test prompt preparation with sample file"""
    reviewer = AIReviewer()
    analysis_results = {"style_issues": ["Missing docstring"], "complexity": "Low"}
    prompt = reviewer._prepare_prompt(str(sample_python_file), analysis_results)
    
    assert "calculate_sum" in prompt
    assert "Missing docstring" in prompt
    assert "complexity: Low" in prompt

@patch('openai.OpenAI')
def test_review_with_openai(mock_openai_class, mock_openai, sample_python_file):
    """Test code review using OpenAI"""
    mock_openai_class.return_value = mock_openai
    reviewer = AIReviewer(use_azure=False)
    
    analysis_results = {"style_issues": ["Missing docstring"]}
    result = reviewer.review(str(sample_python_file), analysis_results)
    
    assert "Style Issues" in result
    assert "Code Improvements" in result
    assert mock_openai.chat.completions.create.called

@patch('openai.AzureOpenAI')
def test_review_with_azure(mock_azure_class, mock_azure_openai, sample_python_file):
    """Test code review using Azure OpenAI"""
    mock_azure_class.return_value = mock_azure_openai
    reviewer = AIReviewer(use_azure=True)
    
    analysis_results = {"style_issues": ["Missing docstring"]}
    result = reviewer.review(str(sample_python_file), analysis_results)
    
    assert "Style Issues" in result
    assert "Code Improvements" in result
    assert mock_azure_openai.chat.completions.create.called

def test_parse_response():
    """Test parsing of AI response"""
    reviewer = AIReviewer()
    response = """
    ✅ Style Issues:
    - Missing docstring
    
    🚀 Code Improvements:
    - Use list comprehension
    
    🔧 Code Fixes:
    ```python
    def improved_function():
        pass
    ```
    """
    
    parsed = reviewer._parse_response(response)
    assert "style_issues" in parsed
    assert "improvements" in parsed
    assert "code_fixes" in parsed
    assert "improved_function" in parsed["code_fixes"]

@pytest.mark.parametrize("language,expected", [
    ("en", "Analyze the following Python code"),
    ("pt-BR", "Analise o seguinte código Python"),
])
def test_language_support(language, expected):
    """Test different language support"""
    reviewer = AIReviewer(language=language)
    analysis_results = {"style_issues": []}
    prompt = reviewer._prepare_prompt("def test(): pass", analysis_results)
    assert expected in prompt

def test_auto_apply_fixes(sample_python_file, tmp_path):
    """Test automatic application of code fixes"""
    reviewer = AIReviewer()
    fixes = {
        "code_fixes": """
def calculate_sum(numbers: list) -> int:
    \"\"\"Calculate the sum of numbers in a list.\"\"\"
    return sum(numbers)
"""
    }
    
    with patch.object(reviewer, '_parse_response', return_value=fixes):
        result = reviewer.review(str(sample_python_file), {}, auto_apply=True)
        
        # Verify the file was modified
        updated_content = sample_python_file.read_text()
        assert "numbers: list" in updated_content
        assert "Calculate the sum" in updated_content

@pytest.mark.parametrize("model", ["gpt-4o", "gpt-3.5-turbo", "claude-3"])
def test_different_models(model, mock_openai):
    """Test support for different AI models"""
    reviewer = AIReviewer(model=model)
    assert reviewer.model == model
    
    with patch('openai.OpenAI', return_value=mock_openai):
        result = reviewer.review("def test(): pass", {})
        assert result is not None

def test_invalid_configuration():
    """Test handling of invalid configuration"""
    with pytest.raises(ValueError):
        AIReviewer(model="invalid-model")
    
    with pytest.raises(ValueError):
        AIReviewer(language="invalid-lang")
