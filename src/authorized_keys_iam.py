#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import grp
import os
import pwd
import sys

from iam import get_active_ssh_keys


SYS_GROUP_NAME = os.environ.get('SYS_GROUP_NAME', '_iam')


if __name__ == '__main__':
    try:
        username = sys.argv[1]

        group_info = grp.getgrnam(SYS_GROUP_NAME)
        user_info = pwd.getpwnam(username)
        user_dot_ssh = '%s/.ssh' % user_info.pw_dir
        user_authorized_keys = '%s/authorized_keys' % user_dot_ssh

        # check if user is part of the IAM managed group
        if not user_info.pw_gid == group_info.gr_gid:
            # user is not part of the managed group
            # read the users authorized_keys file and output the contents to
            # stdout for OpenSSHd
            # in case of an exception we'll fall through into the error case
            # which will terminate this program with the exitcode 1
            with open(user_authorized_keys, 'r') as fi:
                print(fi.read())
            sys.exit(0)
        # we are trying to access an IAM managed user
        # the gecos field does include our full IAM username
        keys = get_active_ssh_keys(user_info.pw_gecos)
        if len(keys):
            authorized_keys = '\n'.join(keys)
            # forward keys to OpenSSHd
            print(authorized_keys)
            # we'll cache the keys we received in the users .ssh/authorized_keys
            try:
                if not os.path.exists(user_dot_ssh):
                    os.mkdir(user_dot_ssh, 0700)
                    os.chown(user_dot_ssh,
                            user_info.pw_uid,
                            user_info.pw_gid)
                with open(user_authorized_keys, 'w') as cache:
                    cache.write(authorized_keys)
                    os.chown(cache.name,
                            user_info.pw_uid,
                            user_info.pw_gid)
                    os.chmod(cache.name, 0600)
            except:
                pass
        sys.exit(0)
    except IndexError, IOError:
        pass

    sys.exit(1)
