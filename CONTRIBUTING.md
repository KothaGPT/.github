# Contributing to KothaGPT

Thanks for your interest in contributing! This document explains how to contribute, where to ask for help, and what our expectations are.

## Table of contents
- Where to start
- How to file a good issue
- Pull request process
- Code style & tests
- Branching and release
- Communication channels

## Where to start
1. Look through open issues and discussions. Good first issues are labeled `good-first-issue`.
2. Read this CONTRIBUTING guide and the project README for the specific repo you're contributing to.
3. If you'd like to propose a large change, open a discussion first to get feedback.

## How to file a good issue
- Use the appropriate issue template.
- Provide a clear title and description.
- Include steps to reproduce (for bugs), expected vs actual behavior, and logs or screenshots when relevant.
- Add the appropriate labels (bug, enhancement, question).

## Pull request process
- Fork the repository and create a branch named `fix/<short-description>` or `feat/<short-description>`.
- Rebase or merge the latest main before creating a PR.
- Use **Conventional Commits** for commit messages (e.g. `feat: add tokenizer for bangla` or `fix: handle unicode normalization`).
- Include tests when applicable and ensure existing tests pass.
- Keep PRs small and focused. For large changes, open a design/discussion issue first.
- Fill the PR template when opening a PR. Assign reviewers if you know who should review.

## Code style & tests
- Python repos: follow PEP8; run `black` and `ruff` before committing.
- JavaScript/TypeScript repos: follow ESLint rules and use `prettier`.
- Include unit tests for new features; PRs should not reduce coverage without discussion.
- CI must pass for merging. Do not merge failing CI.

## Branching & Releases
- `main` is always deployable.
- Use `develop` or short-lived feature branches if desired by the repo policies.
- Releases follow semantic versioning: `MAJOR.MINOR.PATCH`.

## Communication
- Use GitHub issues & discussions for asynchronous work.
- For real-time chat, use the community Slack/Discord (link in README).

## Code of Conduct
By participating you agree to abide by the Code of Conduct.
