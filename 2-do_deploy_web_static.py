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
    put(archive_path, "/tmp/{}".format(archive_filename))

    # Uncompress the archive to the folder
    #     /data/web_static/releases/<archive filename without extension> on
    #     the web server

    # get the release directory
    release_directory = "/data/web_static/releases/{}".format(
        archive_filename.replace(".tgz", ""))

    # create the release directory
    run("mkdir -p {}".format(release_directory))

    # uncompress the data
    run("tar -xzf /tmp/{} -C {}"
        .format(archive_filename, release_directory))

    # Delete the archive from the web server
    run("rm /tmp/{}".format(archive_filename))
    run("mv /data/web_static/releases/{}"
        "/web_static/* /data/web_static/releases/{}/"
        .format(release_directory,
                release_directory))

    run("rm -rf /data/web_static/releases/{}/web_static".format(
        release_directory))

    # Update the symbolic link
    current_link = "/data/web_static/current"

    # Delete the symbolic link /data/web_static/current from the web server
    run("rm -f {}".format(current_link))

    #  Create a new the symbolic link
    #  /data/web_static/current on the web server,
    #     linked to the new version of your code
    #     (/data/web_static/releases/<archive filename without extension>)
    run("ln -sf {} {}".format(release_directory, current_link))

    return True
