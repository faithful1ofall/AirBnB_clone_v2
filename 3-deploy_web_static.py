#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/school -u ubuntu
"""

from fabric.operations import run, put, env, settings, local
from os.path import isdir as test
from datetime import datetime
env.hosts = ["34.229.161.131", "54.89.46.50"]
env.user = 'ubuntu'
time = datetime.now().strftime("%Y%m%d%H%M%S")
archive_path = "versions/web_static_{}.tgz".format(time)
name = archive_path.split("/")[-1]


def deploy():
    """calls do_pack and do_deploy"""
    do_pack()


def do_pack():
    """create packet"""
    try:
        local("mkdir -p versions && tar -cvzf {} ./web_static"
              .format(archive_path))
        return name
    except:
        return False


def do_deploy(archive_path):
    """uploads to server"""
    if not (test(archive_path)):
        return False
    try:
        put(archive_path, "/tmp")
        path = "/data/web_static/releases/".format(name.split(".")[0])
        run("mkdir {0} && tar -xzf /tmp{1} -C {0}".format(path, name))
        run("rm /tmp/{} && rm -rf /data/web_static/current".format(name))
        run("ln -s {} /data/web_static/current".format(path))
        return True
    except:
        return False
