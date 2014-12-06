#!/usr/bin/env python
# coding=utf-8

#	> File Name: git_update.py
#	> Author: LY
#	> Mail: ly.franky@gmail.com
#	> Created Time: Saturday, December 06, 2014 AM09:11:06 CST

import os

cmd = "git add -A"
os.system(cmd)
cmd = "git add ."
os.system(cmd)
cmd = '''git commit -m"`curl -s http://whatthecommit.com/index.txt`"'''
os.system(cmd)
cmd = "git push origin master"
os.system(cmd)

