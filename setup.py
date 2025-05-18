from setuptools import setup, find_packages

setup(
    name="csv-validator-component",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="Declarative CSV Validator with CLI and reports",
    # long_description=open("README.md", encoding="utf-8").read(),
    # long_description_content_type="text/markdown",
    url="https://github.com/YourUsername/csv-validator-component",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "PyYAML",
        "click",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "csv-validator = csv_validator.cli:main",
        ],
    },
    python_requires=">=3.8",
)
