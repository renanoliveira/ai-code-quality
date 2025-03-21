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
| `--show-fixes` | Show details of suggested fixes          | false       |
| `--human-readable` | Use rich formatting for better readability | false       |
| `--recursive`  | Search files recursively                 | true        |
| `--ignore`     | Patterns to ignore (can use multiple)    | -           |
| `--config`     | Configuration file                       | -           |

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

### Directory and File Filtering Examples
```bash
# Analyze a Python file
ai-quality-ci review-files path/to/file.py

# Analyze a directory (recursively)
ai-quality-ci review-files src/

# Analyze multiple files and directories
ai-quality-ci review-files src/ tests/ file.py

# Disable recursive search
ai-quality-ci review-files src/ --no-recursive

# Ignore specific files
ai-quality-ci review-files . --ignore "test_*.py" --ignore "setup.py"

# Specify provider and model
ai-quality-ci review-files src/ --provider claude --model claude-3-opus

# Output in Portuguese with rich formatting
ai-quality-ci review-files src/ --language pt-BR --human-readable

# Show details of suggested fixes
ai-quality-ci review-files src/ --show-fixes

# Auto-apply fixes
ai-quality-ci review-files src/ --auto-apply

# Use configuration file
ai-quality-ci review-files src/ --config config.yaml
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

## CI Integration 🔄

### Tekton Pipeline Integration

AI Quality CI can be integrated into your CI/CD workflow using Tekton pipelines. The integration provides:

- Automated code review in your CI pipeline
- Secure handling of API credentials
- Configurable parameters for all features
- Support for both OpenAI and Azure OpenAI
- Automatic fix commits in your repository

### Quick Setup

1. Build the Docker image:
```bash
docker build -t your-registry/ai-quality-ci:latest .
docker push your-registry/ai-quality-ci:latest
```

2. Apply Tekton resources:
```bash
kubectl apply -f tekton/tasks/code-review-task.yaml
kubectl apply -f tekton/pipelines/code-review-pipeline.yaml
```

3. Configure secrets:
```bash
kubectl apply -f tekton/secrets/secrets.yaml
```

### Pipeline Parameters

| Parameter    | Description                    | Default |
|-------------|--------------------------------|---------|
| repo-url    | Git repository URL             | -       |
| branch-name | Git branch to analyze          | main    |
| path        | Files to analyze               | .       |
| model       | LLM model to use              | gpt-4o  |
| language    | Output language                | en      |
| auto-apply  | Auto-apply fixes              | false   |
| use-azure   | Use Azure OpenAI              | false   |

### Example Pipeline Run

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: code-review-run
spec:
  pipelineRef:
    name: ai-code-review-pipeline
  params:
    - name: repo-url
      value: "https://github.com/your-org/your-repo.git"
    - name: path
      value: "src/*.py"
    - name: auto-apply
      value: "true"
```

For detailed CI setup instructions, see [tekton/README.md](tekton/README.md).

## License 📜
MIT License - See [LICENSE](LICENSE) for details.

# AI Quality CI 🤖

Uma ferramenta de análise de código que combina análise estática com revisão de código alimentada por IA.

## Recursos ✨

- 🔍 Análise estática usando Pylint
- 🤖 Suporte a múltiplos provedores de IA:
  - OpenAI (GPT-4, GPT-3.5-turbo)
  - Claude (claude-3-opus, claude-3-sonnet)
  - DeepSeek (modelos deepseek-coder)
- 🌐 Suporte a múltiplos idiomas (en, pt-BR)
- 🔄 Integração com GitHub PRs
- 🚀 Sugestões de código detalhadas
- ⚡ Pipeline CI/CD com Tekton
- 🛠️ Auto-aplicação de correções
- ⚙️ Configuração flexível via YAML

## Instalação 📦

```bash
# Instalação básica
pip install ai-quality-ci

# Com dependências de desenvolvimento
pip install "ai-quality-ci[dev]"
```

## Configuração ⚙️

### Variáveis de Ambiente

Configure as variáveis de ambiente necessárias para os serviços que você planeja usar:

```bash
# Para OpenAI
export OPENAI_API_KEY=sua_chave_openai

# Para Azure OpenAI
export AZURE_OPENAI_KEY=sua_chave_azure
export AZURE_OPENAI_ENDPOINT=seu_endpoint_azure

# Para Claude
export ANTHROPIC_API_KEY=sua_chave_anthropic

# Para DeepSeek
export DEEPSEEK_API_KEY=sua_chave_deepseek

# Para integração com GitHub
export GITHUB_TOKEN=seu_token_github
```

### Arquivo de Configuração

Você pode personalizar o comportamento da ferramenta usando um arquivo `config.yaml`:

```yaml
# config.yaml
ai:
  provider: openai  # openai, azure, claude, ou deepseek
  model: gpt-4     # modelo específico do provedor
  language: pt-BR  # idioma da saída

analysis:
  ignore_patterns:
    - "test_*.py"
    - "setup.py"
  pylint_config: .pylintrc

github:
  auto_comment: true
  comment_threshold: medium  # low, medium, high
```

## Uso 🚀

### Análise de Arquivos Locais

