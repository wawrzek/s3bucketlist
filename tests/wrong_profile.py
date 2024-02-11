#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import s3bucketlist

bucket = s3bucketlist.bucket4terraform('test', profile='')
