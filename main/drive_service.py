import base64

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os


def get_drive():
    gdrive_key_b64 = os.getenv('GDRIVE_KEY')
    if gdrive_key_b64:
        gdrive_key_json = base64.b64decode(gdrive_key_b64).decode('utf-8')
        with open('/app/gdrive_key.json', 'w') as key_file:
            key_file.write(gdrive_key_json)
    
    gauth = GoogleAuth()
    
    gauth.settings['client_config_backend'] = "service"
    gauth.settings["service_config"] = {
        "client_json_file_path": "/app/gdrive_key.json"
    }
    gauth.ServiceAuth()
    
    return GoogleDrive(gauth)


def upload_file(local_path, gdrive_filename, folder_id=None):
    drive = get_drive()
    
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
        print(f'File {gdrive_filename} downloaded from Google Drive in {local_path}')
    else:
        print(f"File {gdrive_filename} dont founded in Google Drive")
