import pytest
from ai_quality_ci.code_analyzer import CodeAnalyzer

def test_code_analyzer_initialization():
    """Test CodeAnalyzer initialization"""
    analyzer = CodeAnalyzer()
    assert analyzer is not None

def test_analyze_file(sample_python_file):
    """Test analysis of a Python file"""
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(str(sample_python_file))
    
    assert "style_issues" in results
    assert "complexity" in results
    assert isinstance(results["style_issues"], list)

def test_analyze_empty_file(tmp_path):
    """Test analysis of an empty file"""
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(str(empty_file))
    
    assert results["style_issues"] == []
    assert results["complexity"] == "Low"

def test_analyze_invalid_python(tmp_path):
    """Test analysis of invalid Python code"""
    invalid_file = tmp_path / "invalid.py"
    invalid_file.write_text("def invalid_syntax(:")
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(str(invalid_file))
    
    assert "syntax error" in str(results["style_issues"]).lower()

def test_analyze_complex_code(tmp_path):
    """Test analysis of complex code"""
    complex_file = tmp_path / "complex.py"
    complex_file.write_text("""
def complex_function():
    result = 0
    for i in range(10):
        for j in range(10):
            for k in range(10):
                result += i * j * k
    return result
""")
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(str(complex_file))
    
    assert "complexity" in results
    assert results["complexity"] in ["High", "Medium"]
    assert any("complexity" in str(issue).lower() for issue in results["style_issues"])

def test_analyze_with_docstrings(tmp_path):
    """Test analysis of code with proper docstrings"""
    documented_file = tmp_path / "documented.py"
    documented_file.write_text('''
def well_documented_function(param: int) -> int:
    """This is a well documented function.
    
    Args:
        param: An integer parameter
        
    Returns:
        int: The processed result
    """
    return param * 2
''')
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_file(str(documented_file))
    
    assert not any("missing docstring" in str(issue).lower() for issue in results["style_issues"])

def test_analyze_multiple_files(tmp_path):
    """Test analysis of multiple files"""
    file1 = tmp_path / "file1.py"
    file2 = tmp_path / "file2.py"
    
    file1.write_text("def func1(): return 1")
    file2.write_text("def func2(): return 2")
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_files([str(file1), str(file2)])
    
    assert len(results) == 2
    assert all(isinstance(result, dict) for result in results.values())

def test_analyze_with_ignore_patterns():
    """Test analysis with ignored patterns"""
    analyzer = CodeAnalyzer(ignore_patterns=["test_*.py"])
    assert "test_*.py" in analyzer.ignore_patterns

def test_analyze_with_custom_pylint_config(tmp_path):
    """Test analysis with custom pylint configuration"""
    config_file = tmp_path / ".pylintrc"
    config_file.write_text("""
[FORMAT]
max-line-length=120
""")
    
    analyzer = CodeAnalyzer(pylint_config=str(config_file))
    long_line_file = tmp_path / "long_line.py"
    long_line_file.write_text("x = " + "a" * 100)
    
    results = analyzer.analyze_file(str(long_line_file))
    assert not any("line too long" in str(issue).lower() for issue in results["style_issues"])
