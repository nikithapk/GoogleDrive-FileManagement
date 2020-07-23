from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import errors

from Oauth import APIAuth
from constants import APIConstants


def uploadFile(drive_service):
    file_metadata = {'name': APIConstants.FILE_NAME, 'parents': APIConstants.PARENT_ID}
    media = MediaFileUpload(APIConstants.DB_PATH, mimetype='application/x-kdbx')
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    return file.get('id')


def deletePrevious(drive_service, file_id):
    try:
        drive_service.files().delete(fileId=file_id).execute()
    except errors.HttpError:
        print('An error occurred: %s' % errors.HttpError)


def getFileID(drive_service):
    results = drive_service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    print(items)


def main():
    creds = APIAuth.Auth(APIConstants.SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    getFileID(drive_service)
    f = open('../Config/FileID.csv', 'r')
    DeleteFileID = (str(f.readlines())).replace("'", "").replace("[", "").replace("]", "")
    print(DeleteFileID)
    f.close()

    deletePrevious(drive_service, DeleteFileID)

    fw = open('../Config/FileID.csv', 'w')
    fw.write(str(uploadFile(drive_service)))
    fw.close()


if __name__ == '__main__':
    main()
