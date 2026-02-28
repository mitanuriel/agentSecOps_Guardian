# Contributing to agentSecOps_Guardian

Thank you for your interest in contributing!

## Development Setup

1. Fork and clone the repository
2. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   uv pip install -r requirements-dev.txt
   ```

## Coding Standards

- Follow PEP 8 style guide
- Use Black for code formatting
- Write tests for new features
- Update documentation as needed

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes
3. Run tests: `pytest`
4. Run linters: `flake8 src tests` and `black src tests`
5. Commit with clear messages
6. Push to your fork and submit a PR

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.
