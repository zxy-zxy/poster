import os

from pydrive.drive import GoogleDrive


class DriveHandler:
    def __init__(self, google_drive_service: GoogleDrive):
        self.drive_service = google_drive_service

    def load_file_from_google_drive_to_disk(
        self, file_id: str, dir_path: str, mimetype: str = None
    ):
        file = self.drive_service.CreateFile({'id': file_id})
        file_path = os.path.join(dir_path, file['title'])
        file.GetContentFile(file_path, mimetype=mimetype)
        return file_path
