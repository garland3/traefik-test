# OAuth2 Chatbot with Traefik

A modern web application that combines OAuth2 authentication with an OpenAI-powered chatbot, using Traefik as a reverse proxy.

## Architecture

The project consists of three main components:

1. **Authentication App** (FastAPI)
   - Handles OAuth2 authentication
   - Supports multiple providers (Azure AD, Auth0)
   - Manages user sessions

2. **Chatbot App** (FastAPI)
   - OpenAI-powered chatbot interface
   - Receives authenticated user information
   - Simple, modern UI

3. **Traefik Reverse Proxy**
   - Routes traffic between services
   - Handles SSL termination
   - Provides dashboard for monitoring

## Prerequisites

- Docker and Docker Compose
- VS Code (for development container)
- OAuth2 provider credentials (Azure AD or Auth0)
- OpenAI API key

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your credentials:
   ```env
   # OAuth Configuration
   OAUTH_PROVIDER=azure  # or 'auth0'
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   AUTHORITY=your_authority
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Start the services:
   ```bash
   ./run.sh
   ```

## Development

The project includes a development container setup for VS Code:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The development environment will be set up automatically

### Development URLs

- Main Application: http://localhost
- Auth App: http://localhost:5000
- Chatbot App: http://localhost:5001
- Traefik Dashboard: http://localhost:8080

## Project Structure

```
.
├── .devcontainer/          # Development container configuration
├── auth_app/              # Authentication service
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── chatbot_app/           # Chatbot service
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── Dockerfile
├── docker-compose.yml     # Production compose file
├── .env.example           # Environment template
├── run.sh                 # Startup script
└── README.md             # This file
```

## Features

- **Modern Stack**
  - Python 3.12
  - FastAPI
  - UV package manager
  - Async/await support

- **Security**
  - OAuth2 authentication
  - Secure session management
  - Environment variable protection

- **Development**
  - VS Code devcontainer
  - Hot reloading
  - Pre-configured linting
  - Type checking

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OAUTH_PROVIDER` | OAuth provider (azure/auth0) | `azure` |
| `CLIENT_ID` | OAuth client ID | `your-client-id` |
| `CLIENT_SECRET` | OAuth client secret | `your-client-secret` |
| `AUTHORITY` | OAuth authority URL | `your-tenant-id` |
| `OPENAI_API_KEY` | OpenAI API key | `your-api-key` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. # multi-container-test
