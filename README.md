# Info

This is a small module/program to expose selected S3 bucket information helpful to find old and unused buckets.
The information might be usuful for example when importing manually create buckets into Terraform.

There are following classes:

## Classes

### bucket4terraform
The class represent a bucket and expose following information:
- the bucket name
- the name of the profile used to access the bucket
- is the bucket accessible
- is the bucket empty
- does the bucket has any tags
- what is the terraform tag key
- what is the terraform tag value
- does the bucket has a "Terraform" tag
- when the bucket was it is create
- does the class has further details (which required extra time to obtain from AWS)
- total number of objects in the bucket (extra detail)
- total size of object in the bucket (extra detail)
- the last time an object was updated in the bucket (extra detail)

### bucketlists4terraform
The class contain a set of lists helping to find orphant buckets in an account.
All the list are created based on information provided by object from the bucket4terrafom class.
There are following lists:
- empty
- tagged
- taggedEmpty
- notTagged
- notTaggedEmpty
- terraformed
- terraformEmpty
- notTerraformed

There is also an additional list containing all buckets with not access granted to the profile.
- notAccessible

Please note that during creation the 'terraformed', 'terraformed' and 'notTerraformed' lists code check only a tag, not actual Terraform state or code.

# Versions
- 0.3.1 - fixes:
        bucketlists4terraform creation (now with tags);
        notTerraformed list in the same class;
        isEmpty flag definition in bucket4terraform class;
- 0.3 - add new class (bucketlists4terraform) with a simple test
- 0.2.1 - handling empty buckets and broken credentials;
        add valid bucket test;
        cosmetic changes (remove empty lines);
- 0.2 - add method to obtain the extra details;
        simplified how details are set (no passing profile and name around);
        simplified session creation;
        fix how creation time is obtained (use 'us-east-1' region: https://www.marksayson.com/blog/s3-bucket-creation-dates-s3-master-regions/);
      cosmetic changes (consistent usage of ");
        add extra test for enabling passing multiple bucket names;
- 0.1 - initial code with basic bucket properties exposed and simple tests


# Background

The precursor of this module was a simple script grouping S3 buckets.
It was prepared to help find manually created buckets and decide which of them should be migrate to Terraform.
I imagine it's not an uncommon situation.
There is an AWS account(s) with plenty of S3 buckets.
Many of them are old, created by people who left the organisation.
There is no documentation about them.
To help with them the original script was creating a few lists.
For example:
- no accessible buckets
- empty buckets with tags
- empty buckets without tags
- buckets with tag indicating it was create by terraform.

I thought that using a real problem will be an opportunity to refresh, or actually deepen my understanding of Python.
Rather then stopping on a simple script I decided to prepare something with objected oriented programming.
Maybe even a module.

