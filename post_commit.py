#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Waypoint 7"""

from os import (path, open, close, write, O_RDWR, O_CREAT,
                fdopen, listdir, walk, getcwd, remove)
import sys

"""
#######################################################################
# all function with different docstring style are wrote by me in lgit #
#######################################################################
"""


def __get_full_path(file):
    """
    get_full_path(file) -> return full path of file.
    This function figures out exactly the path of file on system.
    Required argument:
        file    --  a string-type file name.
    """
    if file[0] == '~':
        file = path.expanduser(file)
    else:
        file = path.realpath(file)
    return file


def __get_file_type(file):
    """
    get_file_type(file) -> return type of file.
    This function check if a file is a directory, file and return its type via
    a string. If the file is not exist, return None.
    Required argument:
        file    -- a string-type file name.
    """
    try:
        file = __get_full_path(file)
        if path.isfile(file):
            return "file"
        if path.isdir(file):
            return "directory"
        return 0
    except (FileNotFoundError, PermissionError):
        return None


def __open_file(file):
    """
    open_file(file) ->  open a file for reading and writing.
    This function returns a file object.
    Required argument:
        file    --  file' name.
    """
    try:
        file = __get_full_path(file)
        file = open(file, O_RDWR)
        file = fdopen(file)
        return file
    except PermissionError:
        return None



def __read_file(file):
    """
    read_file(file)     ->  get content of a file.
    Required argument:
        file    --  name or path of file.
    """
    try:
        file = __open_file(file)
        content = file.read()
        file.close()
        return content
    except (UnicodeDecodeError, PermissionError, AttributeError) as errors:
        del errors
        return ""



def __list_files(directoy):
    """
    list_dir(dir)   ->  return all files in a directory.
    Required argument:
        directoy     -- name of directory.
    """
    try:
        return listdir(__get_full_path(directoy))
    except (NotADirectoryError, FileNotFoundError) as error:
        del error
        return []


def __find_repo():
    """
    find_repo() -> find lgit repository.
    """

    def check_path(track, repo):
        """
        check_path(folder, track) ->  check the current directory.
        This function check if there is a lgit repository in the path.
        Required argument:
            track   --  current directory pathspec.
            repo    --  folder contain .lgit.
        """
        if ".git" in __list_files(track):
            repo = track
        return repo

    current_dir = getcwd().split("/")
    current_dir.remove('')
    repo = ""
    track = ""
    for element in current_dir:
        track += "/" + element
        repo = check_path(track, repo)
    post_commit_file = ""
    for argument in sys.argv:
        if "post_commit.py" in argument:
            post_commit_file = argument
    return (repo + "/" + post_commit_file).replace("post_commit.py", "")


def __add_content_file(name, content=""):
    """
    add_content_file(name, content)  -> add content to a file.
    This function add content to a file, if it's not exist, create it.
    Required arguments:
        name        -- name of file.
        content     -- content add to file.
    """
    try:
        file_descriptor = open(name, O_RDWR | O_CREAT, 0o644)
        byte_object = str.encode(content)
        write(file_descriptor, byte_object)
        return close(file_descriptor)
    except PermissionError:
        return("Can not execute post_commit.")


def increase_version():
    """Increment Version on Git Commit.

    When changes are committed to the Git repository, the script automatically
    increments the patch number of a semantic versioning 3-component number
    (at least 1) stored in a file VERSION located at the root folder of
    a Git repository.

    If this file VERSION doesn't initially exist, the script creates it and
    stores the version 1.0.1 (the script assumes that the initial version
    before the commit is 1.0.0).
    """
    version_filepath = __find_repo() + "VERSION"
    content = ""
    if __get_file_type(version_filepath) == "file":
        content = __read_file(version_filepath)
    content = content.split(".")

    # Check if the file dose not store good content, set content empty.
    if "" in content:
        content == ""
    if len(content) != 3:
        content = ""
    try:
        for index in range(len(content)):
            content[index] = int(content[index])
    except ValueError:
        content = ""
    if isinstance(content, list):
        content[2] = content[2] + 1
        write_content = f"{content[0]}.{content[1]}.{content[2]}"
        return __add_content_file(version_filepath, write_content)
    remove(version_filepath)
    return __add_content_file(version_filepath, "1.0.1")


increase_version()
