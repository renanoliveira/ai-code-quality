import pytest
from unittest.mock import MagicMock, patch
from github.PullRequest import PullRequest
from github.File import File
from ai_quality_ci.github_client import GitHubClient

@pytest.fixture
def mock_github():
    """Mock GitHub API client"""
    with patch('github.Github') as mock:
        yield mock

@pytest.fixture
def mock_pr():
    """Mock GitHub PR"""
    pr = MagicMock(spec=PullRequest)
    
    # Mock files in PR
    file1 = MagicMock(spec=File)
    file1.filename = "test.py"
    file1.patch = """
def test_function():
    x = 1
    return x
"""
    
    file2 = MagicMock(spec=File)
    file2.filename = "not_python.txt"
    file2.patch = "Some text content"
    
    pr.get_files.return_value = [file1, file2]
    return pr

def test_github_client_initialization():
    """Test GitHubClient initialization"""
    with pytest.raises(ValueError):
        GitHubClient()  # Should fail without token
    
    client = GitHubClient("test-token")
    assert client.token == "test-token"

def test_get_pr(mock_github):
    """Test getting a PR from GitHub"""
    client = GitHubClient("test-token")
    repo = mock_github.return_value.get_repo.return_value
    repo.get_pull.return_value = "test-pr"
    
    pr = client.get_pr("owner/repo", 123)
    
    assert pr == "test-pr"
    mock_github.return_value.get_repo.assert_called_with("owner/repo")
    repo.get_pull.assert_called_with(123)

def test_analyze_pr(mock_github, mock_pr, mock_openai):
    """Test PR analysis"""
    mock_github.return_value.get_repo.return_value.get_pull.return_value = mock_pr
    
    client = GitHubClient("test-token")
    results = client.analyze_pr("owner/repo", 123)
    
    assert "test.py" in results
    assert "not_python.txt" not in results
    assert "analysis" in results["test.py"]
    assert "review" in results["test.py"]

def test_comment_on_pr(mock_github, mock_pr):
    """Test commenting on a PR"""
    mock_github.return_value.get_repo.return_value.get_pull.return_value = mock_pr
    
    client = GitHubClient("test-token")
    results = {
        "test.py": {
            "analysis": {"style_issues": ["Missing docstring"]},
            "review": "Add docstring to improve documentation"
        }
    }
    
    client.comment_on_pr("owner/repo", 123, results)
    mock_pr.create_issue_comment.assert_called_once()
    comment = mock_pr.create_issue_comment.call_args[0][0]
    assert "AI Code Review Results" in comment
    assert "test.py" in comment

def test_pr_with_no_python_files(mock_github, mock_pr):
    """Test PR analysis with no Python files"""
    # Modify mock to return no Python files
    mock_pr.get_files.return_value = [
        MagicMock(filename="file1.txt", patch="content"),
        MagicMock(filename="file2.js", patch="content")
    ]
    mock_github.return_value.get_repo.return_value.get_pull.return_value = mock_pr
    
    client = GitHubClient("test-token")
    results = client.analyze_pr("owner/repo", 123)
    
    assert len(results) == 0

def test_pr_with_invalid_files(mock_github, mock_pr):
    """Test PR analysis with invalid Python files"""
    # Modify mock to return invalid Python code
    mock_pr.get_files.return_value = [
        MagicMock(filename="invalid.py", patch="def invalid_syntax(:")
    ]
    mock_github.return_value.get_repo.return_value.get_pull.return_value = mock_pr
    
    client = GitHubClient("test-token")
    results = client.analyze_pr("owner/repo", 123)
    
    assert "invalid.py" in results
    assert "syntax error" in str(results["invalid.py"]["analysis"]).lower()

@pytest.mark.parametrize("review_format", [
    "string format",
    {"section": ["item1", "item2"]},
    {"style_issues": ["issue1"], "improvements": ["imp1"]}
])
def test_format_review_comment(mock_github, review_format):
    """Test different review comment formats"""
    client = GitHubClient("test-token")
    results = {
        "test.py": {
            "analysis": {},
            "review": review_format
        }
    }
    
    comment = client._format_review_comment(results)
    assert "AI Code Review Results" in comment
    assert "test.py" in comment
