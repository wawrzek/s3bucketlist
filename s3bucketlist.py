#!/usr/bin/env python


import boto3
import botocore
import datetime
import sys

class bucket4terraform:

    def __init__(self, name, profile="default", tagKey="Managed_by", tagValue="terraform", extraDetails=False):
        self.profile = profile
        try:
            bucket_head = self._getSession('c').head_bucket(Bucket=name)
        except botocore.exceptions.ClientError as error:
            print (error)
            sys.exit(3)
        except botocore.exceptions.NoCredentialsError as error:
            print (error)
            sys.exit(33)

        self.extraDetails = extraDetails
        self.name = name
        self.tagKey = tagKey
        self.tagValue = tagValue
        self.timeCreation = self._getSession('r').Bucket(name).creation_date

        self._setFlags()

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
        session = self._getSession("c")
        paginator = session.get_paginator("list_objects_v2")
        response = paginator.paginate(Bucket=self.name)
        for page in response:
            files = page.get("Contents")
            if files:
                for file in files:
                    objects += 1
                    size += file["Size"]
                    if file["LastModified"] > update:
                        update = file["LastModified"]
            else:
                objects = 0
                size = 0
                update = self.timeCreation
        self.objectsNumber = objects
        self.sizeTotal = size
        self.timeLastUpdate = update
        self.extraDetails = True


    def _getSession(self, kind):
        try:
            session = boto3.session.Session(profile_name=self.profile, region_name='us-east-1')
        except botocore.exceptions.ProfileNotFound as Error:
            print (f"Profile '{self.profile}' not found in the config")
            sys.exit(2)
        if kind == 'c':
            return session.client(service_name="s3")
        elif kind == 'r':
            return session.resource("s3")

    def _setFlags(self):
        self.isAccessible = True
        self.isEmpty = False
        self.isTagged = True
        self.isTerraformed = False
        session = self._getSession("r")
        bucket = session.Bucket(self.name)
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
                print ("Not handled error accessing tags for bucket %s" % self.name)
                sys.exit(5)
        else:
            for tags in tagSet:
                if tags == {"Key": self.tagKey, "Value": self.tagValue}:
                    self.isTerraformed = True
                    break
                if sum([1 for _ in bucket.objects.limit(1)]) == 0:
                    self.isEmpty = True

class bucketlists4terraform:

    def __init__(self, profile="default"):

        self.profile = profile

        session = self._getSession("c")

        self.lists = [
                "isAccessible",
                "isEmpty",
                "isTagged",
                "isTerraformed",
                ]

        self.all = [b['Name'] for b in session.list_buckets()["Buckets"]]

        tempLists = {}
        for l in self.lists:
            tempLists[l] = []
        for b in self.all:
            bucket = bucket4terraform(b, profile=self.profile)
            for l in self.lists:
                if getattr(bucket,l):
                    tempLists[l].append(bucket.name)

        self.empty = tempLists['isEmpty']
        self.notAccessible = [b for b in self.all if b not in tempLists['isAccessible']]
        self.tagged = [b for b in self.all if b in tempLists['isTagged']]
        self.taggedEmpty = [b for b in self.tagged if b in self.empty]
        self.notTagged = [b for b in self.all if b not in tempLists['isTagged']]
        self.notTaggedEmpty = [b for b in self.notTagged if b in self.empty]
        self.terraformed = [b for b in self.tagged if b in tempLists['isTerraformed']]
        self.terraformEmpty = [b for b in self.terraformed if b in self.empty]
        self.notTerraformed = [b for b in self.tagged if b not in tempLists['isTerraformed']]

    def _getSession(self, kind):
        try:
            session = boto3.session.Session(profile_name=self.profile, region_name='us-east-1')
        except botocore.exceptions.ProfileNotFound as Error:
            print (f"Profile '{self.profile}' not found in the config")
            sys.exit(2)
        if kind == 'c':
            return session.client(service_name="s3")
        elif kind == 'r':
            return session.resource("s3")



