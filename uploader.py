from azure.core.exceptions import ResourceNotFoundError
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient
)
import traceback

from azure.identity import DefaultAzureCredential

def upload_data(message_data,blob_client):
    try:
        blob_data = blob_client.download_blob().readall().decode('utf-8')
        updated_blob_data = blob_data + message_data
    
        # Upload the updated log file
        blob_client.upload_blob(updated_blob_data, overwrite=True)
    except ResourceNotFoundError:
        blob_data = ''
    except Exception:
        print("Exception :: --- > ")    

def append_data(message_data, file_system_client:FileSystemClient , container_name, file_name):
    try:
        file_path = f"{container_name}/{file_name}"
        file_client = file_system_client.get_file_client(file_path)
        data = message_data.encode('utf-8')
        file_client.append_data(data, offset=0, length=len(data))
        file_client.flush_data(len(data))
    except ResourceNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(" ----> ",traceback.format_exc())
    
def get_service_client_token_credential(account_name) -> DataLakeServiceClient:
    account_url = f"https://{account_name}.dfs.core.windows.net"
    token_credential = DefaultAzureCredential()

    service_client = DataLakeServiceClient(account_url, credential=token_credential)

    return service_client

def create_file_system( service_client: DataLakeServiceClient, file_system_name: str) -> FileSystemClient:
    file_system_client = service_client.create_file_system(file_system=file_system_name)

    return file_system_client

def create_directory(file_system_client: FileSystemClient, directory_name: str) -> DataLakeDirectoryClient:
    directory_client = file_system_client.create_directory(directory_name)
    
    return directory_client

def append_data_to_file(directory_client: DataLakeDirectoryClient, file_name: str):
    file_client = directory_client.get_file_client(file_name)
    file_size = file_client.get_file_properties().size
    
    data = b"Data to append to end of file"
    file_client.append_data(data, offset=file_size, length=len(data))

    file_client.flush_data(file_size + len(data))