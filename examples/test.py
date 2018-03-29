#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

api = InstagramAPI("michaeldimuro", "beastmedia123")
if (api.login()):
    print("Login succes!")
    api.searchUsername("michaeldimuro")
    print(api.LastJson)
    print(api.LastJson['user']['pk'])


else:
    print("Can't login!")
