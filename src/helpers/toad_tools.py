import csv
import json
import os
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple, Union

import yaml


# =========================================================================== #

class FileCheckType(Enum):
    EXISTS = auto()
    NOT_FOUND = auto()

class FileType(Enum):
    JSON = "json"
    HTML = "html"
    SQL = "sql"
    XML = "xml"
    CSV = "csv"
    YAML = "yaml"
    TXT = "txt"
    MD = "md"
    INI = "ini"
    LOG = "log"
    CONF = "conf"
    PY = "py"
    JS = "js"
    CSS = "css"
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"
    PDF = "pdf"
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"

# =========================================================================== #'

def get_file_type_map() -> Dict[FileType, Tuple[str, Callable]]:
    """
    Returns a mapping of file types to read modes and read functions.

    This function returns a dictionary where the keys are FileType enums and
    the values are tuples containing the read mode ('r' or 'rb') and a callable
    read function to handle files of that type.

    Returns:
        Dict[FileType, Tuple[str, Callable]]: A dictionary mapping file types
        to read modes and read functions.
    """

    def _read_text_file(f):
        """Reads and returns the entire content of a text file."""
        return f.read()

    return {
        FileType.JSON: ('r', json.load),
        FileType.HTML: ('r', _read_text_file),
        FileType.SQL : ('r', _read_text_file),
        FileType.XML : ('r', _read_text_file),
        FileType.CSV: ('r', csv.reader),
        FileType.YAML: ('r', yaml.safe_load),
        FileType.TXT: ('r', _read_text_file),
        FileType.MD: ('r', _read_text_file),
        FileType.INI: ('r', _read_text_file),
        FileType.LOG: ('r', _read_text_file),
        FileType.CONF: ('r', _read_text_file),
        FileType.PY: ('r', _read_text_file),
        FileType.JS: ('r', _read_text_file),
        FileType.CSS: ('r', _read_text_file),
        FileType.PDF: ('rb', _read_text_file),
    }


def check_filepath(
    filepath: Path,
    check_type: FileCheckType
) -> None:
    """
    Checks the existence or absence of a file and raises appropriate errors.

    This function performs checks on a file path based on the specified check
    type. It either checks if the file exists and raises a `FileExistsError`,
    or checks if the file is not found and raises a `FileNotFoundError`.

    Args:
        filepath (Path): The full path to the file that needs to be checked.
        check_type (FileCheckType): An enum indicating the type of check to
            perform. Use `FileCheckType.EXISTS` to check if the file exists,
            and `FileCheckType.NOT_FOUND` to check if the file is not found.

    Raises:
        FileExistsError: If the check type is `FileCheckType.EXISTS` and the
            file exists.
        FileNotFoundError: If the check type is `FileCheckType.NOT_FOUND` and
            the file is not found.
    """
    folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if check_type == FileCheckType.EXISTS and filepath.is_file():
        raise FileExistsError(f"{filename} already exists in {folder}.")

    if check_type == FileCheckType.NOT_FOUND and not filepath.is_file():
        raise FileNotFoundError(f"{filename} not found in {folder}.")


def force_extension(
    filename: str,
    extension: str
) -> str:
    """
    Ensures that a filename has the specified extension.

    This function takes a filename and an extension, then returns the filename
    with the given extension. If the filename already has the correct
    extension, it is returned as-is. Otherwise, the correct extension is added.
    Extensions are case-insensitive and leading dots are optional.

    Args:
        filename (str): The name of the file, which can include an existing
            extension.
        extension (str): The desired file extension, with or without a leading
            dot.

    Returns:
        str: The filename with the specified extension.

    Raises:
        ValueError: If either the filename or extension is empty or None.
    """
    if not filename:
        raise ValueError("Filename cannot be empty or None.")

    if not extension:
        raise ValueError("Extension cannot be empty or None.")

    normalized_extension = extension.lstrip('.').lower()
    current_extension = Path(filename).suffix.lstrip('.').lower()

    if filename.endswith('.'):
        filename = filename.rstrip('.')

    if not current_extension or normalized_extension != current_extension:
        return f"{filename}.{normalized_extension}"

    return filename


def get_file(
    folder: str,
    filename: str,
    file_type: FileType,
    find_replace: Optional[Dict[str, str]] = None
) -> Union[Dict, str, bytes]:
    """
    Reads a file from a specified folder.

    This function reads a file based on its type and location. Additionally,
    it can perform find-replace operations on the file content if specified.

    Args:
        folder (str): The path to the folder containing the file.
        filename (str): The name of the file to read.
        file_type (FileType): Enum representing the file type.
        find_replace (Optional[Dict[str, str]]): A dictionary for find-replace
            operations to be performed on the file's content. Keys are the
            substrings to find, and values are the substrings to replace them
            with. Defaults to None.

    Returns:
        Union[Dict, str, bytes]: The content of the file. The type of the
            returned object depends on the file type:
            - For JSON files, a dictionary is returned.
            - For HTML and SQL files, a string is returned.
            - For other file types, bytes may be returned.

    Raises:
        ValueError: If the folder or filename is empty or None.
        FileNotFoundError: If the specified file is not found.
        ValueError: If an unsupported file type is specified.
    """
    if not folder or not filename:
        raise ValueError("Folder and filename cannot be empty or None.")

    standardized_filename = force_extension(filename, file_type.name.lower())
    filepath = Path(folder) / standardized_filename

    file_type_map = get_file_type_map()

    if file_type not in file_type_map:
        raise ValueError(f"Unsupported file type: {file_type.name}")

    read_mode, read_func = file_type_map[file_type]

    with open(filepath, read_mode) as file:
        obj = read_func(file)

    if find_replace and isinstance(obj, str):
        for key, val in find_replace.items():
            obj = obj.replace(key, str(val))

    return obj
