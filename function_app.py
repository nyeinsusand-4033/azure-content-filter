import azure.functions as func
import logging
import json
import re
import os
import pymongo
from bson import ObjectId
import urllib.parse
import datetime
import settings

app = func.FunctionApp()

def filter_text(text: str) -> dict:
    """
    Shared helper function to filter bad words from text.
    """
    bad_words = ["bad", "terrible", "worst"]
    filtered_text = text
    is_safe = True

    for word in bad_words:
        if word.lower() in filtered_text.lower():
            is_safe = False
            # Simple case-insensitive replacement (imperfect but functional for this demo)
            # A more robust regex solution could be used for better matching
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered_text = pattern.sub("****", filtered_text)
    
    return {
        "original": text,
        "filtered": filtered_text,
        "is_safe": is_safe
    }

@app.route(route="filter_comment", auth_level=func.AuthLevel.ANONYMOUS)
def filter_comment(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: Processing request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    comment = req_body.get('comment')
    if not comment:
        return func.HttpResponse(
            "Please pass a comment in the request body",
            status_code=400
        )

    result = filter_text(comment)

    # Save to MongoDB
    if settings.client and settings.MONGO_DB_NAME:
        try:
            db = settings.client[settings.MONGO_DB_NAME]
            collection = db["reviews"] # Using 'reviews' collection
            
            # Prepare document
            doc = {
                "original": result["original"],
                "filtered": result["filtered"],
                "is_safe": result["is_safe"],
                "processed_at": datetime.datetime.utcnow().isoformat()
            }
            
            insert_result = collection.insert_one(doc)
            logging.info(f"Document inserted into MongoDB with ID: {insert_result.inserted_id}")
            
            # Add ID to response for reference
            result["id"] = str(insert_result.inserted_id)

        except Exception as e:
            logging.error(f"Error inserting into MongoDB: {e}")
            # We don't fail the request if DB save fails, but we log it.
    
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=200
    )

# Option 2: Cosmos DB Trigger
# This generic trigger will fire whenever a new document is added to the 'Reviews' container.
# Make sure to update 'CosmosDbConnectionString', 'database_name', and 'container_name' with your actual values.
# @app.cosmos_db_trigger(arg_name="documents", 
#                        container_name="Reviews",
#                        database_name="ContentDB", 
#                        connection="CosmosDbConnectionString",
#                        lease_container_name="leases",
#                        create_lease_container_if_not_exists=True)
# def cosmos_filter_trigger(documents: func.DocumentList) -> None:
    logging.info('Cosmos DB trigger: Processing %s documents.', len(documents))

    for doc in documents:
        comment = doc.get('comment')
        doc_id = doc.get('id')
        
        # Prevent infinite loops: check if already processed
        if doc.get('is_processed'):
           continue

        if comment:
            result = filter_text(comment)
            logging.info(f"Document {doc_id} processed. Safe: {result['is_safe']}")
            
            # NOTE: To update the document, you would typically use an Output Binding 
            # or the Cosmos DB SDK here to write back the 'filtered' text and set 'is_processed' to True.
            # For this example, we just log the action to demonstrate the trigger.
