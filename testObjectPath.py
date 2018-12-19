#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tests import doTests

# starts all test suites
# doTests()


import objectpath

data = {
    "peoples": [
        {
            "name": "Kelly Robertson",
            "birthDate": "1980-05-11 04:22:33"
        },
        {
            "name": "Trevin Haley",
            "birthDate": "1985-09-12 12:03:10"
        }
    ]
}

t = objectpath.Tree(data)
r = t.execute("avg(age(dateTime($.peoples.birthDate,'%Y-%m-%d %H:%M:%S')))")
print(r)
