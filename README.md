# Azure Content Filter

A serverless content filtering microservice built with Azure Functions (Python v2 model).

## Features

-   **HTTP Trigger**: `filter_comment` endpoint.
-   **Content Filtering**: Detects and masks bad words (e.g., "bad", "terrible", "worst").
-   **JSON Output**: Returns original text, filtered text, and safety status.

## Getting Started

> **[👉 Go to Setup Guide (docs/SETUP.md)](docs/SETUP.md)** for detailed installation and configuration instructions.

1.  **Install Prerequisites**: Python, Azure Functions Core Tools, Azurite.
2.  **Configure**: Set up `local.settings.json`.
3.  **Run**: Start Azurite and the Function App.

## Deployment

> **[👉 Go to Deployment Guide (docs/DEPLOYMENT.md)](docs/DEPLOYMENT.md)** for instructions on deploying to Azure and configuring production settings.

## Triggers

This function app supports two triggers:
1.  **HTTP Trigger**: Invoke directly via HTTP POST.
2.  **Cosmos DB Trigger**: Automatically invoked when a document is created/updated in the `Reviews` container.

See **[docs/USAGE.md](docs/USAGE.md)** for API documentation and examples.



1.  **Login to Azure:**

    ```bash
    az login
    ```

2.  **Deploy using Azure Functions Core Tools:**

    ```bash
    func azure functionapp publish <APP_NAME>
    ```

    *Alternatively, use the VS Code Azure Functions extension for easier deployment.*
