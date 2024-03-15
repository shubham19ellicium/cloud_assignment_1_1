from azure.core.exceptions import ResourceNotFoundError

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
    

