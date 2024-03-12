#!/usr/bin/env python3


import os
import pprint
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import s3bucketlist

LISTS = [
	"empty",
    "notAccessible",
	"tagged",
	"taggedEmpty",
	"notTagged",
	"notTaggedEmpty",
	"terraformed",
	"terraformEmpty",
	"notTerraformed",
]

test = s3bucketlist.bucketlists4terraform(profile="s3bucketlist")

for l in LISTS:
    print (f"{l}:")
    print (getattr(test, l))
