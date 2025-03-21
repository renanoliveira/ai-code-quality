# AI Quality CI

A tool for automated code review using AI models (OpenAI GPT-4, Azure OpenAI) and static analysis.

## Features

- AI-powered code review using OpenAI GPT-4 or Azure OpenAI
- Static code analysis using pylint
- Human-readable output format
- Support for reviewing multiple Python files
- Customizable AI provider and model selection

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Review a single Python file:
```bash
python -m ai_quality_ci review-files path/to/file.py --provider azure --model gpt-4o
```

Review with human-readable output:
```bash
python -m ai_quality_ci review-files path/to/file.py --provider azure --model gpt-4o --human-readable
```

Show suggested code fixes:
```bash
python -m ai_quality_ci review-files path/to/file.py --provider azure --model gpt-4o --show-fixes
```

## Environment Variables

For Azure OpenAI:
```bash
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_KEY="your-key"
```

For OpenAI:
```bash
export OPENAI_API_KEY="your-key"
```

## License

MIT
