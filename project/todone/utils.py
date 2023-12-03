import datetime

ALLOWED_EXTENSIONS = {"json"}


class FileNotAllowedError(Exception):
    """The format of file is not allowed"""

    pass

# check  the format of file allowed?
def allowedFile(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Getting time
def now():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
