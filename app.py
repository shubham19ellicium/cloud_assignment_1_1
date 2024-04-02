from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from azure.storage.filedatalake import DataLakeServiceClient
import os

myapp = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

last_log_message = ""

class CustomLogHandler(logging.Handler):
    def emit(self, record):
        global last_log_message
        last_log_message = self.format(record)

handler = CustomLogHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

storage_account_name = 'salogstoragesa'
storage_account_key = os.environ.get("AZURE_DATA_LAKE_KEY")
file_system_name = 'apilog'
directory_name = 'logs'
file_name = 'app.log'

service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net/",
                                       credential=storage_account_key)

def create_file_in_adls(file_system_name, directory_name, file_name):
    try:
        path = f"{directory_name}/{file_name}"
        file_system_client = service_client.get_file_system_client(file_system_name)
        file_client = file_system_client.get_file_client(path)
        file_client.create_file()
    except Exception as e:
        logger.exception("Failed to create file in ADLS")

create_file_in_adls(file_system_name, directory_name, file_name)


def append_logs_to_adls(message):
    try:
        path = f"{directory_name}/{file_name}"
        file_client = service_client.get_file_client(file_system_name, path)
        file_size = file_client.get_file_properties().size
        file_contents = f"{message}\n"
        file_client.append_data(file_contents, offset=file_size, length=len(file_contents))
        file_client.flush_data(file_size + len(file_contents))
        
        logger.info("Data appended and flushed successfully.")
    except Exception as e:
        logger.exception("Failed to append logs")

@myapp.route("/")
def hello_world():
    logger.info(f"Home")
    append_logs_to_adls(last_log_message)
    return 'Hello World'

@myapp.route('/test', methods=['POST'])
def test():
    try:
        name = request.json["name"]
        logger.info(f"Name is : {name}")
        append_logs_to_adls(last_log_message)
        return jsonify({'result': name}), 200
    except Exception as e:
        logger.exception("An error occurred during addition")
        append_logs_to_adls(last_log_message)
        return jsonify({'error': str(e)}), 500


@myapp.route('/add', methods=['POST'])
def add():
    try:
        num1 = request.json["num_1"]
        num2 = request.json["num_2"]
        result = num1 + num2
        logger.info(f"Result : {result}")
        print("FINAL MESSAGE :: ",last_log_message)
        append_logs_to_adls(last_log_message)
        return jsonify({'result': result}), 200
    except Exception as e:
        logger.exception("An error occurred during addition")
        append_logs_to_adls(last_log_message)
        return jsonify({'error': str(e)}), 500

@myapp.route('/div', methods=['POST'])
def div():
    try:
        num1 = request.json["num_1"]
        num2 = request.json["num_2"]
        result = num1 / num2
        logger.info(f"Result : {result}")
        append_logs_to_adls(last_log_message)
        return jsonify({'result': result}), 200
    except ZeroDivisionError as e:
        logger.exception("Attempted division by zero")
        append_logs_to_adls(last_log_message)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.exception("An error occurred during division")
        append_logs_to_adls(last_log_message)
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    myapp.run(port=8000)