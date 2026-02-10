# Setup Guide

[← Back to README](../README.md)


Follow these instructions to set up your local development environment for the Azure Content Filter.

## Prerequisites

Ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **Azure Functions Core Tools**: [Install Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash%2Ckeda#install-the-azure-functions-core-tools)
3.  **Azure CLI**: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
4.  **Azurite (Azure Storage Emulator)**: Required for local execution.
    *   Install via npm: `npm install -g azurite`
    *   Or use the **Azurite** extension in VS Code.
5.  **MongoDB**: Required for data storage.
    *   **Local**: [Install MongoDB Community Edition](https://www.mongodb.com/try/download/community)
    *   **Cloud**: [MongoDB Atlas](https://www.mongodb.com/atlas/database) (Free Tier available)

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/raksit/azure-content-filter.git
    cd azure-content-filter
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Configuration

1.  Create a `local.settings.json` file in the root directory if it doesn't exist.
2.  Add the following configuration:

    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "MONGO_URI": "mongodb://localhost:27017/",
        "MONGO_DB_NAME": "content_filter_db"
      }
    }
    ```

    *   **AzureWebJobsStorage**: `UseDevelopmentStorage=true` connects to local Azurite.
    *   **MONGO_URI**: Connection string to your MongoDB instance.
    *   **MONGO_DB_NAME**: Name of the database to use.

---

## Running Locally

1.  **Start Azurite**:
    Open a new terminal and run:
    ```bash
    azurite
    ```
    *(Or us the VS Code command palette: `Azurite: Start`)*

2.  **Start the Function App**:
    In your project terminal (with `.venv` activated):
    ```bash
    func start
    ```

3.  **Verify**:
    You should see the following endpoints listed:
    *   `filter_comment`: [POST] http://localhost:7071/api/filter_comment

   See [USAGE.md](USAGE.md) for how to test the endpoints.
