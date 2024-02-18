#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import s3bucketlist

name = "s3listtestcase"
bucket = s3bucketlist.bucket4terraform(name, profile="s3bucketlist")
print (f"Bucket {name}")
print ("\tis Accessible: %s"% bucket.isAccessible)
print ("\tis Empty: %s" % bucket.isEmpty)
print ("\thas tags: %s" % bucket.isTagged)
print ("\thas Terraform tag: %s" % bucket.isTerraformed)
print ("\twas created: %s" % bucket.timeCreation)

bucket.addDetails()

print ("\twas last updated: %s" % bucket.timeLastUpdate)
print ("\thas total size: %d" % bucket.sizeTotal)
print ("\twith total objects: %d" % bucket.objectsNumber)
