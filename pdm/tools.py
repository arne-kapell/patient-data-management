import hashlib
import pathlib
from exiftool import ExifToolHelper


def getUsersDocFolder(user, base="documents/"):
    """Return the path to the user's Documents folder."""
    hashed = hashlib.sha256(user.email.encode()).hexdigest()
    return base + hashed + "/"


def extractPageNumber(file) -> int:
    """Extract the number of pages from a file name."""
    file_path = pathlib.Path(file).resolve()
    print(file_path)
    PAGE_COUNT_KEYS = ["PDF:PageCount",
                       "XML:Pages"]  # TODO: Add more keys/formats
    IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]
    if str(file_path).lower().split(".")[-1] in IMAGE_FORMATS:
        return 1
    with ExifToolHelper() as et:
        info = dict(et.get_metadata(file_path)[0])
        possible_vals = [i for i in info.items() if i[0] in PAGE_COUNT_KEYS]
        return int(possible_vals[0][1]) if len(possible_vals) > 0 else 0
