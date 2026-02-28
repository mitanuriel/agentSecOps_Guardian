# AgentOps Guardian 🛡️

**AgentOps Guardian** is a self-healing DevOps framework built for the **Mistral AI Hackathon 2026** that automatically detects and repairs LLM vulnerabilities in real-time. By integrating Mistral AI, it monitors agentic workflows for prompt injections and "hallucination crashes," autonomously pushing verified code fixes to secure the pipeline.

## Features

- 🔍 **Real-time Vulnerability Detection** - Continuously monitors LLM-powered agents for security threats
- 🛡️ **Prompt Injection Defense** - Identifies and blocks malicious prompt injection attempts
- 🔧 **Self-Healing Capabilities** - Automatically generates and applies code fixes to vulnerable components
- 🤖 **Mistral AI Integration** - Leverages Mistral AI for intelligent threat analysis and remediation
- 📊 **Hallucination Crash Prevention** - Detects and mitigates LLM output anomalies before they impact production
- ✅ **Verified Fix Deployment** - Validates and safely deploys security patches to the pipeline
- 📄 **Text Analysis & Security Reporting** - Analyzes text files for security vulnerabilities and generates comprehensive reports

## Installation

### Prerequisites

Install [uv](https://github.com/astral-sh/uv) - a fast Python package installer:

```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip:
pip install uv
```

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd agentSecOps_Guardian

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Installing the Package in development mode 

To install the `secure` CLI tool system-wide:

```bash
# Install in development mode (recommended for development)
pip install -e .
```

After installation, you can run the `secure` command from anywhere:

```bash
# Run security analysis on a file
secure ./tests/example_backend.py

# With Mistral AI analysis (requires API key)
secure ./tests/example_backend.py --mistral --mistral-key your_api_key
```

📋 Report generated: report.md

## Usage

### Running the Security Analysis CLI

After installation, you can use the `secure` command:

```bash
# Basic usage - analyze a text file and generate security report
secure input_file.txt

# With output file specification
secure input_file.txt -o security_report.md

# With text processing options
secure input_file.txt -l -s -w --lines

# With Mistral AI analysis (requires API key)
secure input_file.txt --mistral --mistral-key your_api_key

# With different analysis types
secure input_file.txt --mistral --analysis-type prompt_injection

# Advanced options
secure input_file.txt --verbose --no-patterns

# Available options:
# -l, --lowercase              Convert text to lowercase
# -s, --strip                  Strip leading/trailing whitespace
# -w, --remove-whitespace      Remove extra whitespace between words
# --lines                     Process line by line (removes empty lines)
# -o, --output                 Output report file path (default: report.md)
# --mistral                   Enable Mistral AI analysis
# --mistral-key               Mistral API key (overrides MISTRAL_API_KEY env var)
# --analysis-type             Type of Mistral analysis (prompt_injection, hallucination, etc.)
# --verbose                   Enable verbose output
# --no-patterns               Skip pattern-based security analysis
```

### Example Workflow

1. **Analyze a configuration file for security issues:**
   ```bash
   python -m agentsecops.main config.txt -o config_security_report.md
   ```

2. **Process and analyze a log file:**
   ```bash
   python -m agentsecops.main app.log --lines -s -o log_analysis.md
   ```

3. **Analyze code files for potential vulnerabilities:**
   ```bash
   python -m agentsecops.main source_code.py -o code_security_report.md
   ```

## Development

```bash
# Install development dependencies
uv pip install -r requirements-dev.txt

# Run tests
pytest

# Run specific test files
pytest tests/test_main.py
pytest tests/test_textfile_parsing.py

# Run linter
flake8 agentsecops tests

# Format code
black agentsecops tests
```

## Architecture

The current architecture focuses on text analysis and security reporting:

```
agentsecops/
├── __init__.py               # Package initialization
├── main.py                  # Main CLI orchestrator
├── cli.py                   # Original CLI (deprecated, use main.py)
├── parsing/
│   └── textfile.py          # Text file parsing utilities
├── securityinstructions/    # Security analysis module
│   └── __init__.py          # Security pattern detection
└── reporting/               # Reporting module
    └── __init__.py          # Markdown report generation

tests/
├── test_main.py             # Main workflow tests
└── test_textfile_parsing.py # Text parsing tests
```

### How It Works

1. **Text Parsing** - `agentsecops/parsing/textfile.py` reads and processes text files with various transformation options
2. **Security Analysis** - `agentsecops/securityinstructions/` analyzes content for:
   - Potential passwords and credentials
   - API keys and secrets
   - Sensitive data patterns (emails, credit cards, SSNs)
   - Common security issues (eval(), exec(), insecure protocols)
3. **Report Generation** - `agentsecops/reporting/` creates comprehensive markdown reports with findings
4. **CLI Orchestration** - `agentsecops/main.py` coordinates the entire workflow

## Security Analysis Capabilities

The system detects various security issues:

- **Passwords**: `password=`, `passwd=`, `pwd=` patterns
- **API Keys**: `api_key=`, `secret=`, `token=` patterns and long hex strings
- **Sensitive Data**: Credit card numbers, SSN patterns, email addresses
- **Security Issues**: Use of `eval()`, `exec()`, `pickle.load()`, insecure HTTP, path traversal

## Example Security Report

When you run the analysis, it generates a detailed markdown report:

```markdown
# Security Analysis Report
**Generated:** 2026-02-28 12:34:56

---
## Analysis Metadata
- **Content Length:** 1024 characters
- **Line Count:** 42 lines

---
## 🔴 Potential Passwords Found (2)
### Line 15
**Match:** `password = secret123`
**Context:** `database_password = secret123`

### Line 23
**Match:** `api_key = abc123`
**Context:** `config.api_key = abc123`

---
## 📊 Summary
- **Total Findings:** 5
- **Passwords:** 2
- **API Keys:** 1
- **Sensitive Data:** 1
- **Security Issues:** 1

⚠️  **Recommendation:** Review the findings above and address any genuine security issues.
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/security-enhancement`)
3. Commit your changes (`git commit -m 'Add security enhancement'`)
4. Push to the branch (`git push origin feature/security-enhancement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for Mistral AI Hackathon 2026**

## Mistral AI Hackathon 2026

This project was created for the **Mistral AI Hackathon 2026**, showcasing the potential of AI-driven security automation in DevOps workflows. AgentOps Guardian demonstrates how advanced language models can be leveraged to create self-healing systems that protect against emerging LLM security threats.