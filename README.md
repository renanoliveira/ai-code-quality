# AI Quality CI 🤖

Ferramenta de análise de qualidade de código alimentada por IA, com suporte a múltiplos provedores de LLM e integração com GitHub.

## Características ✨

- 🧠 **Múltiplos Provedores de IA**
  - OpenAI (GPT-4, GPT-3.5-turbo)
  - Azure OpenAI
  - Claude (claude-3-opus, claude-3-sonnet)
  - DeepSeek (deepseek-coder)

- 🔍 **Análise de Código**
  - Análise estática com Pylint
  - Sugestões de melhoria por IA
  - Correções automáticas
  - Formatação de código

- 🌟 **Integração GitHub**
  - Análise de Pull Requests
  - Comentários automáticos
  - Criação de commits
  - Sugestões de código

- 💻 **Interface Amigável**
  - Saída formatada com cores
  - Diff no estilo git
  - Aplicação interativa de correções
  - Suporte a múltiplos idiomas

## Instalação 📦

```bash
pip install ai-quality-ci
```

## Configuração ⚙️

### 1. Variáveis de Ambiente

Configure as variáveis de ambiente necessárias:

```bash
# OpenAI
export OPENAI_API_KEY="sua-chave"

# Azure OpenAI
export AZURE_OPENAI_KEY="sua-chave"
export AZURE_OPENAI_ENDPOINT="seu-endpoint"

# GitHub
export GITHUB_TOKEN="seu-token"
```

### 2. Arquivo de Configuração (Opcional)

Crie um arquivo `config.yaml` para personalizar as configurações:

```yaml
provider:
  name: openai  # ou azure, claude, deepseek
  model: gpt-4  # modelo específico do provedor
  
analysis:
  ignore_patterns:
    - "test_*.py"
    - "setup.py"
  pylint_config: "path/to/pylintrc"

output:
  language: pt-BR  # ou en, es
  human_readable: true
```

## Uso 🚀

### Análise de Arquivos

```bash
# Analisar um arquivo
ai-quality-ci review-files arquivo.py

# Analisar um diretório
ai-quality-ci review-files src/

# Ignorar arquivos específicos
ai-quality-ci review-files . --ignore "test_*.py"

# Saída formatada em português
ai-quality-ci review-files src/ --language pt-BR --human-readable
```

### Análise de Pull Requests

```bash
# Analisar PR
ai-quality-ci review-pr usuario/repo 123

# Analisar PR com modelo específico
ai-quality-ci review-pr usuario/repo 123 --provider azure --model gpt-4
```

## Opções 🎛️

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

## Correções Sugeridas 🛠️

Ao usar `--show-fixes`, a ferramenta mostra as correções em formato git-diff:

```diff
Correção #1: Adicionar tipagem de parâmetros
--- a/arquivo.py
+++ b/arquivo.py
@@ -1,5 +1,5 @@
-def processa_dados(dados):
-    resultado = []
+def processa_dados(dados: List[Dict]) -> List[Dict]:
+    resultado: List[Dict] = []
     for item in dados:
         # processamento
     return resultado
```

Para cada correção você pode:
1. Ver o título e descrição
2. Ver as alterações propostas
3. Escolher aplicar ou não
4. Gerar commit automaticamente

## Modos de Visualização 👀

1. **Modo Padrão**: Saída em texto simples
2. **Modo Human-Readable** (`--human-readable`):
   - Cores e ícones
   - Formatação rica
   - Diff colorido
   - Interação amigável

## Aplicação de Correções ✅

1. **Manual** (`--show-fixes`):
   - Escolha individual
   - Commits separados
   - Visualização prévia

2. **Automática** (`--auto-apply --show-fixes`):
   - Todas as correções
   - Confirmação prévia
   - Commits automáticos

> ⚠️ **Nota**: `--auto-apply` requer `--show-fixes`

## Desenvolvimento 🔧

### Ambiente

```bash
# Clone o repositório
git clone https://github.com/usuario/ai-quality-ci
cd ai-quality-ci

# Instale em modo desenvolvimento
pip install -e ".[dev]"
```

### Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=ai_quality_ci
```

## Licença 📜

MIT License - Veja [LICENSE](LICENSE) para detalhes.
