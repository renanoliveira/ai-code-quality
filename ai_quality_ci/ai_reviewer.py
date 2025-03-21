"""AI-powered code review using OpenAI or Azure OpenAI"""

import os
import subprocess
from typing import Dict, Optional, List
import openai

class AIReviewer:
    """AI-powered code reviewer using GPT models."""
    
    def __init__(self, model: str = "gpt-4o", use_azure: bool = False, language: str = "en"):
        """Initialize AI reviewer.
        
        Args:
            model: Model to use for review
            use_azure: Whether to use Azure OpenAI
            language: Output language (e.g., 'en', 'pt-BR')
        """
        self.model = model
        self.use_azure = use_azure
        self.language = language
        
        if use_azure:
            openai.api_type = "azure"
            openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
            openai.api_version = "2024-02-01"
            openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        else:
            openai.api_type = "open_ai"
            openai.api_base = "https://api.openai.com/v1"
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def review(self, file_path: str, analysis_results: Dict, auto_apply: bool = False) -> Dict:
        """
        Review code using GPT model
        
        Args:
            file_path: Path to the file to review
            analysis_results: Results from static analysis
            auto_apply: If True, automatically apply suggested fixes and create a commit
        """
        # Prepare the prompt
        prompt = self._prepare_prompt(file_path, analysis_results, self.language)
        
        try:
            # Create chat completion
            if openai.api_type == "azure":
                response = openai.ChatCompletion.create(
                    engine=self.model,  # For Azure, model is specified as engine
                    messages=[
                        {"role": "system", "content": "You are an expert Python code reviewer. Provide detailed, actionable feedback with complete code examples in the specified language."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
            else:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert Python code reviewer. Provide detailed, actionable feedback with complete code examples in the specified language."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )

            # Parse response
            review = self._parse_response(response.choices[0].message.content)
            
            # Apply fixes if requested
            if auto_apply and review['code_fixes']:
                self._apply_fixes(file_path, review['code_fixes'])
                
            return review
            
        except Exception as e:
            print(f"Error during AI review: {str(e)}")
            return {
                "style_issues": ["Error during AI review"],
                "code_improvements": [],
                "documentation": [],
                "code_fixes": []
            }

    def _prepare_prompt(self, file_path: str, analysis_results: Dict, language: str) -> str:
        """Prepare the prompt for the AI model"""
        with open(file_path, 'r') as f:
            code = f.read()

        return f"""Review this Python code and provide detailed feedback with specific code fixes in {language}.

Code to review:
```python
{code}
```

Static Analysis Issues:
{analysis_results}

Please provide your review in this exact format:

1. Style Issues:
- List each style issue found
- Focus on PEP 8 compliance and readability
- Include line numbers where applicable

2. Code Improvements:
- List each code improvement needed
- Focus on performance, maintainability, and best practices
- Include specific reasons why the improvement is needed

3. Documentation:
- List documentation improvements needed
- Focus on docstrings, comments, and code clarity
- Include examples of good documentation

4. Code Fixes:
For each issue mentioned above, provide a complete code fix in this EXACT format:

[Issue: Brief title]
```python
# Problem: Detailed description of the issue
# Location: File and line number(s)
# Impact: Why this is important to fix

# Original code:
<paste the EXACT problematic code here, with NO modifications>

# Fixed code:
<paste the EXACT fixed code here, with ALL necessary imports and context>

# Explanation:
# - Why this fix is better
# - What potential issues it prevents
# - Any additional context needed
```

IMPORTANT RULES FOR CODE FIXES:
1. ALWAYS include the EXACT original code that needs to be replaced
2. ALWAYS include ALL necessary imports and context in the fixed code
3. Make sure the original code matches EXACTLY what's in the file
4. Indent both original and fixed code correctly
5. Do not skip any lines or context needed for the fix
6. If a fix requires multiple changes, show ALL changes needed
7. Format must be EXACTLY as shown above for automatic application

Remember to:
- Be specific and actionable
- Provide complete code examples
- Explain the reasoning behind each suggestion
- Consider the broader context of the codebase"""

    def _parse_response(self, response: str) -> Dict:
        """Parse the AI response into structured feedback"""
        sections = {
            "style_issues": [],
            "code_improvements": [],
            "documentation": [],
            "code_fixes": []
        }
        
        current_section = None
        code_block = []
        in_code_block = False
        current_fix_title = None
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "Style Issues:" in line:
                current_section = "style_issues"
            elif "Code Improvements:" in line:
                current_section = "code_improvements"
            elif "Documentation:" in line:
                current_section = "documentation"
            elif "Code Fixes:" in line:
                current_section = "code_fixes"
            elif line.startswith('```'):
                if in_code_block:
                    # End of code block
                    if current_fix_title and code_block:
                        sections["code_fixes"].append({
                            "title": current_fix_title,
                            "code": "\n".join(code_block)
                        })
                        code_block = []
                        current_fix_title = None
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
            elif in_code_block:
                code_block.append(line)
            elif line.startswith('[Issue:') and line.endswith(']'):
                # This is a fix title
                current_fix_title = line[1:-1]
            elif current_section and line.startswith('-'):
                sections[current_section].append(line[2:].strip())
                
        return sections

    def _apply_fixes(self, file_path: str, code_fixes: List[Dict]) -> None:
        """Apply code fixes and create a commit"""
        if not code_fixes:
            return

        # Create a backup of the original file
        backup_path = f"{file_path}.bak"
        os.system(f"cp {file_path} {backup_path}")

        try:
            # Read the original file
            with open(file_path, 'r') as f:
                content = f.read()

            # Apply each fix
            for fix in code_fixes:
                # Extract the original and fixed code from the fix
                if isinstance(fix, str):
                    # Skip if it's just a string (not a proper fix)
                    continue
                    
                fix_lines = fix['code'].split('\n')
                original_code = None
                fixed_code = None
                current_section = None
                
                for line in fix_lines:
                    line = line.strip()
                    if not line or line.startswith('```') or line.startswith('#'):
                        if line.startswith('# Original code:'):
                            current_section = 'original'
                        elif line.startswith('# Fixed code:'):
                            current_section = 'fixed'
                        elif line.startswith('#'):
                            current_section = None
                        continue
                    
                    if current_section == 'original':
                        if original_code is None:
                            original_code = line
                        else:
                            original_code += '\n' + line
                    elif current_section == 'fixed':
                        if fixed_code is None:
                            fixed_code = line
                        else:
                            fixed_code += '\n' + line

                if original_code and fixed_code:
                    # Replace the code
                    content = content.replace(original_code.strip(), fixed_code.strip())

            # Write the modified content back to the file
            with open(file_path, 'w') as f:
                f.write(content)

            # Create a git commit with the changes
            repo_root = os.path.dirname(os.path.dirname(file_path))
            subprocess.run(['git', 'add', file_path], cwd=repo_root)
            commit_message = "AI Code Review: Applied automatic fixes\n\n"
            for fix in code_fixes:
                if isinstance(fix, dict) and 'title' in fix:
                    commit_message += f"- {fix['title']}\n"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_root)

            # Remove the backup file
            os.remove(backup_path)
            print(f"\nSuccessfully applied {len(code_fixes)} fixes and created a commit.")

        except Exception as e:
            print(f"Error applying fixes: {str(e)}")
            # Restore from backup
            if os.path.exists(backup_path):
                os.system(f"mv {backup_path} {file_path}")
                print("Restored original file from backup.")
