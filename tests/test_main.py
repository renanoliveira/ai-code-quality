import pytest
from unittest.mock import patch
from click.testing import CliRunner
from ai_quality_ci.__main__ import review_files

@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing"""
    return CliRunner()

def test_review_files_basic(cli_runner, sample_python_file):
    """Test basic file review command"""
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [str(sample_python_file)])
        
        assert result.exit_code == 0
        assert mock_review.called

def test_review_files_with_options(cli_runner, sample_python_file):
    """Test file review with various options"""
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [
            str(sample_python_file),
            '--model', 'gpt-4o',
            '--language', 'en',
            '--use-azure',
            '--auto-apply'
        ])
        
        assert result.exit_code == 0
        assert mock_review.called
        args, kwargs = mock_review.call_args
        assert kwargs.get('auto_apply') is True

def test_review_multiple_files(cli_runner, tmp_path):
    """Test reviewing multiple files"""
    file1 = tmp_path / "test1.py"
    file2 = tmp_path / "test2.py"
    file1.write_text("def test1(): pass")
    file2.write_text("def test2(): pass")
    
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [str(file1), str(file2)])
        
        assert result.exit_code == 0
        assert mock_review.call_count == 2

def test_review_files_error_handling(cli_runner):
    """Test error handling for non-existent files"""
    result = cli_runner.invoke(review_files, ['nonexistent.py'])
    assert result.exit_code != 0
    assert "Error" in result.output

def test_review_files_with_config(cli_runner, sample_python_file, sample_config_file):
    """Test file review with configuration file"""
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [
            str(sample_python_file),
            '--config', str(sample_config_file)
        ])
        
        assert result.exit_code == 0
        assert mock_review.called

@pytest.mark.parametrize("model", ["gpt-4o", "gpt-3.5-turbo", "claude-3"])
def test_review_files_different_models(cli_runner, sample_python_file, model):
    """Test review with different AI models"""
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [
            str(sample_python_file),
            '--model', model
        ])
        
        assert result.exit_code == 0
        assert mock_review.called

def test_review_files_with_auto_apply(cli_runner, sample_python_file):
    """Test auto-apply functionality"""
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Changes applied"
        result = cli_runner.invoke(review_files, [
            str(sample_python_file),
            '--auto-apply'
        ])
        
        assert result.exit_code == 0
        assert "Changes applied" in result.output

def test_review_files_environment_variables(cli_runner, sample_python_file, monkeypatch):
    """Test environment variable handling"""
    monkeypatch.setenv('OPENAI_API_KEY', 'test-key')
    monkeypatch.setenv('AZURE_OPENAI_KEY', 'azure-key')
    
    with patch('ai_quality_ci.ai_reviewer.AIReviewer.review') as mock_review:
        mock_review.return_value = "Analysis complete"
        result = cli_runner.invoke(review_files, [str(sample_python_file)])
        
        assert result.exit_code == 0
        assert mock_review.called
