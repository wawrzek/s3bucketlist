#!/usr/bin/env python


import boto3
import botocore
import datetime
import sys

class bucket4terraform:


    def __init__(self, name, profile="default", tagKey="Managed_by", tagValue="terraform", extraDetails=False):

        try:
            bucket_head = self._getSession(profile, 'c').head_bucket(Bucket=name)
        except botocore.exceptions.ClientError as error:
            print (error)
            sys.exit(3)

        self.extraDetails = extraDetails
        self.name = name
        self.profile = profile
        self.tagKey = tagKey
        self.tagValue = tagValue
        self.timeCreation = self._getSession(profile, 'r').Bucket(name).creation_date

        self._setFlags(self.name, self.profile)

        if extraDetails:
            addDetails()
        else:
            self.objectsNumber = "Unknown"
            self.sizetotal = "Unknown"
            self.timeLastUpdate = "Unknown"


    def addDetails(self):
        objects = 0
        size = 0
        update = self.timeCreation
        session = self._getSession(self.profile, "c")
        paginator = session.get_paginator("list_objects_v2")
        response = paginator.paginate(Bucket=self.name)
        for page in response:
            files = page.get("Contents")
            for file in files:
                objects += 1
                size += file["Size"]
                if file["LastModified"] > update:
                    update = file["LastModified"]
        self.objectsNumber = objects
        self.sizeTotal = size
        self.timeLastUpdate = update
        self.extraDetails = True


    def _getSession(self, profile, kind):
        try:
            session = boto3.session.Session(profile_name=profile)
        except botocore.exceptions.ProfileNotFound as Error:
            print (f"Profile '{profile}' not found in the config")
            sys.exit(2)
        if kind == 'c':
            return session.client(service_name="s3")
        elif kind == 'r':
            return session.resource("s3")

    def _setFlags(self, name, profile):

        self.isAccessible = True
        self.isEmpty = False
        self.isTagged = True
        self.isTerraformed = False

        session = self._getSession(self.profile, "r")
        bucket = session.Bucket(name)
        try:
            tagSet = bucket.Tagging().tag_set
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == "NoSuchTagSet":
                self.isTagged = False
            elif error.response['Error']['Code'] == "AccessDenied":
                self.isAccessible = False
            else:
                print (error)
                print ("=" *80)
                print ("Not handled error accessing tags for bucket %s" % name)
                sys.exit(5)
        else:
            for tags in tagSet:
                if tags == {"Key": self.tagKey, "Value": self.tagValue}:
                    self.isTerraformed = True
                    break
                if sum([1 for _ in bucket.objects.limit(1)]) == 0:
                    self.isEmpty = True
