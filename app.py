from datetime import datetime
import json
import psycopg2
import boto3
import hashlib
import logging
import os
import time
import sys

class SQSMessageProcessor:

    def __init__(self):

        self.queue_name = "login-queue"
        self.queue_url = f"http://localstack:4566/000000000000/{self.queue_name}"
        self.db_connection_string = "dbname=postgres user=postgres password=postgres host=postgres port=5432"

        # Logging setup
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_db_connection(self):

        attempts = 0
        max_attempts = 5
        delay = 5

        while attempts < max_attempts:

            try:
                conn = psycopg2.connect(self.db_connection_string)
                return conn
            except psycopg2.OperationalError as e:
                attempts += 1
                if attempts < max_attempts:
                    self.logger.warning(f"Connection attempt {attempts}/{max_attempts} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    self.logger.error(f"Failed to establish connection after {max_attempts} attempts. Error: {e}")
                    raise

        return None

    def mask_field(self, value):
        return hashlib.sha256(value.encode()).hexdigest()

    def insert_data(self, cursor, data):

        try:
            insert_query = """
                            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                            VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, %(app_version)s, %(create_date)s)
            """
            cursor.execute(insert_query, data)
            self.logger.info("Data inserted successfully.")

        except Exception as e:
            self.logger.error(f"Error inserting data: {str(e)}")
            self.log_error(str(e), data)

    def process_message(self, cursor, message):

        try:
            data = json.loads(message["Body"])
            data["masked_ip"] = self.mask_field(data["ip"])
            data["masked_device_id"] = self.mask_field(data["device_id"])
            flattened_data = {
                "user_id": data["user_id"],
                "device_type": data["device_type"],
                "masked_ip": data["masked_ip"],
                "masked_device_id": data["masked_device_id"],
                "locale": data["locale"],
                "app_version": data["app_version"],
                "create_date": datetime.now()
            }

            self.insert_data(cursor, flattened_data)

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            self.log_error(str(e), message)

    def log_error(self, error_message, message):
        self.logger.error(f"Error: {error_message}. Message: {message}")
        self.logger.info("Error message logged successfully.")

    def main(self):

        sqs = boto3.client('sqs', 
                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'dummy_access_key'),
                           aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy_secret_key'),
                           aws_session_token=os.getenv('AWS_SESSION_TOKEN', 'dummy_session_token'),
                           endpoint_url='http://localstack:4566', 
                           region_name='us-east-1')

        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Alter the table as there are some different version data formats
        alter_query = """
        ALTER TABLE public.user_logins ALTER COLUMN app_version TYPE VARCHAR(100)
        """
        cursor.execute(alter_query)

        queue_available = False

        while not queue_available:
            
            try:
                sqs.create_queue(QueueName=self.queue_name)
                queue_available = True
                self.logger.info("Queue created or already exists.")
            except sqs.exceptions.QueueDoesNotExist:
                self.logger.info("Waiting for the queue to be available...")
                time.sleep(5)

        self.logger.info("Queue is now available.")

        while True:
            response = sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=20)
            messages = response.get('Messages', [])

            if not messages:
                self.logger.info("No messages to process. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking the queue again
                continue

            for message in messages:
                self.process_message(cursor, message)
                sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])
                self.logger.info("Message deleted successfully.")

            conn.commit()

        cursor.close()
        conn.close()

if __name__ == "__main__":
    processor = SQSMessageProcessor()
    processor.main()
