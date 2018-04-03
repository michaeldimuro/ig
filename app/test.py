#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from db import DB

if __name__ == "__main__":
    db = DB()
    db.create_connection("/Users/michaeldimuro/code/Instagram-API-python/app/accounts/ijerseywebdesign/data.db")

    print(db.expired())

