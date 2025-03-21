"""Command line interface for AI Quality CI"""

import click
from .code_analyzer import CodeAnalyzer
from .ai_reviewer import AIReviewer

@click.group()
def cli():
    """AI Quality CI CLI"""
    pass

@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--model', default='gpt-4', help='OpenAI/Azure model to use')
@click.option('--use-azure', is_flag=True, help='Use Azure OpenAI instead of OpenAI')
@click.option('--auto-apply', is_flag=True, help='Automatically apply suggested fixes and create a commit')
def review_files(files, model, use_azure, auto_apply):
    """Review Python files for code quality issues"""
    analyzer = CodeAnalyzer()
    reviewer = AIReviewer(model=model, use_azure=use_azure)
    
    for file_path in files:
        print(f"\nAnalyzing {file_path}...")
        with open(file_path, 'r') as f:
            content = f.read()
            
        analysis_results = analyzer.analyze([{
            'name': file_path,
            'content': content
        }])
        
        print("\nStyle Issues:")
        for issue in analysis_results['style_issues']:
            print(f"Line {issue['line']}: {issue['message']}")
                
        print("\nQuality Issues:")
        for issue in analysis_results['quality_issues']:
            print(f"Line {issue['line']}: {issue['message']}")
        
        print("\nGetting AI review...")
        review = reviewer.review(file_path, analysis_results, auto_apply=auto_apply)
        
        if review['style_issues']:
            print("\nAI Style Suggestions:")
            for issue in review['style_issues']:
                print(f"- {issue}")
        
        if review['code_improvements']:
            print("\nAI Code Improvements:")
            for improvement in review['code_improvements']:
                print(f"- {improvement}")
        
        if review['documentation']:
            print("\nAI Documentation Suggestions:")
            for doc in review['documentation']:
                print(f"- {doc}")
        
        if review['code_fixes'] and not auto_apply:
            print("\nAI Code Fixes Available:")
            for fix in review['code_fixes']:
                print(f"\n[{fix['title']}]")
                print(fix['code'])

if __name__ == '__main__':
    cli()
