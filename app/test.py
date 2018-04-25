#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

if __name__ == "__main__":
    api = InstagramAPI("michaeldimuro", "mikedimuro99")
    if api.login():
        print("Logged in")
        api.getUserFeed("6307810977")
        print(str(api.LastJson))
    else:
        print("Could not log in.")

