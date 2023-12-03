ALLOWED_EXTENSIONS = {"json"}


class FileNotAllowedError(Exception):
    """The format of file is not allowed"""

    pass


def allowedFile(filename):
    if not "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        raise FileNotAllowedError(
            "Exception occurred: You can upload only .json files!"
        )
