# Deployment Guide

[← Back to README](../README.md)


This guide explains how to deploy the Azure Content Filter to Azure and configure it correctly.

## 1. Create Azure Resources

Before deploying the code, you need to create the infrastructure.

### Option A: VS Code (Recommended)
1.  Open the **Azure** extension.
2.  Under **Resources**, click **+** -> **Create Resource...**.
3.  Select **Function App in Azure**.
4.  Follow the prompts:
    -   **Name**: Globally unique name (e.g., `my-content-filter-app`).
    -   **Runtime Stack**: Python 3.11 (or your local version).
    -   **Location**: Choose a region near you.

### Option B: Azure CLI
```bash
# Create a Resource Group
az group create --name ContentFilterRG --location eastus

# Create a Storage Account
az storage account create --name <STORAGE_NAME> --location eastus --resource-group ContentFilterRG --sku Standard_LRS

# Create the Function App
az functionapp create --resource-group ContentFilterRG --consumption-plan-location eastus --runtime python --runtime-version 3.11 --functions-version 4 --name <APP_NAME> --os-type linux --storage-account <STORAGE_NAME>
```

---

## 2. Configure Settings (CRITICAL)

Your `local.settings.json` file is **NOT** deployed to Azure for security reasons. You must manually configure the connection strings in the Azure Portal or via CLI.

### Required Settings
-   `MONGO_URI`: Connection string to your MongoDB instance (e.g., MongoDB Atlas).
-   `MONGO_DB_NAME`: Name of the database (e.g., `prod_db`).
-   `AzureWebJobsStorage`: Automatically set by Azure when creating the Function App, but verify it exists.

### How to Set Settings
**Via Azure Portal:**
1.  Go to your Function App.
2.  Select **Settings** -> **Environment variables**.
3.  Click **+ Add** (or **New App Setting**).
4.  Name: `MONGO_URI`.
5.  Value: Your actual MongoDB connection string.
6.  Click **Apply**.
7.  Repeat for `MONGO_DB_NAME`.

**Via Azure CLI:**
```bash
az functionapp config appsettings set --name <APP_NAME> --resource-group <RESOURCE_GROUP> --settings "MONGO_URI=<YOUR_URI>" "MONGO_DB_NAME=<YOUR_DB_NAME>"
```

---

## 3. Deploy the Code

### Option A: VS Code
1.  Open the **Azure** extension.
2.  Under **Workspace**, click the **Deploy to Azure...** (cloud icon).
3.  Select your subscription and the Function App you created.
4.  Click **Deploy**.

### Option B: Azure CLI (Core Tools)
Run this command in your project root:
```bash
func azure functionapp publish <APP_NAME>
```

---

## 4. Verification

After deployment, your HTTP endpoint will be public.

**Test URL:**
`https://<APP_NAME>.azurewebsites.net/api/filter_comment`

**Test with curl:**
```bash
curl -X POST https://<APP_NAME>.azurewebsites.net/api/filter_comment \
     -H "Content-Type: application/json" \
     -d '{"comment": "Testing deployment."}'
```
