import click
from typing import List, Dict
import os
from pathlib import Path
import difflib
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Confirm
from .code_analyzer import CodeAnalyzer
from .ai_reviewer import AIReviewer
from .github_client import GitHubClient

console = Console()

def find_python_files(path: str, recursive: bool = True) -> List[str]:
    """Find Python files in a directory.
    
    Args:
        path: Path to file or directory
        recursive: Whether to search recursively in directories
        
    Returns:
        List of Python file paths
    """
    path_obj = Path(path)
    if path_obj.is_file():
        return [str(path_obj)] if path_obj.suffix == '.py' else []
    
    if not recursive:
        return [str(p) for p in path_obj.glob('*.py')]
    
    python_files = []
    for p in path_obj.rglob('*.py'):
        # Skip common directories to ignore
        parts = p.parts
        if any(x.startswith('.') or x in {'venv', 'env', '__pycache__'} for x in parts):
            continue
        python_files.append(str(p))
    
    return python_files

def generate_diff(original: str, modified: str, file_path: str) -> str:
    """Generate a git-style diff between original and modified code."""
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f'a/{file_path}',
        tofile=f'b/{file_path}',
        lineterm=''
    )
    return ''.join(diff)

def apply_fix(file_path: str, original: str, modified: str, description: str) -> bool:
    """Apply a fix to the file and create a commit."""
    try:
        # Write the modified content
        with open(file_path, 'w') as f:
            f.write(modified)
        
        # Create a commit
        os.system(f'git add "{file_path}"')
        os.system(f'git commit -m "fix: {description}"')
        return True
    except Exception as e:
        console.print(f"[red]Erro ao aplicar correção: {str(e)}[/]")
        return False

def format_review_output(result: dict, file_path: str, show_fixes: bool = False, human_readable: bool = False) -> None:
    """Format and display review output in a readable way."""
    if not human_readable:
        output = []
        # Add header
        output.append(f"\n {file_path}")
        output.append("=" * (len(file_path) + 4))
        
        # Style issues
        if result.get('style_issues'):
            output.append("\n Problemas de Estilo:")
            for issue in result['style_issues']:
                output.append(f"  • {issue}")
        
        # Code improvements
        if result.get('code_improvements'):
            output.append("\n Sugestões de Melhorias:")
            for improvement in result['code_improvements']:
                output.append(f"  • {improvement}")
        
        # Documentation
        if result.get('documentation'):
            output.append("\n Documentação:")
            for doc in result['documentation']:
                output.append(f"  • {doc}")
        
        # Code fixes
        if result.get('code_fixes'):
            if show_fixes:
                output.append("\n Correções Sugeridas:")
                for fix in result['code_fixes']:
                    output.append(f"\n  {fix['title']}")
                    if 'code' in fix:
                        # Format code block
                        code_lines = fix['code'].split('\n')
                        output.append("\n  ```python")
                        for line in code_lines:
                            output.append(f"  {line}")
                        output.append("  ```")
            else:
                num_fixes = len(result['code_fixes'])
                output.append(f"\n Correções Sugeridas: {num_fixes} correções disponíveis")
                output.append("  Use --show-fixes para ver os detalhes das correções")
        
        click.echo("\n".join(output))
        return

    # Rich formatted output
    console.print()
    console.print(Panel(f"[bold blue]{file_path}[/]", expand=False))

    # Style issues
    if result.get('style_issues'):
        console.print("\n[bold red]🔍 Problemas de Estilo[/]")
        table = Table(show_header=False, show_edge=False, box=None)
        for issue in result['style_issues']:
            table.add_row("•", f"[yellow]{issue}[/]")
        console.print(table)

    # Code improvements
    if result.get('code_improvements'):
        console.print("\n[bold green]💡 Sugestões de Melhorias[/]")
        table = Table(show_header=False, show_edge=False, box=None)
        for improvement in result['code_improvements']:
            table.add_row("•", f"[cyan]{improvement}[/]")
        console.print(table)

    # Documentation
    if result.get('documentation'):
        console.print("\n[bold magenta]📚 Documentação[/]")
        table = Table(show_header=False, show_edge=False, box=None)
        for doc in result['documentation']:
            table.add_row("•", f"[magenta]{doc}[/]")
        console.print(table)

    # Code fixes
    if result.get('code_fixes'):
        if show_fixes:
            console.print("\n[bold yellow]🛠️  Correções Sugeridas[/]")
            for i, fix in enumerate(result['code_fixes'], 1):
                # Mostrar título da correção
                console.print(Panel(
                    f"[bold yellow]Correção #{i}: {fix['title']}[/]",
                    expand=False,
                    style="yellow"
                ))
                
                if 'code' in fix:
                    # Gerar e mostrar diff
                    with open(file_path, 'r') as f:
                        original_code = f.read()
                    diff = generate_diff(original_code, fix['code'], file_path)
                    
                    console.print("\n[bold]Alterações propostas:[/]")
                    syntax = Syntax(
                        diff,
                        "diff",
                        theme="monokai",
                        line_numbers=True,
                        word_wrap=True
                    )
                    console.print(syntax)
                    
                    # Perguntar se deseja aplicar a correção
                    if Confirm.ask("\nDeseja aplicar esta correção?", console=console):
                        if apply_fix(file_path, original_code, fix['code'], fix['title']):
                            console.print("[green]✓ Correção aplicada e commitada com sucesso![/]")
                        else:
                            console.print("[red]✗ Falha ao aplicar a correção.[/]")
                    
                    console.print("\n" + "─" * 80 + "\n")
        else:
            num_fixes = len(result['code_fixes'])
            console.print(f"\n[bold yellow]🛠️  Correções Sugeridas:[/] {num_fixes} correções disponíveis")
            console.print("[dim]Use --show-fixes para ver os detalhes das correções[/]")

