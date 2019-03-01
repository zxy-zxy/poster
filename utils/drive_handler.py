import os

from pydrive.drive import GoogleDrive


def load_file_from_google_drive_to_disk(
    google_drive_service: GoogleDrive, file_id: str, dir_path: str, mimetype: str = None
):
    file = google_drive_service.CreateFile({'id': file_id})
    file_path = os.path.join(dir_path, file['title'])
    file.GetContentFile(file_path, mimetype=mimetype)
    return file_path
