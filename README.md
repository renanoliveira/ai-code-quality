# AI Quality CI

A simple Python tool that combines Pylint with OpenAI to provide AI-powered code quality analysis and suggestions.

## Features

- Code quality analysis using Pylint
- AI-powered code review suggestions using OpenAI
- Command-line interface for analyzing Python files

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key
```

2. (Optional) Create a `config.yaml` file to customize settings:
```yaml
ai_review:
  model: gpt-3.5-turbo  # or gpt-4
```

## Usage

Review Python files:
```bash
python -m ai_quality_ci review-files path/to/file1.py path/to/file2.py
```

Options:
- `--model`: Specify OpenAI model (default: gpt-3.5-turbo)

## Example Output

```
Analyzing example.py...

Style Issues:
- Consider using more descriptive variable names
- Add docstrings to functions

Code Improvements:
- Use list comprehension instead of for loop
- Consider adding error handling

Documentation:
- Add module-level docstring
- Document function parameters
