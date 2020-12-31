from os import makedirs, walk
from os.path import exists, isfile, join, split, splitext
from typing import AnyStr, Iterable, Optional, Tuple


def ensure_file(file_path: str) -> bool:
    """
    Create file if it doesn't exists
    :param str file_path: full path to target file
    :return: return True if file exists or it's created otherwise False
    :raise: when creating directories fails (permission issue, unreachable target media, etc ...)
    """
    if isfile(file_path):
        return True
    dir_path, file_name = split(file_path)
    if not exists(dir_path):
        makedirs(dir_path)
    open(file_path, "a").close()  # "Touch" file

    return isfile(file_path)


def read_text_file_lines(file_path: AnyStr, unique: bool = False) -> Iterable[AnyStr]:
    """Yields text string from file line by line"""
    lines = set()
    if isfile(file_path):
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not unique:
                    yield line
                elif unique and line not in lines:
                    yield line
                    lines.add(line)
    else:
        yield from []


def list_files(
    dir_path: str, file_type: str = None, full_path=True
) -> Iterable[AnyStr]:
    """
    Lists files in a directory
    :param str dir_path: path to a directory with files
    :param str file_type: filter files by file type
    :param bool full_path: return file full path otherwise just file names
    :return: yields file paths/names
    """
    # files = []
    for (root, _, file_names) in walk(dir_path):
        for file_name in file_names:
            if file_type is not None:
                _, file_ext = splitext(file_name)
                if (
                    not file_ext.startswith(".")
                    or file_ext.lower()[1:] != file_type.lower()
                ):
                    continue
            if full_path:
                file_name = join(root, file_name)
            # files.append(file_name)
            yield file_name

    # return files


def append_lines(
    file_path: AnyStr, lines: Iterable[AnyStr], unique: bool = False
) -> Tuple[bool, Optional[AnyStr]]:
    """Appends lines to existing text file or newly created and return pair of 
     True and empty string if succeeded or False and error message if failed"""
    ok, error = True, None
    try:
        old_lines = set(read_text_file_lines(file_path, unique=True)) if unique else set()
        new_lines = []
        for line in lines:
            if unique and line in old_lines:
                continue
            new_lines.append(line)
        if len(new_lines) > 0:
            text = "\n".join(new_lines) + '\n'
            with open(file_path, "a") as f:
                f.write(text)
    except Exception as e:
        ok = False
        error = str(e)

    return ok, error


def read_text_file(file_path: AnyStr) -> Optional[AnyStr]:
    """Returns file content string from given file path on success otherwise None"""
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except:
        text = None

    return text
