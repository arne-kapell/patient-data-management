import hashlib
import os
import pathlib
from exiftool import ExifToolHelper
import werkzeug
from encrypted_files.base import EncryptedFile


def getUsersDocFolder(user, base="documents/"):
    """Return the path to the user's Documents folder."""
    hashed = hashlib.sha256(user.email.encode()).hexdigest()
    return base + hashed + "/"


def extractPageNumber(file) -> int:
    """Extract the number of pages from a file name."""
    file_path = pathlib.Path(file).resolve()
    PAGE_COUNT_KEYS = ["PDF:PageCount",
                       "XML:Pages"]  # TODO: Add more keys/formats
    IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]
    if str(file_path).lower().split(".")[-1] in IMAGE_FORMATS:
        return 1
    with ExifToolHelper() as et:
        info = dict(et.get_metadata(file_path)[0])
        possible_vals = [i for i in info.items() if i[0] in PAGE_COUNT_KEYS]
        return int(possible_vals[0][1]) if len(possible_vals) > 0 else 0


def getPageNumberFromEncryptedFile(file) -> int:
    try:
        file_extension = file.name.split(".")[-1]
        tmp_path = "documents/tmp/"
        tmp = f"{tmp_path}exif.{file_extension}"
        tmp = werkzeug.utils.secure_filename(tmp)
        os.makedirs(tmp_path, exist_ok=True)
        with open(tmp, "wb") as f:
            efile = EncryptedFile(file).read()
            f.write(efile)
        pages = extractPageNumber(tmp)
        os.unlink(tmp)
        os.rmdir(tmp_path)
        return pages
    except Exception as e:
        print(e)
        return -1
