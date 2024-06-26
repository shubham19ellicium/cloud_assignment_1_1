from flask import Flask, request,jsonify
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from logger_log import *
import traceback
from uploader import upload_data, get_service_client_token_credential,append_data_to_file,append_data
import os
from dotenv import load_dotenv
from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient
)

myapp = Flask(__name__)

load_dotenv()
# account_name = os.environ.get("ACCOUNT_NAME")
# account_name = "logfileadls"
# account_name = "southasiastorageaccount"
account_name = "salogstoragesa"
# account_key = os.environ.get("AZURE_DATA_LAKE_KEY")
account_key = os.environ.get("ACCOUNT_KEY")

container_name = 'apilogs'
blob_name = 'basic_log.log'

connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)
blob_list = container_client.list_blobs()
blob_client = container_client.get_blob_client(blob_name)


flag_store = [True if i['name'] == blob_name else False for i in blob_list]
print("FLAG ::::: ",flag_store)
if True not in flag_store:
    blob_client.upload_blob(blob_name)
    upload_data(log_info(f"CREATING NEW BLOB WITH NAME : {blob_name} ---> "),blob_client)
else:
    upload_data(log_info(f" BLOB '{blob_name}' ALREADY EXIST "),blob_client)

def check_blob_file():
    blob_list_cont = container_client.list_blobs()
    blob_flag = []
    for i in blob_list_cont:
        print("BLOB LIST ---> ",i['name'])
        if i['name'] == blob_name:
            blob_flag.append(True)

    print("BLOB NAME ---> ",blob_name)
    # blob_flag = [True if i['name'] == blob_name else False for i in blob_list_cont]
    print("FLAG ::::: ",blob_flag)
    if True not in blob_flag:
        blob_client.upload_blob(blob_name)
        upload_data(log_info(f"CREATING NEW BLOB WITH NAME : {blob_name} ---> "),blob_client)
    else:
        upload_data(log_info(f" BLOB '{blob_name}' ALREADY EXIST "),blob_client)

@myapp.route('/')
def hello_world():
    service_client = get_service_client_token_credential(account_name)
    file_system_client = service_client.get_file_system_client(container_name)
    # dir_client = file_system_client.get_directory_client(blob_name)
    # file_client = dir_client.get_file_client(blob_name).get_access_control()
    message_append = "Hello world"
    append_data(message_append,file_system_client,container_name,blob_name)

    # append_data_to_file(dir_client,blob_name)
    return 'Hello World'

@myapp.route('/add',methods=['POST'])
def add():
    try:
        check_blob_file()
        upload_data(log_info(" -------- Started addition -------- "),blob_client)
        keys_list = ['num_1',"num_2"]
        for key_to_check in keys_list:
            if key_to_check not in request.json:
                upload_data(log_error(f"The key '{key_to_check}' is not present in the JSON request."),blob_client)
                upload_data(log_info(" -------- Addition process stoped -------- "),blob_client)
                return "Incorrect input (Provide : num_1,num_2)"
            
        num_1 = request.json["num_1"]
        num_2 = request.json["num_2"]
        addition = num_1 + num_2
        upload_data(log_info(f"Number 1 :: {num_1}"),blob_client)
        upload_data(log_info(f"Number 2 :: {num_2}"),blob_client)
        upload_data(log_info(" -------- Addition completed -------- "),blob_client)
        return jsonify({"data":addition}),200
    except :
        upload_data(log_error("Something went wrong"),blob_client)
        return "Something went wrong"

@myapp.route('/div',methods=['POST'])
def div():
    try:
        check_blob_file()
        upload_data(log_info(" -------- Started division -------- "),blob_client)
        keys_list = ['num_1',"num_2"]
        for key_to_check in keys_list:
            if key_to_check not in request.json:
                upload_data(log_error(f"The key '{key_to_check}' is not present in the JSON request."),blob_client)
                upload_data(log_info(" -------- Division process stoped -------- "),blob_client)
                return "Incorrect input (Provide : num_1,num_2)"
        
        num_1 = request.json["num_1"]
        num_2 = request.json["num_2"]

        if num_2 == 0:
            print("In zero")
            raise ZeroDivisionError("Attempted to divide by zero.")
            

        division = num_1 / num_2
        upload_data(log_info(f"Number 1 :: {num_1}"),blob_client)
        upload_data(log_info(f"Number 2 :: {num_2}"),blob_client)
        upload_data(log_info(" -------- division completed -------- "),blob_client)
        return jsonify({"data":division}),200
    except ZeroDivisionError as e:
        upload_data(log_error(f"ZeroDivisionError: {str(e)}"),blob_client)
        return "Division by zero is not allowed", 400
    except Exception as e:
        print(" ----> ",traceback.format_exc())
        upload_data(log_error("Something went wrong"),blob_client)
        return "Something went wrong"



if __name__ == '__main__':
    myapp.run(port=8000)

