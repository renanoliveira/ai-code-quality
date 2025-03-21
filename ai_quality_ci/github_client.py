from typing import Dict, List, Optional
import os
import tempfile
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from .code_analyzer import CodeAnalyzer
from .ai_reviewer import AIReviewer

class GitHubClient:
    """Client for interacting with GitHub PRs."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client.
        
        Args:
            token: GitHub token. If not provided, will try to get from GITHUB_TOKEN env var.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token not provided. Set GITHUB_TOKEN env var or pass token.")
        
        self.github = Github(self.token)
        self.analyzer = CodeAnalyzer()
        self.reviewer = AIReviewer()
    
    def get_pr(self, repo_url: str, pr_number: int) -> PullRequest:
        """Get a PR from a repository.
        
        Args:
            repo_url: Repository URL (e.g., 'owner/repo')
            pr_number: PR number
            
        Returns:
            PullRequest object
        """
        repo = self.github.get_repo(repo_url)
        return repo.get_pull(pr_number)
    
    def analyze_pr(self, repo_url: str, pr_number: int, **kwargs) -> Dict:
        """Analyze a GitHub PR.
        
        Args:
            repo_url: Repository URL (e.g., 'owner/repo')
            pr_number: PR number
            **kwargs: Additional arguments for AIReviewer
            
        Returns:
            Dict with analysis results and review comments
        """
        pr = self.get_pr(repo_url, pr_number)
        results = {}
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Get changed files
            changed_files = self._get_changed_files(pr)
            python_files = [f for f in changed_files if f.filename.endswith('.py')]
            
            for file in python_files:
                # Get file content
                file_path = os.path.join(temp_dir, file.filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w') as f:
                    f.write(file.patch)
                
                # Analyze file
                analysis = self.analyzer.analyze_file(file_path)
                review = self.reviewer.review(file_path, analysis, **kwargs)
                results[file.filename] = {
                    'analysis': analysis,
                    'review': review
                }
        
        return results
    
    def comment_on_pr(self, repo_url: str, pr_number: int, results: Dict) -> None:
        """Add review comments to a PR.
        
        Args:
            repo_url: Repository URL
            pr_number: PR number
            results: Analysis results
        """
        pr = self.get_pr(repo_url, pr_number)
        
        # Create review comment
        comment = self._format_review_comment(results)
        pr.create_issue_comment(comment)
    
    def _get_changed_files(self, pr: PullRequest) -> List:
        """Get list of changed files in PR."""
        return list(pr.get_files())
    
    def _format_review_comment(self, results: Dict) -> str:
        """Format review results as a markdown comment."""
        comment = "# AI Code Review Results 🔍\n\n"
        
        for filename, file_results in results.items():
            comment += f"## {filename}\n\n"
            
            review = file_results['review']
            if isinstance(review, str):
                comment += review
            elif isinstance(review, dict):
                for section, items in review.items():
                    comment += f"### {section.replace('_', ' ').title()}\n"
                    if isinstance(items, list):
                        for item in items:
                            comment += f"- {item}\n"
                    else:
                        comment += f"{items}\n"
            
            comment += "\n---\n\n"
        
        return comment
