#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import grp
import os
import pwd
import subprocess

from iam import get_users_in_group


IAM_GROUP_NAME = os.environ.get('IAM_GROUP_NAME', 'AccessSSH')
SYS_GROUP_NAME = os.environ.get('SYS_GROUP_NAME', '_iam')

DEVNULL = open(os.devnull, 'wb')


def login_from_username(s):
    return s.split('@')[0]


if __name__ == '__main__':
    for _ in range(3):
        try:
            grp_iam = grp.getgrnam(SYS_GROUP_NAME)
        except KeyError:
            subprocess.call(['groupadd', '-g', '999', SYS_GROUP_NAME])
        else:
            break
    else:
        raise Exception('Cannot read/create group')

    print('SYNC: Synching IAM group %(group_name)s' % dict(group_name=IAM_GROUP_NAME))

    iam_users = get_users_in_group(IAM_GROUP_NAME)
    current = grp_iam.gr_mem
    logins = [login_from_username(u['UserName']) for u in iam_users]

    # remove obsolete users
    for login in current:
        if login not in logins:
            print('SYNC: removing user %(login)s' % dict(login=login))
            subprocess.call(['userdel', '-r', '-f', login], stderr=DEVNULL)
    # add missing users
    for user in iam_users:
        login = login_from_username(user['UserName'])
        if login not in current:
            print('SYNC: adding user %(login)s for IAM username %(username)s' % dict(login=login, username=user['UserName']))
            subprocess.call([
                'useradd',
                '-c', user['UserName'],
                '-d', '/home/%(login)s' % dict(login=login),
                '-m', '-N',
                '-g', SYS_GROUP_NAME,
                '-G', SYS_GROUP_NAME,
                '-s', '/bin/bash',
                login])
