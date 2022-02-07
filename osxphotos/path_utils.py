""" utility functions for validating/sanitizing path components """

import re

import pathvalidate

from ._constants import MAX_DIRNAME_LEN, MAX_FILENAME_LEN

__all__ = [
    "is_valid_filepath",
    "sanitize_dirname",
    "sanitize_filename",
    "sanitize_filepath",
    "sanitize_filestem_with_count",
    "sanitize_pathpart",
]


def sanitize_filepath(filepath):
    """sanitize a filepath"""
    return pathvalidate.sanitize_filepath(filepath, platform="macos")


def is_valid_filepath(filepath):
    """returns True if a filepath is valid otherwise False"""
    return pathvalidate.is_valid_filepath(filepath, platform="macos")


def sanitize_filename(filename, replacement=":"):
    """replace any illegal characters in a filename and truncate filename if needed

    Args:
        filename: str, filename to sanitze
        replacement: str, value to replace any illegal characters with; default = ":"

    Returns:
        filename with any illegal characters replaced by replacement and truncated if necessary
    """

    if filename:
        filename = filename.replace("/", replacement)
        if len(filename) > MAX_FILENAME_LEN:
            parts = filename.split(".")
            drop = len(filename) - MAX_FILENAME_LEN
            if len(parts) > 1:
                # has an extension
                ext = parts.pop(-1)
                stem = ".".join(parts)
                if drop > len(stem):
                    ext = ext[:-drop]
                else:
                    stem = stem[:-drop]
                filename = f"{stem}.{ext}"
            else:
                filename = filename[:-drop]
    return filename


def sanitize_filestem_with_count(file_stem: str, file_suffix: str) -> str:
    """Sanitize a filestem that may end in (1), (2), etc. to ensure it + file_suffix doesn't exceed MAX_FILENAME_LEN"""
    filename_len = len(file_stem) + len(file_suffix)
    if filename_len <= MAX_FILENAME_LEN:
        return file_stem

    drop = filename_len - MAX_FILENAME_LEN
    match = re.match(r"(.*)(\(\d+\))$", file_stem)
    if not match:
        # filename doesn't end in (1), (2), etc.
        # truncate filename to MAX_FILENAME_LEN
        return file_stem[:-drop]

    # filename ends in (1), (2), etc.
    file_stem = match.group(1)
    file_count = match.group(2)
    file_stem = file_stem[:-drop]
    return f"{file_stem}{file_count}"


def sanitize_dirname(dirname, replacement=":"):
    """replace any illegal characters in a directory name and truncate directory name if needed

    Args:
        dirname: str, directory name to sanitize
        replacement: str, value to replace any illegal characters with; default = ":"; if None, no replacement occurs

    Returns:
        dirname with any illegal characters replaced by replacement and truncated if necessary
    """
    if dirname:
        dirname = sanitize_pathpart(dirname, replacement=replacement)
    return dirname


def sanitize_pathpart(pathpart, replacement=":"):
    """replace any illegal characters in a path part (either directory or filename without extension) and truncate name if needed

    Args:
        pathpart: str, path part to sanitize
        replacement: str, value to replace any illegal characters with; default = ":"; if None, no replacement occurs

    Returns:
        pathpart with any illegal characters replaced by replacement and truncated if necessary
    """
    if pathpart:
        pathpart = (
            pathpart.replace("/", replacement) if replacement is not None else pathpart
        )
        if len(pathpart) > MAX_DIRNAME_LEN:
            drop = len(pathpart) - MAX_DIRNAME_LEN
            pathpart = pathpart[:-drop]
    return pathpart
