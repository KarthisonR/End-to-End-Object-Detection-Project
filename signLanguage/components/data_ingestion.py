import os
import sys
import urllib
import zipfile
import gdown
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import DataIngestionConfig
from signLanguage.entity.artifacts_entity import DataIngestionArtifact
from urllib.parse import urlparse, parse_qs
import requests




class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise SignException(e, sys)
       
    # def extract_file_id(drive_url):
    # # Example Google Drive link: https://drive.google.com/file/d/FILE_ID/view
    #     parsed_url = urlparse(drive_url)
    #     file_id = parse_qs(parsed_url.query).get('id', [None])[0]
    #     if not file_id:
    #         # Extract file ID from path if available
    #         path_parts = parsed_url.path.split('/')
    #         if 'd' in path_parts:
    #             file_id = path_parts[path_parts.index('d') + 1]
    #     return file_id

    
    # def download_from_google_drive(drive_url, destination_path):
    #     file_id = extract_file_id(drive_url)
    #     if not file_id:
    #         raise ValueError("Could not extract file ID from the provided Google Drive URL.")
        
    #     download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
    #     # Using requests to handle potential redirections and cookies
    #     response = requests.get(download_url, stream=True)
    #     response.raise_for_status()  # Check for HTTP errors
        
    #     with open(destination_path, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=8192):
    #             if chunk:
    #                 f.write(chunk)
        
    #     logging.info(f"Downloaded data from {drive_url} into file {destination_path}")
    #     return destination_path
        
    

    def download_data(self)-> str:
        '''
        Fetch data from the url
        '''

        try:
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)  # Adjust if necessary
            # zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            # Extract file ID from URL
            # parsed_url = urlparse(dataset_url)
            # file_id = parse_qs(parsed_url.query).get('id', [None])[0]
            # # file_id = parsed_url.path.split('/')[3]
            # if not file_id:
            #     # Extract file ID from path if available
            #     path_parts = parsed_url.path.split('/')
            #     if 'd' in path_parts:
            #         file_id = path_parts[path_parts.index('d') + 1]

            # if not file_id:
            #     raise ValueError("Could not extract file ID from the provided Google Drive URL.")
            
            # download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # # Using requests to handle potential redirections and cookies
            # response = requests.get(download_url, stream=True)
            # response.raise_for_status()  # Check for HTTP errors
            # # logging.info(f"Response Content-Type: {response.headers.get('Content-Type')}")
            # # if "html" in response.headers.get("Content-Type", ""):
            # #     logging.error("Download failed. The link may not be accessible or requires confirmation.")
            # #     return None
            # data_file_name = "data.zip"  # You can customize this as needed
            file_id = '1MPmAMUPhgoRXrMqSdYETRmAKKxLmoEr_'
            data_file_name = 'downloaded_file.zip'  # The output filename for the downloaded file
            if not os.path.exists(zip_download_dir):
                os.makedirs(zip_download_dir)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            gdown.download(f'https://drive.google.com/uc?id={file_id}', zip_file_path, quiet=False)
            
            
            # with open(zip_file_path, 'wb') as f:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         if chunk:
            #             f.write(chunk)
            
            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            return zip_file_path

        except Exception as e:
            error_message = f"An error occurred while downloading data: {e}"
            error_detail = sys.exc_info()  # Pass the original exception details
            raise SignException(error_message, error_detail)
        

    

    def extract_zip_file(self,zip_file_path: str)-> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")

            return feature_store_path

        except Exception as e:
            raise SignException(e, sys)
        


    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise SignException(e, sys)
