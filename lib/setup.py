#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os


def get_roles(args):
    dir_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isfile(args+d):
            pass
        else:
            dir_list.append(d)
    return dir_list


def get_playbook(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            pass
        elif d.endswith(".retry"):
            os.remove(args+d)
        else:
            files_list.append(d)
    return files_list


def get_scripts(args):
    files_list = []
    dirs = os.listdir(args)
    for d in dirs:
        if d[0] == '.':
            pass
        elif os.path.isdir(args+d):
            pass
        else:
            files_list.append(d)
    return files_list
