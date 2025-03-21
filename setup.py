from setuptools import setup, find_packages

setup(
    name="ai-quality-ci",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=0.28.0",
        "pylint>=3.0.0",
        "click>=7.1.2",
        "pyyaml>=6.0.0",
        "PyGithub>=2.1.1",
        "rich>=13.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-mock>=3.10.0',
            'black>=23.0.0',
            'isort>=5.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'ai-quality-ci=ai_quality_ci.__main__:cli',
        ],
    },
    author="Renan Oliveira",
    author_email="renan.oliveira@example.com",
    description="AI-powered code quality analysis with multiple LLM providers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-quality-ci",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