@click.group()
def cli():
    """AI Quality CI - Code quality analysis with AI-powered suggestions."""
    pass

@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--provider', default='openai', help='AI provider to use')
@click.option('--model', default='gpt-4', help='AI model to use')
@click.option('--language', default='en', help='Output language')
@click.option('--auto-apply', is_flag=True, default=False, help='[CUIDADO] Aplicar correções automaticamente (use com cautela)')
@click.option('--show-fixes', is_flag=True, help='Mostrar detalhes das correções sugeridas')
@click.option('--human-readable', is_flag=True, help='Usar formatação rica para melhor legibilidade')
@click.option('--config', type=click.Path(), help='Path to config file')
@click.option('--recursive/--no-recursive', default=True, help='Search recursively in directories')
@click.option('--ignore', multiple=True, help='Patterns to ignore (e.g., "test_*.py")')
def review_files(paths: List[str], provider: str, model: str, language: str, 
                auto_apply: bool, show_fixes: bool, human_readable: bool,
                config: str, recursive: bool, ignore: List[str]):
    """Review Python files or directories for code quality and suggest improvements."""
    if auto_apply and not show_fixes:
        if human_readable:
            console.print("\n[bold red]⚠️  Para usar --auto-apply, você precisa usar --show-fixes também.[/]")
        else:
            click.echo("\n Para usar --auto-apply, você precisa usar --show-fixes também.")
        return

    if auto_apply:
        if human_readable:
            console.print("\n[bold red]⚠️  ATENÇÃO:[/] Modo auto-apply ativado. As correções serão aplicadas automaticamente!")
        else:
            click.echo("\n ATENÇÃO: Modo auto-apply ativado. As correções serão aplicadas automaticamente!")
        
        if not click.confirm("Deseja continuar?"):
            if human_readable:
                console.print("[red]❌ Operação cancelada pelo usuário.[/]")
            else:
                click.echo(" Operação cancelada pelo usuário.")
            return

    analyzer = CodeAnalyzer(ignore_patterns=list(ignore))
    reviewer = AIReviewer(
        model=model,
        use_azure=(provider == 'azure'),
        language=language
    )
    
    all_files = []
    for path in paths:
        python_files = find_python_files(path, recursive=recursive)
        all_files.extend(python_files)
    
    if not all_files:
        if human_readable:
            console.print("[red]❌ Nenhum arquivo Python encontrado nos caminhos especificados.[/]")
        else:
            click.echo(" Nenhum arquivo Python encontrado nos caminhos especificados.")
        return
    
    if human_readable:
        console.print(f"[blue]🔍 Encontrados {len(all_files)} arquivos Python para análise...[/]")
    else:
        click.echo(f" Encontrados {len(all_files)} arquivos Python para análise...")
    
    for file_path in all_files:
        try:
            relative_path = os.path.relpath(file_path)
            analysis = analyzer.analyze_file(file_path)
            result = reviewer.review(file_path, analysis, auto_apply=auto_apply)
            
            # Format and display results
            format_review_output(result, relative_path, show_fixes=show_fixes, human_readable=human_readable)
            
        except Exception as e:
            if human_readable:
                console.print(f"[red]❌ Erro ao analisar {file_path}: {str(e)}[/]")
            else:
                click.echo(f" Erro ao analisar {file_path}: {str(e)}", err=True)

@cli.command()
@click.argument('repo')
@click.argument('pr_number', type=int)
@click.option('--provider', default='openai', help='AI provider to use')
@click.option('--model', default='gpt-4', help='AI model to use')
@click.option('--language', default='en', help='Output language')
@click.option('--auto-apply', is_flag=True, help='Automatically apply suggested fixes')
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub token')
def review_pr(repo: str, pr_number: int, provider: str, model: str, 
             language: str, auto_apply: bool, token: str):
    """Review a GitHub Pull Request.
    
    REPO: Repository in format 'owner/repo'
    PR_NUMBER: Pull Request number
    """
    try:
        github_client = GitHubClient(token)
        click.echo(f"\nAnalyzing PR #{pr_number} in {repo}...")
        
        results = github_client.analyze_pr(
            repo,
            pr_number,
            provider=provider,
            model=model,
            language=language,
            auto_apply=auto_apply
        )
        
        # Add review comments to PR
        github_client.comment_on_pr(repo, pr_number, results)
        
        click.echo(" Review completed and comments posted to PR!")
        
    except Exception as e:
        click.echo(f"Error reviewing PR: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
