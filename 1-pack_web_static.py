#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the
    web_static folder of your AirBnB Clone repo.
"""

from datetime import datetime
from os.path import isdir
from fabric.api import local

def do_pack():
    '''generates a .tgz archive from the contents of the web_static folder'''
    date_time = datetime.now()
    format_date = date_time.strftime("%Y%m%d%H%M%S")
    try:
        if not isdir("versions"):
            local("mkdir versions")
        file_names = "versions/web_static_{}.tgz".format(format_date)
        local("tar -cvzf {} web_static".format(file_names))
        return file_name
    except Exception as e:
        None
