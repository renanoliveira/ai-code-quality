"""AI-powered code review using OpenAI or Azure OpenAI"""

import os
import subprocess
from typing import Dict, Optional, List
import openai
import json

class AIReviewer:
    """AI-powered code reviewer using GPT models."""
    
    SUPPORTED_PROVIDERS = {
        'openai': {
            'models': ['gpt-4o', 'gpt-4', 'gpt-3.5-turbo'],
            'default': 'gpt-4o'
        },
        'azure': {
            'models': ['gpt-4o', 'gpt-4', 'gpt-35-turbo', 'gpt-35-turbo-16k'],
            'default': 'gpt-4o'
        },
        'claude': {
            'models': ['claude-3-opus', 'claude-3-sonnet', 'claude-3'],
            'default': 'claude-3-opus'
        },
        'deepseek': {
            'models': ['deepseek-coder'],
            'default': 'deepseek-coder'
        }
    }
    
    def __init__(self, provider: str = "azure", model: str = "gpt-4o", language: str = "en"):
        """Initialize AIReviewer with provider and model."""
        self.provider = provider
        self.model = model
        self.language = language
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client based on the provider."""
        if self.provider == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider")
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "azure":
            if not os.getenv("AZURE_OPENAI_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"):
                raise ValueError("AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT environment variables are required for Azure provider")
            self.client = openai.AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version="2024-02-01",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            # Map model names to deployment IDs
            self.deployment_id = {
                'gpt-4o': 'gpt-4o',
                'gpt-4': 'gpt-4',
                'gpt-35-turbo': 'gpt-35-turbo',
                'gpt-35-turbo-16k': 'gpt-35-turbo-16k'
            }.get(self.model, self.model)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _prepare_prompt(self, file_path: str, analysis_results: Dict) -> str:
        """Prepare prompt for AI review.
        
        Args:
            file_path: Path to file to review
            analysis_results: Results from static analysis
            
        Returns:
            Formatted prompt string
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            code = ""
            
        prompt = f"Review the following Python code and provide feedback in {self.language}.\n\n"
        prompt += "Code to review:\n```python\n"
        prompt += code
        prompt += "\n```\n\n"
        
        if analysis_results:
            prompt += "Static analysis results:\n"
            if isinstance(analysis_results, list):
                for result in analysis_results:
                    prompt += f"- {result['type']}: {result['message']} (Line {result['line']})\n"
            else:
                prompt += f"- {analysis_results['type']}: {analysis_results['message']} (Line {analysis_results['line']})\n"
        
        prompt += "\nPlease provide a detailed review including:\n"
        prompt += "1. Style Issues\n"
        prompt += "2. Code Improvements\n"
        prompt += "3. Documentation\n"
        prompt += "4. Code Fixes\n\n"
        prompt += "Format your response as a JSON with the following structure:\n"
        prompt += "{\n"
        prompt += '  "style_issues": ["issue1", "issue2", ...],\n'
        prompt += '  "code_improvements": ["improvement1", "improvement2", ...],\n'
        prompt += '  "documentation": ["doc1", "doc2", ...],\n'
        prompt += '  "code_fixes": {\n'
        prompt += '    "fix1_title": {"description": "...", "fix": "code here"},\n'
        prompt += '    "fix2_title": {"description": "...", "fix": "code here"}\n'
        prompt += "  }\n"
        prompt += "}\n"
        
        return prompt

    def review(self, file_path: str, analysis_results: Dict, auto_apply: bool = False) -> Dict:
        """Review code using selected AI provider.
        
        Args:
            file_path: Path to file to review
            analysis_results: Results from static analysis
            auto_apply: Whether to automatically apply fixes
            
        Returns:
            Review results dictionary
        """
        try:
            prompt = self._prepare_prompt(file_path, analysis_results)
            
            if self.provider == "azure":
                response = self.client.chat.completions.create(
                    model=self.deployment_id,
                    messages=[
                        {"role": "system", "content": "Você é um revisor de código Python especializado em identificar problemas de estilo, melhorias de código e documentação. Sempre forneça sugestões de correção no formato especificado."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                raw_response = response.choices[0].message.content
                
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert Python code reviewer. Provide detailed, actionable feedback with complete code examples in the specified language."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                raw_response = response.choices[0].message.content
                
            print("\nAI Response:", raw_response)  # Debug
            result = self._parse_response(raw_response)
            print("\nParsed Result:", json.dumps(result, indent=2))  # Debug
            
            # Apply fixes if requested
            if auto_apply and result.get("code_fixes", {}) and file_path:
                for fix_title, fix_info in result["code_fixes"].items():
                    try:
                        if isinstance(fix_info, dict) and "fix" in fix_info:
                            # Clean up code fix
                            code_fix = fix_info["fix"]
                            if code_fix.startswith("```"):
                                code_fix = code_fix[code_fix.find("\n")+1:]
                            if code_fix.endswith("```"):
                                code_fix = code_fix[:code_fix.rfind("```")]
                                
                            # Remove leading/trailing whitespace and empty lines
                            code_fix = "\n".join(line for line in code_fix.split("\n") 
                                             if line.strip())
                            
                            with open(file_path, "w") as f:
                                f.write(code_fix)
                    except (IOError, FileNotFoundError):
                        pass
                    
            return result
            
        except Exception as e:
            print(f"\nError during AI review: {str(e)}")  # Debug
            return {
                "error": f"Error during AI review: {str(e)}",
                "style_issues": [],
                "code_improvements": [],
                "documentation": [],
                "code_fixes": {}
            }

    def _parse_response(self, response: str) -> Dict:
        """Parse AI response into structured format.
        
        Args:
            response: Raw response from AI
            
        Returns:
            Parsed response dictionary
        """
        try:
            # Find the JSON block
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "error": "Could not find JSON in response",
                    "style_issues": [],
                    "code_improvements": [],
                    "documentation": [],
                    "code_fixes": {}
                }
        except Exception as e:
            print(f"Error parsing response: {str(e)}")  # Debug
            return {
                "error": f"Error parsing response: {str(e)}",
                "style_issues": [],
                "code_improvements": [],
                "documentation": [],
                "code_fixes": {}
            }
