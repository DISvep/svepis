from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import base64
import json
import os


def get_drive():
    gdrive_key_b64 = os.getenv('GDRIVE_KEY')

    if not gdrive_key_b64:
        raise ValueError("GDRIVE_KEY environment variable is missing!")

    gdrive_key_json = base64.b64decode(gdrive_key_b64).decode('utf-8')
    with open('/app/gdrive_key.json', 'w') as key_file:
        key_file.write(gdrive_key_json)

    key_data = json.loads(gdrive_key_json)

    gauth = GoogleAuth()
    gauth.settings['client_config_backend'] = "service"
    gauth.settings["service_config"] = {
        "client_json_file_path": "/app/gdrive_key.json",
        'client_user_email': key_data['client_email'],
    }
    gauth.ServiceAuth()

    return GoogleDrive(gauth)


def upload_file(local_path, gdrive_filename, folder_id=None):
    drive = get_drive()
    
    # query = f"title='{gdrive_filename}'"
    # if folder_id:
    #     query += f" and '{folder_id}' in parents"
    # 
    # existing_files = drive.ListFile({'q': query}).GetList()
    # if existing_files:
    #     file = existing_files[0]
    #     
    #     file.SetContentFile(local_path)
    #     file.Upload()
    #     
    #     print(f'File {local_path} UPDATED on Google Drive as {gdrive_filename}')
    
    file_metadata = {'title': gdrive_filename}
    if folder_id:
        file_metadata['parents'] = [{'id': folder_id}]

    file = drive.CreateFile(file_metadata)
    file.SetContentFile(local_path)
    file.Upload()
    print(f"File {local_path} was uploaded to Google Drive as {gdrive_filename}")

    return file['id']


def download_file(gdrive_filename, local_path, folder_id=None):
    drive = get_drive()
    
    query = f"title='{gdrive_filename}'"
    if folder_id:
        query += f" and '{folder_id}' in parents"

    file_list = drive.ListFile({'q': query}).GetList()

    if file_list:
        file = file_list[0]
        file.GetContentFile(local_path)
        print(f'File {gdrive_filename} downloaded from Google Drive to {local_path}')
    else:
        print(f"File {gdrive_filename} not found on Google Drive")


def delete_file(file_id):
    drive = get_drive()
    
    file = drive.CreateFile({'id': file_id})
    file.Delete()
    
    print(f"File with id {file_id} was deleted from Google Drive")
