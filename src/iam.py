#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import boto3

client = boto3.client('iam')


def get_users_in_group(groupname):
    response = client.get_group(
        GroupName=groupname,
        MaxItems=1000
    )
    if response:
        return response['Users']


def get_active_ssh_keys(username):
    keys = []
    response = client.list_ssh_public_keys(
        UserName=username,
        MaxItems=1000
    )
    if response:
        for pk in response['SSHPublicKeys']:
            if pk['Status'] == 'Active':
                key = client.get_ssh_public_key(
                    UserName=username,
                    SSHPublicKeyId=pk['SSHPublicKeyId'],
                    Encoding='SSH'
                )
                if key:
                    keys.append(key['SSHPublicKey']['SSHPublicKeyBody'])
    return keys
