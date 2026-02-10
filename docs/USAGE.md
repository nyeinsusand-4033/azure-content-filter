# Usage Guide

[← Back to README](../README.md)


This document provides detailed instructions on how to use the Azure Content Filter service.

## 1. HTTP Trigger (`filter_comment`)

The HTTP trigger allows you to filter text on-demand by sending a POST request.

### Endpoint
`POST /api/filter_comment`

### Request Format
**Headers:**
- `Content-Type`: `application/json`

**Body:**
```json
{
  "comment": "String to be filtered"
}
```

### Response Format
**Success (200 OK):**
```json
{
  "original": "Original string",
  "filtered": "Filtered string with bad words masked (****)",
  "is_safe": boolean,
  "id": "MongoDB Document ID"
}
```

**Note:** The results are now stored in your configured MongoDB instance in the `reviews` collection.

**Error (400 Bad Request):**
- If the body is invalid JSON.
- If the `comment` field is missing.

### Example (cURL)
```bash
curl -X POST http://localhost:7071/api/filter_comment \
     -H "Content-Type: application/json" \
     -d '{"comment": "This is a really bad example."}'
```

---

## 2. Cosmos DB Trigger (`cosmos_filter_trigger`) (Deprecated/Disabled)

> **Note:** This trigger is currently disabled. It is incompatible with MongoDB vCore clusters.

The Cosmos DB trigger automatically processes new documents added to the database.

### Workflow
1.  A new document is created in the `Reviews` container.
2.  The trigger fires and reads the document.
3.  The function extracts the `comment` field.
4.  The content is filtered using the shared logic.
5.  **Output**: Currently, the function **logs** the result.
    *   *Note: In a production scenario, you would typically write the filtered result back to the database or to another container.*

### Data Requirements
The document in Cosmos DB must have a `comment` field.

**Example Document:**
```json
{
  "id": "1",
  "comment": "This product is terrible!",
  "author": "User A"
}
```

### Logging
Check the function logs to see the processing result:
```
Cosmos DB trigger: Processing 1 documents.
Document 1 processed. Safe: False
```