```bash
# Analisar um arquivo Python
ai-quality-ci review-files caminho/para/arquivo.py

# Analisar um diretório (recursivamente)
ai-quality-ci review-files src/

# Analisar múltiplos arquivos e diretórios
ai-quality-ci review-files src/ tests/ arquivo.py

# Desativar busca recursiva
ai-quality-ci review-files src/ --no-recursive

# Ignorar arquivos específicos
ai-quality-ci review-files . --ignore "test_*.py" --ignore "setup.py"

# Especificar provedor e modelo
ai-quality-ci review-files src/ --provider claude --model claude-3-opus

# Saída em português com formatação rica
ai-quality-ci review-files src/ --language pt-BR --human-readable

# Ver detalhes das correções sugeridas
ai-quality-ci review-files src/ --show-fixes

# Auto-aplicar correções (use com cautela)
ai-quality-ci review-files src/ --auto-apply

# Usar arquivo de configuração
ai-quality-ci review-files src/ --config config.yaml
```

### Análise de Pull Requests

```bash
# Analisar um PR específico
ai-quality-ci review-pr dono/repositorio 123

# Analisar PR com opções
ai-quality-ci review-pr dono/repo 123 \
    --provider claude \
    --model claude-3-opus \
    --language pt-BR \
    --auto-apply
```

### Opções Disponíveis

| Opção           | Descrição                                   | Padrão  |
|-----------------|---------------------------------------------|---------|
| --provider      | Provedor de IA                             | openai  |
| --model         | Modelo de IA                               | gpt-4   |
| --language      | Idioma da saída (en, pt-BR)               | en      |
| --auto-apply    | Aplicar correções automaticamente          | false   |
| --show-fixes    | Mostrar detalhes das correções sugeridas  | false   |
| --human-readable| Usar formatação rica para melhor leitura   | false   |
| --recursive     | Buscar arquivos recursivamente             | true    |
| --ignore        | Padrões para ignorar (pode usar múltiplos) | -       |
| --config        | Arquivo de configuração                    | -       |

### Modelos Suportados

#### OpenAI
- gpt-4
- gpt-3.5-turbo

#### Claude
- claude-3-opus
- claude-3-sonnet

#### DeepSeek
- deepseek-coder-33b-instruct
- deepseek-coder-6.7b-instruct

## Integração CI/CD com Tekton 🔄

### Instalação

```bash
# Instalar secrets
kubectl apply -f tekton/secrets/secrets.yaml
```

### Parâmetros do Pipeline

| Parâmetro    | Descrição                     | Padrão  |
|--------------|-------------------------------|---------|
| repo-url     | URL do repositório Git        | -       |
| branch-name  | Branch para análise           | main    |
| path         | Arquivos para análise         | .       |
| provider     | Provedor de IA               | openai  |
| model        | Modelo de IA                 | gpt-4   |
| language     | Idioma da saída              | en      |
| auto-apply   | Auto-aplicar correções       | false   |

### Exemplo de Pipeline Run

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: code-review-run
spec:
  pipelineRef:
    name: ai-code-review-pipeline
  params:
    - name: repo-url
      value: "https://github.com/seu-org/seu-repo.git"
    - name: path
      value: "src/*.py"
    - name: provider
      value: "claude"
    - name: model
      value: "claude-3-opus"
    - name: language
      value: "pt-BR"
    - name: auto-apply
      value: "true"
```

Para instruções detalhadas de configuração do CI, veja [tekton/README.md](tekton/README.md).

## Desenvolvimento 🛠️

### Testes

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
pytest

# Executar testes com cobertura
pytest --cov=ai_quality_ci tests/

# Formatar código
black ai_quality_ci tests
isort ai_quality_ci tests

# Verificar tipos
mypy ai_quality_ci
```

### Estrutura do Projeto

```
ai-quality-ci/
├── ai_quality_ci/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ai_reviewer.py
│   ├── code_analyzer.py
│   ├── github_client.py
│   └── providers/
│       ├── __init__.py
│       ├── base.py
│       ├── openai.py
│       ├── claude.py
│       └── deepseek.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_ai_reviewer.py
│   ├── test_code_analyzer.py
│   ├── test_github_client.py
│   └── test_providers/
├── tekton/
│   ├── pipelines/
│   ├── tasks/
│   └── secrets/
├── README.md
├── setup.py
├── requirements.txt
└── config.yaml
```

## Licença 📜

MIT License - Veja [LICENSE](LICENSE) para detalhes.

### Correções Sugeridas

Ao usar a opção `--show-fixes`, a ferramenta mostrará as correções sugeridas em um formato git-diff amigável:

```diff
Correção #1: Adicionar tipagem de parâmetros
--- a/meu_arquivo.py
+++ b/meu_arquivo.py
@@ -1,5 +1,5 @@
-def processa_dados(dados):
-    resultado = []
+def processa_dados(dados: List[Dict]) -> List[Dict]:
+    resultado: List[Dict] = []
     for item in dados:
         # processamento
     return resultado
```

Para cada correção sugerida, você pode:
1. Ver o título e descrição da correção
2. Ver as alterações propostas em formato git-diff
3. Escolher se deseja aplicar a correção
4. Se aplicada, a correção será commitada automaticamente com uma mensagem descritiva

### Opções de Formatação

A ferramenta oferece dois modos de visualização:

1. **Modo Padrão**: Saída em texto simples
2. **Modo Human-Readable** (`--human-readable`): 
   - Cores e ícones para melhor visualização
   - Formatação rica para melhor legibilidade
   - Diff colorido para correções sugeridas
   - Confirmação interativa para aplicar correções

### Aplicação de Correções

Existem duas formas de aplicar correções:

1. **Manual** (`--show-fixes`):
   - Mostra cada correção individualmente
   - Permite escolher quais correções aplicar
   - Cria commits separados para cada correção

2. **Automática** (`--auto-apply --show-fixes`):
   - Mostra todas as correções
   - Aplica todas as correções aprovadas
   - Cria commits separados para cada correção

> ⚠️ **Nota**: A opção `--auto-apply` só funciona em conjunto com `--show-fixes`
