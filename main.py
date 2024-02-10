#!/usr/bin/env python


import boto3
import botocore
import datetime
import sys

class bucket4terraform:


    def __init__(self, name, profile='default', extra_details=False):

        try:
            self.time_creation = self._getSession(profile, 'r').Bucket(name).creation_date
        except botocore.exceptions.ClientError as Error:
            if error.response['Error']['Code'] == 'NoSuchBucket':
                print ("Wrong bucket name")
                sys.exit(3)
        self.extra_details = extra_details
        self.name = name
        self.aws_profile = profile

        resultFlags = _setFlags(self.name, self.profile)

        self.isAccessible = resultFlags[0]
        self.isTerraformed = resultFlags[1]
        self.isTagged = resultFlags[2]


    def _setFlags(self, name, profile):

        isAccessible = True
        isEmpty = False
        isTagged = True
        isTerraformed = False

        session = self._getSession(self.aws_profile, 'r')
        try:
            tagSet = session.Bucket(name).Tagging().tag_set
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == "NoSuchTagSet":
                isTagged = False
            elif error.response['Error']['Code'] == "AccessDenied":
                isAccessible = False
            else:
                print ("=" *80)
                print ("Not handled error accessing tags for bucket %s" % bucket)
                sys.exit(5)
        else:
            for tags in tagSet:
                if tags == {"Key": tagKey, "Value": tagValue}:
                    isTerraformed = True
                    break
                if sum([1 for _ in bucket.objects.limit(1)]) == 0:
                    isEmpty = True
        return (isAccessible, isEmpty, isTagged, isTerraformed)


    def _getSession(self, aws_profile, kind):
        try:
            session = boto3.session.Session(profile_name=aws_profile)
        except botocore.exceptions.ProfileNotFound as Error:
            print (f"Profile '{aws_profile}' not found in the config")
            sys.exit(2)
        if kind == 'c':
            return session.client(service_name='s3')
        elif kind == 'r':
            return session.resource('s3')


def main():
    bucket = bucket4terraform('test')

if __name__ == "__main__":
    main()
