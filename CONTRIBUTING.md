# Contributing to KothaGPT
Thanks for your interest in contributing! This document explains the contribution process and our expectations.

## How to contribute
1. Fork the repository
2. Create a branch: `git checkout -b feat/my-feature`
3. Make your changes and test them locally
4. Commit your changes and push: `git push origin feat/my-feature`
5. Open a Pull Request describing your change

## Development Setup
- Install Python 3.9+
- Install dependencies: `pip install -r requirements.txt`
- Install dev tools: `pip install black flake8 pytest`
- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8 .`

## Coding standards
- Follow `black` for Python formatting
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation for API changes
- Run `make test` before opening a PR

## Commit messages
Use imperative subject lines, e.g. `fix: correct typo in README`.

## Pull Request Process
- Ensure all tests pass
- Update CHANGELOG.md if applicable
- Follow the PR template
- Request review from maintainers

## Code of conduct
Please follow the Contributor Covenant (link). Report issues to CODEOFCONDUCT@kothagpt.org