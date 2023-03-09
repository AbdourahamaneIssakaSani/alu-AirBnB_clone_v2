#!/usr/bin/python3
"""Comment"""
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Comment"""

    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        return False

    # Upload the archive to the web server
    archive_filename = os.path.basename(archive_path)
    put(archive_path, "/tmp/{}".format(archive_filename))

    # Uncompress the archive to /data/web_static/releases/
    release_directory = "/data/web_static/releases/{}".format(
        archive_filename.replace(".tgz", ""))

    run("mkdir -p {}".format(release_directory))
    run("tar -xzf /tmp/{} -C {}"
        .format(archive_filename, release_directory))
    run("rm /tmp/{}".format(archive_filename))
    run("mv {}/web_static/* {}/".format(release_directory, release_directory))
    run("rm -rf {}/web_static".format(release_directory))

    # Update the symbolic link
    current_link = "/data/web_static/current"
    # run("rm -f {}".format(current_link))
    run("ln -sf {} {}".format(release_directory, current_link))

    return True
