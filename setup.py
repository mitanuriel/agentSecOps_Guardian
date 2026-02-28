"""
Setup script for AgentSecOps Guardian package.
"""

from setuptools import setup, find_packages

# Read the version from the package
with open("agentsecops/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="agentsecops",
    version=version,
    description="AI-Powered Security Analysis Tool for detecting vulnerabilities, prompt injections, and hallucination risks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AgentSecOps Team",
    author_email="security@agentsecops.ai",
    url="https://github.com/agentsecops/guardian",
    packages=find_packages(),
    package_data={
        "agentsecops": ["py.typed"],
    },
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "secure=agentsecops.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords=[
        "security",
        "analysis",
        "ai",
        "mistral",
        "vulnerability",
        "prompt-injection",
        "hallucination",
        "cli",
    ],
)