# AI Quality CI 🔍🤖

**Python tool for AI-powered code quality analysis and review**  
Integrates static analysis (Pylint) with language models (OpenAI/Azure) to provide:
- Automatic detection of style issues and best practices
- Intelligent code improvement suggestions
- Automatic code fixes with commit generation
- Multi-language support for reports

## Key Features 💡

- **Code analysis** with Pylint
- **AI review** using OpenAI GPT or Azure OpenAI
- **Automatic fixes** with Git commit generation
- **Intuitive CLI** with multiple configuration options
- **Multi-language support** for reports (en, pt-BR, etc)
- **Continuous integration** via GitHub Actions

## Installation ⚙️

```bash
git clone https://github.com/your-username/ai-quality-ci.git
cd ai-quality-ci
pip install -r requirements.txt
```

## Configuration 🔧

### 🔑 OpenAI
```bash
export OPENAI_API_KEY="your-openai-key"
```

### 🔵 Azure OpenAI
```bash
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_KEY="your-azure-key"
```

### ⚙️ Configuration File (Optional)
Create `config.yaml` to customize:
```yaml
ai_review:
  model: gpt-4o          # Model to use
  use_azure: false       # Use Azure OpenAI?
  auto_apply: false      # Apply fixes automatically?
  language: en           # Report language
```

## Usage 🚀

### Basic Analysis
```bash
python -m ai_quality_ci review-files path/to/file.py
```

### Advanced Options:
| Option         | Description                               | Default     |
|----------------|------------------------------------------|-------------|
| `--model`      | LLM model (gpt-4o, gpt-3.5, claude-3, etc) | gpt-4o     |
| `--use-azure`  | Use Azure OpenAI                         | false       |
| `--auto-apply` | Apply fixes automatically + commit        | false       |
| `--language`   | Report language (en, pt-BR, es)          | en          |

### Practical Examples:
**1. Analysis with Azure OpenAI:**
```bash
python -m ai_quality_ci review-files \
  --use-azure \
  --model gpt-4o \
  mycode.py
```

**2. Automatic Fix + Commit:**
```bash
python -m ai_quality_ci review-files \
  --auto-apply \
  --language pt-BR \
  src/*.py
```

**3. Full Project Analysis:**
```bash
python -m ai_quality_ci review-files \
  --model claude-3-sonnet \
  --language en \
  $(find . -name '*.py')
```

## Example Output 📄
```plaintext
🔍 Analyzing algorithm.py...

✅ Style Issues:
- [Line 12] Generic variable name 'x'
- [Line 5] Missing docstring in function calculate_metrics

🚀 Code Improvements:
- [Line 32] Replace loop with list comprehension
- [Line 47] Missing exception handling

📝 Documentation:
- Add docstring explaining Regressor class parameters

🔧 Automatically Applied Fixes:
- Renamed 'x' to 'metrics_result' [Commit #a1b2c3d]
- Added try/except for zero division handling [Commit #d4e5f6a]
```

## Auto Fix Example 🛠️

Here's a practical example of how the auto fix feature works:

### Original Code:
```python
def calculate_average(x):
    total = 0
    for i in range(len(x)):
        total = total + x[i]
    return total / len(x)
```

### AI Review Output:
```plaintext
🔍 Analyzing calculate_average function...

✅ Style Issues:
- Generic parameter name 'x'
- Missing function docstring
- Loop can be simplified

🚀 Suggested Fixes:
1. Add descriptive parameter name
2. Add docstring
3. Use sum() function
4. Add error handling for empty list
```

### Auto-Applied Fixes:
```python
def calculate_average(numbers: list) -> float:
    """Calculate the arithmetic mean of a list of numbers.
    
    Args:
        numbers (list): List of numerical values
        
    Returns:
        float: The arithmetic mean of the input list
        
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

### Git Commit:
```bash
commit a1b2c3d4e5f6g7h8i9j0k
Author: AI Quality CI <ai@quality.ci>
Date: Fri Mar 21 11:32:27 2025 -0300

refactor: Improve calculate_average function
- Add type hints
- Add comprehensive docstring
- Use sum() for better readability
- Add empty list validation
- Rename parameter for clarity
```

The auto fix feature automatically:
1. Analyzes the code for improvements
2. Applies the suggested fixes
3. Creates a Git commit with detailed changes
4. Maintains code history and traceability

## Contributing 🤝
Contributions are welcome! See our [Contributing Guide](CONTRIBUTING.md).

## License 📜
MIT License - See [LICENSE](LICENSE) for details.
