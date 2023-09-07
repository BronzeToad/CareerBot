import configparser
import os
import re
from typing import List, Optional, Union

# =========================================================================== #

def replace_position_dash(position: str) -> str:
    """Replace '-', '- ', ' -', or ' - ' with ','."""
    return re.sub(r'\s*-\s*', ', ', position)

def replace_position_ampersand(position: str) -> str:
    """Replace '&' with 'and'."""
    return position.replace("&", "and")

def remove_special_chars(input_str: str) -> str:
    """Remove specific special characters (other than numbers, commas, and parentheses)."""
    return re.sub('[^A-Za-z0-9,() ]+', '', input_str)


def get_folder_name(
    company: str,
    position: str,
    info: Optional[str] = None
) -> str:
    """Create a folder name from the company, position, and info."""
    _company = remove_special_chars(company.strip())

    _position = replace_position_dash(position.strip())
    _position = replace_position_ampersand(_position)
    _position = remove_special_chars(_position)

    folder_name = f"{_company} - {_position}"

    if info is not None:
        _info = remove_special_chars(info.strip())
        folder_name += f"_{_info}"

    return folder_name


def get_job_search_dir(subfolder: str = None) -> str:
    """Return the job search directory path."""
    config = configparser.ConfigParser()
    config.read('/Users/ajp/Documents/Projects/CareerBot/config/main.ini')
    job_search_root = config.get('Directories', 'JobSearchRoot')

    if subfolder is None:
        return job_search_root
    else:
        return os.path.join(job_search_root, subfolder)


def create_dir(directory_path: str) -> bool:
    """Create a directory if it doesn't already exist."""

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created.")
    else:
        print(f"Directory {directory_path} already exists.")

    return True if os.path.exists(directory_path) else False


def create_dirs(folder_namez: Union[str, List[str]]) -> None:
    """Create directories for each folder name in folder_namez."""
    names = folder_namez if isinstance(folder_namez, list) else [folder_namez]

    log_dict = {
        'success': 0,
        'failure': 0,
        'total': len(names)
    }

    job_search_dir = get_job_search_dir('TODO')

    for name in names:
        dir_path = os.path.join(job_search_dir, name)
        if create_dir(dir_path):
            log_dict['success'] += 1
        else:
            log_dict['failure'] += 1

    print("\nJob folder creation summary:")
    print(f"  Success: {log_dict['success']}")
    print(f"  Failure: {log_dict['failure']}")
    print(f"  Total: {log_dict['total']}")


def create_new_job_folders(job_recordz: Union[dict, List[dict]]) -> None:
    """Create new job folders from a list of job records."""
    records = job_recordz if isinstance(job_recordz, list) else [job_recordz]

    folder_namez = []
    for record in records:
        company = record.get('company', None)
        position = record.get('position', None)
        info = record.get('info', None)
        folder_name = get_folder_name(company, position, info)
        folder_namez.append(folder_name)

    create_dirs(folder_namez)
