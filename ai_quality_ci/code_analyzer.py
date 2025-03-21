"""Static code analysis using pylint."""

import os
import sys
import json
from typing import Dict, List, Optional
from pylint.lint import Run
from pylint.reporters import JSONReporter
from io import StringIO

class CodeAnalyzer:
    """Static code analyzer using pylint."""
    
    def __init__(self):
        """Initialize CodeAnalyzer."""
        pass
        
    def analyze_file(self, file_path: str) -> List[Dict]:
        """Analyze a single Python file.
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            List of analysis results
        """
        # Capture stdout to prevent pylint from printing to console
        stdout = StringIO()
        reporter = JSONReporter(stdout)
        
        # Run pylint
        Run([file_path], reporter=reporter, exit=False)
        
        # Parse results
        output = stdout.getvalue()
        if output:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                pass
                
        return []
        
    def analyze_directory(self, directory: str) -> Dict[str, List[Dict]]:
        """Analyze all Python files in directory.
        
        Args:
            directory: Directory to analyze
            
        Returns:
            Dictionary mapping file paths to analysis results
        """
        results = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.analyze_file(file_path)
                    
        return results
