#!/usr/bin/env python


import boto3
import botocore
import datetime
import sys

class bucket4terraform:


    def __init__(self, name, profile='default', tagKey='Managed_by', tagValue='terraform', extraDetails=False):

        try:
            bucket_head = self._getSession(profile, 'c').head_bucket(Bucket=name)
        except botocore.exceptions.ClientError as error:
            print (error)
            sys.exit(3)

        self.tagKey = tagKey
        self.tagValue = tagValue
        self.timeCreation = self._getSession(profile, 'r').Bucket(name).creation_date
        self.extraDetails = extraDetails
        self.name = name
        self.profile = profile

        resultFlags = self._setFlags(self.name, self.profile)

        self.isAccessible = resultFlags[0]
        self.isEmpty = resultFlags[1]
        self.isTagged = resultFlags[2]
        self.isTerraformed = resultFlags[3]


    def _setFlags(self, name, profile):

        isAccessible = True
        isEmpty = False
        isTagged = True
        isTerraformed = False

        session = self._getSession(self.profile, 'r')
        bucket = session.Bucket(name)
        try:
            tagSet = bucket.Tagging().tag_set
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == "NoSuchTagSet":
                isTagged = False
            elif error.response['Error']['Code'] == "AccessDenied":
                isAccessible = False
            else:
                print (error)
                print ("=" *80)
                print ("Not handled error accessing tags for bucket %s" % name)
                sys.exit(5)
        else:
            for tags in tagSet:
                if tags == {"Key": self.tagKey, "Value": self.tagValue}:
                    isTerraformed = True
                    break
                if sum([1 for _ in bucket.objects.limit(1)]) == 0:
                    isEmpty = True
        return (isAccessible, isEmpty, isTagged, isTerraformed)


    def _getSession(self, profile, kind):
        try:
            session = boto3.session.Session(profile_name=profile)
        except botocore.exceptions.ProfileNotFound as Error:
            print (f"Profile '{profile}' not found in the config")
            sys.exit(2)
        if kind == 'c':
            return session.client(service_name='s3')
        elif kind == 'r':
            return session.resource('s3')
