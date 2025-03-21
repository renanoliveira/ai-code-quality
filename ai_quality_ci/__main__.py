"""Command line interface for AI Quality CI tool."""

import os
import sys
from typing import List, Dict, Optional
import click
from rich.console import Console
from rich.prompt import Confirm
from rich import print as rprint

from .ai_reviewer import AIReviewer
from .code_analyzer import CodeAnalyzer

console = Console()

def format_review_output(result: Dict, file_path: str, show_fixes: bool = False, human_readable: bool = False):
    """Format and display review results.
    
    Args:
        result: Review results from AIReviewer
        file_path: Path to reviewed file
        show_fixes: Whether to show code fixes
        human_readable: Whether to use human-readable format
    """
    if "error" in result and result["error"]:
        rprint(f"[red]❌ Error: {result['error']}[/]")
        return
        
    rprint(f"\n[bold]{file_path}[/]")
    rprint("=" * len(file_path))
    
    if human_readable:
        if result.get("style_issues"):
            rprint("\n[bold]Style Issues:[/]")
            for issue in result["style_issues"]:
                rprint(f"• {issue}")
                
        if result.get("code_improvements"):
            rprint("\n[bold]Code Improvements:[/]")
            for improvement in result["code_improvements"]:
                rprint(f"• {improvement}")
                
        if result.get("documentation"):
            rprint("\n[bold]Documentation:[/]")
            for doc in result["documentation"]:
                rprint(f"• {doc}")
                
        if show_fixes and result.get("code_fixes"):
            rprint("\n[bold]Code Fixes:[/]")
            for title, fix_info in result["code_fixes"].items():
                rprint(f"\n[bold]{title}[/]")
                if isinstance(fix_info, dict):
                    if fix_info.get("description"):
                        rprint(fix_info["description"])
                    if fix_info.get("fix"):
                        rprint("```python")
                        rprint(fix_info["fix"])
                        rprint("```")
                        
                        if Confirm.ask("\nDeseja aplicar esta correção?"):
                            try:
                                with open(file_path, "w") as f:
                                    f.write(fix_info["fix"])
                                rprint("[green]✓ Correção aplicada com sucesso![/]")
                            except Exception as e:
                                rprint(f"[red]❌ Erro ao aplicar correção: {str(e)}[/]")
    else:
        rprint(result)

def find_python_files(directory: str) -> List[str]:
    """Find all Python files in directory recursively.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of Python file paths
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

@click.group()
def cli():
    """AI Quality CI tool for automated code review."""
    pass

@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--provider", default="azure", help="AI provider to use (openai, azure)")
@click.option("--model", default="gpt-4o", help="Model to use for AI review")
@click.option("--language", default="en", help="Language for AI responses")
@click.option("--show-fixes", is_flag=True, help="Show suggested code fixes")
@click.option("--human-readable", is_flag=True, help="Use human-readable output format")
def review_files(files: List[str], provider: str, model: str, language: str, 
                show_fixes: bool, human_readable: bool):
    """Review Python files using AI."""
    python_files = []
    
    # Collect all Python files
    for file_path in files:
        if os.path.isdir(file_path):
            python_files.extend(find_python_files(file_path))
        elif file_path.endswith(".py"):
            python_files.append(file_path)
            
    if not python_files:
        rprint("[red]❌ No Python files found to analyze[/]")
        return
        
    rprint(f"🔍 Found {len(python_files)} Python files to analyze...")
    
    # Initialize analyzers
    code_analyzer = CodeAnalyzer()
    ai_reviewer = AIReviewer(provider=provider, model=model, language=language)
    
    # Process each file
    for file_path in python_files:
        try:
            # Get static analysis results
            analysis_results = code_analyzer.analyze_file(file_path)
            
            # Get AI review
            result = ai_reviewer.review(file_path, analysis_results)
            
            # Format and display results
            format_review_output(result, os.path.relpath(file_path), show_fixes=show_fixes, human_readable=human_readable)
            
        except Exception as e:
            rprint(f"[red]❌ Error analyzing {file_path}: {str(e)}[/]")

if __name__ == "__main__":
    cli()
