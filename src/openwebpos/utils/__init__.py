from secrets import token_urlsafe


def get_file_extension(filename: str) -> str:
    """
    Get the file extension.
    filename: str, name of the file.
    return: str, file extension.
    """
    from os import path
    return path.splitext(filename)[1][1:]


def allowed_file(filename: str) -> bool:
    """
    Check if the file is allowed.
    filename: str, name of the file.
    return: bool, True if the file is allowed.
    """
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def delete_file(file_path: str, file_name: str):
    """
    Delete a file if it exists.
    file_path: str, path to the file.
    file_name: str, name of the file.
    """
    try:
        from os import path
        from os import remove
        remove(path.join(file_path, file_name))
    except FileNotFoundError:
        pass


def gen_urlsafe_token(length: int) -> str:
    """
    Generate a URL-safe, Base64-encoded securely generated random string.
    length: int, length of the string to generate.
    return: str, URL-safe, Base64-encoded securely generated random string.
    """
    return token_urlsafe(length)


def create_folder(folder_path: str, folder_name: str):
    """
    Create a folder if it doesn't exist.
    folder_path: str, path to the folder.
    folder_name: str, name of the folder.
    """
    try:
        from os import path
        from os import mkdir
        mkdir(path.join(folder_path, folder_name))
    except FileExistsError:
        pass


def create_file(file_path: str, file_name: str, file_mode: str = "x", file_content: str = ''):
    """
    Create a file if it doesn't exist.
    file_path: str, path to the file.
    file_name: str, name of the file.
    file_mode: str, file mode to open the file.
    """
    try:
        from os import path
        with open(path.join(file_path, file_name), file_mode) as f:
            f.write(file_content)
    except FileExistsError:
        pass
