#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from shutil import rmtree
import time
import subprocess as sp
from subprocess import PIPE
import tempfile
import pysvn

from urllib.parse import urlparse
from config_monitoring import svn_login, svn_password

class SvnClient:
    def __init__(self):
        self.login = svn_login
        self.password = svn_password
        self.timeout = 300

    def connect(self):
        client = pysvn.Client()
        client.callback_ssl_server_trust_prompt = lambda dummy: (True, 0, False)
        cancel_at = time.time() + self.timeout
        client.callback_cancel = lambda: time.time() > cancel_at
        client.set_auth_cache(False)
        client.set_store_passwords(False)
        client.set_interactive(False)
        client.set_default_username(self.login)
        client.set_default_password(self.password)
        return client

    def checkout(self, svn_url, folder):
        client = SvnClient.connect(self)
        try:
            client.checkout(svn_url, folder)
            return True
        except:
            return False


class Merger(SvnClient):
    def __init__(self):
        super().__init__()

    def svnWrapper(self, br, tr, cwd):
        p = sp.Popen(['svn', 'merge', tr, '--username', self.login, '--password', self.password, '--non-interactive', '--no-auth-cache'],
                     cwd=cwd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
        out, err = p.communicate()
        mergeResult = out + err
        msg = 'Web button: more trunk merged into {0}'.format(br)
        p = sp.Popen(
            ['svn', 'commit', '-m', msg, '--username', self.login, '--password', self.password, '--non-interactive', '--no-auth-cache'],
            cwd=cwd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
        out, err = p.communicate()
        commitResult = out + err
        return mergeResult + commitResult

    def mergeGo(self, branch):
        url = ''
        path = urlparse(branch).path.split('/')
        trunk = os.path.join(url, path[1], path[2], 'trunk').replace('\\', '/')
        tempDir = tempfile.mkdtemp()
        self.checkout(branch, tempDir)
        result = self.svnWrapper(branch, trunk, tempDir)
        rmtree(tempDir)
        return result

if __name__ == '__main__':
    branch = ''
    m = Merger()
    m.mergeGo(branch)