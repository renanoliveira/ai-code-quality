# AI Quality CI 🤖

AI-powered code quality analysis tool with support for multiple LLM providers and GitHub integration.

## Features ✨

- 🧠 **Multiple AI Providers**
  - OpenAI (GPT-4, GPT-3.5-turbo)
  - Azure OpenAI
  - Claude (claude-3-opus, claude-3-sonnet)
  - DeepSeek (deepseek-coder)

- 🔍 **Code Analysis**
  - Static analysis with Pylint
  - AI-powered improvement suggestions
  - Automatic fixes
  - Code formatting

- 🌟 **GitHub Integration**
  - Pull Request analysis
  - Automatic comments
  - Commit creation
  - Code suggestions

- 💻 **User-Friendly Interface**
  - Colored output
  - Git-style diffs
  - Interactive fix application
  - Multi-language support

## Installation 📦

```bash
pip install ai-quality-ci
```

## Configuration ⚙️

### 1. Environment Variables

Set up the required environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="your-key"

# Azure OpenAI
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"

# GitHub
export GITHUB_TOKEN="your-token"
```

### 2. Configuration File (Optional)

Create a `config.yaml` file to customize settings:

```yaml
provider:
  name: openai  # or azure, claude, deepseek
  model: gpt-4  # provider-specific model
  
analysis:
  ignore_patterns:
    - "test_*.py"
    - "setup.py"
  pylint_config: "path/to/pylintrc"

output:
  language: en  # or pt-BR, es
  human_readable: true
```

## Usage 🚀

### File Analysis

```bash
# Analyze a file
ai-quality-ci review-files file.py

# Analyze a directory
ai-quality-ci review-files src/

# Ignore specific files
ai-quality-ci review-files . --ignore "test_*.py"

# Human-readable output
ai-quality-ci review-files src/ --human-readable
```

### Pull Request Analysis

```bash
# Analyze PR
ai-quality-ci review-pr username/repo 123

# Analyze PR with specific model
ai-quality-ci review-pr username/repo 123 --provider azure --model gpt-4
```

## Options 🎛️

| Option          | Description                               | Default |
|----------------|-------------------------------------------|---------|
| --provider     | AI provider                               | openai  |
| --model        | AI model                                  | gpt-4   |
| --language     | Output language (en, pt-BR)               | en      |
| --auto-apply   | Apply fixes automatically                 | false   |
| --show-fixes   | Show suggested fix details                | false   |
| --human-readable| Use rich formatting for better readability| false   |
| --recursive    | Search files recursively                  | true    |
| --ignore       | Patterns to ignore (can use multiple)     | -       |
| --config       | Configuration file                        | -       |

## Suggested Fixes 🛠️

When using `--show-fixes`, the tool shows corrections in git-diff format:

```diff
Fix #1: Add parameter typing
--- a/file.py
+++ b/file.py
@@ -1,5 +1,5 @@
-def process_data(data):
-    result = []
+def process_data(data: List[Dict]) -> List[Dict]:
+    result: List[Dict] = []
     for item in data:
         # processing
     return result
```

For each fix you can:
1. View title and description
2. View proposed changes
3. Choose to apply or not
4. Generate commit automatically

## Display Modes 👀

1. **Standard Mode**: Plain text output
2. **Human-Readable Mode** (`--human-readable`):
   - Colors and icons
   - Rich formatting
   - Colored diffs
   - Friendly interaction

## Applying Fixes ✅

1. **Manual** (`--show-fixes`):
   - Individual choice
   - Separate commits
   - Preview changes

2. **Automatic** (`--auto-apply --show-fixes`):
   - All fixes
   - Prior confirmation
   - Automatic commits

> ⚠️ **Note**: `--auto-apply` requires `--show-fixes`

## Development 🔧

### Environment

```bash
# Clone repository
git clone https://github.com/username/ai-quality-ci
cd ai-quality-ci

# Install in development mode
pip install -e ".[dev]"
```

### Tests

```bash
# Run tests
pytest

# With coverage
pytest --cov=ai_quality_ci
```

## License 📜

MIT License - See [LICENSE](LICENSE) for details.
