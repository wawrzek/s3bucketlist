#!/usr/bin/env python3

import os
import random
import string
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import s3bucketlist

name ='-'.join(random.choices(string.ascii_lowercase, k=10))
name = 'test'
bucket = s3bucketlist.bucket4terraform(name, profile='s3bucketlist')
