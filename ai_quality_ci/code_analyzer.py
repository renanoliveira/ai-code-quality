"""Code quality analysis using Pylint"""

import os
import tempfile
from typing import Dict, List
from pylint import lint
from pylint.reporters import JSONReporter

class CodeAnalyzer:
    """Code quality analyzer using Pylint"""
    
    def analyze(self, files: List[Dict]) -> Dict:
        """Analyze code quality using Pylint"""
        results = {
            'style_issues': [],
            'quality_issues': []
        }
        
        for file_info in files:
            # Create temporary file for analysis
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as temp_file:
                temp_file.write(file_info['content'])
                temp_file.flush()
                
                # Run Pylint
                reporter = JSONReporter()
                lint.Run([temp_file.name], reporter=reporter, exit=False)
                
                # Process Pylint results
                for msg in reporter.messages:
                    issue = {
                        'file': file_info['name'],
                        'line': msg.line,
                        'message': msg.msg
                    }
                    
                    if msg.symbol.startswith(('C', 'R')):  # Convention and Refactor
                        results['style_issues'].append(issue)
                    else:  # Warning and Error
                        results['quality_issues'].append(issue)
        
        return results
