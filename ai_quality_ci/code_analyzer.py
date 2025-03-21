from typing import Dict, List, Union
import os
from pylint import lint
from pylint.reporters import JSONReporter
import tempfile

class CodeAnalyzer:
    """Analyzes Python code for quality and style issues."""
    
    def __init__(self, ignore_patterns: List[str] = None, pylint_config: str = None):
        """Initialize code analyzer.
        
        Args:
            ignore_patterns: List of glob patterns to ignore
            pylint_config: Path to pylint config file
        """
        self.ignore_patterns = ignore_patterns or []
        self.pylint_config = pylint_config
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a single Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dict with analysis results
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Create temporary file for pylint output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as tmp:
            args = ['--output-format=json', '--output=' + tmp.name]
            
            if self.pylint_config:
                args.append('--rcfile=' + self.pylint_config)
            
            args.append(file_path)
            
            try:
                lint.Run(args, exit=False)
                tmp.seek(0)
                issues = eval(tmp.read() or '[]')
            except Exception as e:
                issues = [{'message': f'Error analyzing file: {str(e)}'}]
        
        # Process issues
        style_issues = []
        complexity = "Low"
        
        for issue in issues:
            msg = issue.get('message', '')
            if 'complexity' in msg.lower():
                complexity = "High" if 'too high' in msg.lower() else "Medium"
            style_issues.append(msg)
        
        return {
            'style_issues': style_issues,
            'complexity': complexity
        }
    
    def analyze_files(self, files: List[str]) -> Dict[str, Dict]:
        """Analyze multiple Python files.
        
        Args:
            files: List of file paths
            
        Returns:
            Dict mapping file paths to analysis results
        """
        results = {}
        for file_path in files:
            if any(pattern in file_path for pattern in self.ignore_patterns):
                continue
            results[file_path] = self.analyze_file(file_path)
        return results
