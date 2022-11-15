import os
import io
from io import BytesIO
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2 import service_account

def get_service(api_name, api_version, scopes, key_file_location):
    credentials = service_account.Credentials.from_service_account_file(
    key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)
    service = build(api_name, api_version, credentials=scoped_credentials)
    return service


def download(file_id):
    scope = 'https://www.googleapis.com/auth/drive.file'
    key_file_location = 'key.json'
    folder_id = ''         #UploadedImg folder
    org_file_name = ''
    try:
        # Authenticate and construct service.
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location
        )

        #List files in Dreambooth folder
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            if item["id"] == file_id:
                org_file_name = item['name']
            
        # Get file by UID
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Downloaded {int(status.progress() * 100)}%')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    #Save as sks.zip
    with open('sks.zip', 'wb') as f:
        f.write(file.getvalue())
    return org_file_name


def upload(new_ckpt):
    scope = 'https://www.googleapis.com/auth/drive.file'
    key_file_location = 'key.json'
    folder_id = ''        #Models folder
    file_name = 'model.ckpt'
    new_file = ''
    try:
        # Authenticate and construct service.
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location
        )
            
        # Upload ckpt
        file_metadata = {
            'name': new_ckpt,
            'parents': [folder_id]
        }
        media = MediaFileUpload('./{0}'.format(file_name), mimetype='text/plain', resumable=True)
        print('Uploading file: {0}...'.format(file_name))
        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Call the Drive v3 API again to see files
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')
    return new_file.get("id")


if __name__ == '__main__':
    upload()
