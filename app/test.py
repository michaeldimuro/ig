#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from db import DB

if __name__ == "__main__":
    db = DB("accounts/ijerseywebdesign/data.db")

    botFollowed = db.bot_followed("ijerseywebdesign")
    print(botFollowed)

