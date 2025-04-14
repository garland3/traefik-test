#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your credentials"
    exit 1
fi

# Check for required environment variables
required_vars=("OAUTH_PROVIDER" "CLIENT_ID" "CLIENT_SECRET" "AUTHORITY" "OPENAI_API_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if ! grep -q "^$var=" .env; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "Error: Missing required environment variables in .env file:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    exit 1
fi

# Validate OAuth provider
OAUTH_PROVIDER=$(grep "^OAUTH_PROVIDER=" .env | cut -d'=' -f2)
if [[ "$OAUTH_PROVIDER" != "azure" && "$OAUTH_PROVIDER" != "auth0" ]]; then
    echo "Error: OAUTH_PROVIDER must be either 'azure' or 'auth0'"
    exit 1
fi

# Run docker-compose
echo "Starting the application stack..."
docker-compose up --build 