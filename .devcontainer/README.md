# Development Container Setup

This directory contains the configuration for the development container used in this project.

## Features

- Python 3.9 development environment
- VS Code extensions for Python development
- Pre-configured linting and formatting
- Development versions of the auth and chatbot apps
- Traefik reverse proxy for local development

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

2. Update the following environment variables in `.env`:
   - `CLIENT_ID`: Your OAuth provider client ID
   - `CLIENT_SECRET`: Your OAuth provider client secret
   - `AUTHORITY`: Your OAuth provider authority URL
   - `OPENAI_API_KEY`: Your OpenAI API key

3. Open the project in VS Code

4. When prompted, click "Reopen in Container"

## Development Workflow

- The auth app runs on port 5000
- The chatbot app runs on port 5001
- Traefik dashboard is available on port 8080
- The main application is accessible on port 80

## VS Code Extensions

The following extensions are automatically installed:
- Python
- Pylance
- Docker
- YAML

## Python Tools

The following Python tools are pre-installed:
- black (code formatting)
- pylint (linting)
- mypy (type checking)
- pytest (testing) 