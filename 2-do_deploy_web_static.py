#!/usr/bin/python3
"""Comment"""
from fabric.api import *
import os

env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Comment"""

    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = os.path.basename(archive_path)
    result = put(archive_path, "/tmp/{}".format(archive_filename))
    if result.failed:
        return False
    # Uncompress the archive to the folder
    #     /data/web_static/releases/<archive filename without extension> on
    #     the web server

    # get the release directory
    release_directory = "/data/web_static/releases/{}".format(
        archive_filename.replace(".tgz", ""))

    # create the release directory
    result = run("mkdir -p {}".format(release_directory))
    if result.failed:
        return False

    # uncompress the data
    result = run("tar -xzf /tmp/{} -C {}"
                 .format(archive_filename, release_directory))
    if result.failed:
        return False
    # Delete the archive from the web server
    result = run("rm /tmp/{}".format(archive_filename))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(release_directory,
                         release_directory))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static".format(
        release_directory))
    if result.failed:
        return False
    # Update the symbolic link
    current_link = "/data/web_static/current"

    # Delete the symbolic link /data/web_static/current from the web server
    result = run("rm -f {}".format(current_link))
    if result.failed:
        return False
    #  Create a new the symbolic link
    #  /data/web_static/current on the web server,
    #     linked to the new version of your code
    #     (/data/web_static/releases/<archive filename without extension>)
    result = run("ln -sf {} {}".format(release_directory, current_link))
    if result.failed:
        return False

    return True
