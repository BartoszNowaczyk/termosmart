from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

app = FastAPI()

# 🔓 Dodanie CORS, aby frontend mógł pobierać dane z innej domeny
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz tu wpisać konkretną domenę frontendową, np. "https://twojfrontend.azurestaticapps.net"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Blob Storage
connection_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER")
container_client = ContainerClient.from_connection_string(connection_str, container_name)

@app.get("/api/data")
def get_data():
    results = []
    blobs = container_client.list_blobs()

    for blob in blobs:
        if blob.name.endswith(".json"):
            blob_client = container_client.get_blob_client(blob)
            blob_data = blob_client.download_blob().readall()

            try:
                for line in blob_data.splitlines():
                    record = json.loads(line)
                    body_encoded = record.get("Body")
                    if body_encoded:
                        decoded = base64.b64decode(body_encoded).decode("utf-8")
                        parsed = eval(decoded)  # Uważaj: eval może być niebezpieczny. Lepsze byłoby json.loads(decoded)
                        results.append({
                            "timestamp": record.get("EnqueuedTimeUtc"),
                            "device": record["SystemProperties"].get("connectionDeviceId"),
                            **parsed
                        })
            except Exception as e:
                print(f"Błąd przy pliku {blob.name}: {e}")

    return results
