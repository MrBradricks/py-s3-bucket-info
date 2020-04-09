#!/usr/bin/env python
import boto3
import argparse
import math

# Function to parse any arguments passed to the script
def getArgs():
    parser = argparse.ArgumentParser(description='Script to view S3 bucket data')
    parser.add_argument("-H", action="store_true", dest='human_readable', help="Convert bucket size to powers of 1000 (kB, MB, GB ...)", required=False)
    args = parser.parse_args()
    return args

# Function to convert bytes to human readable units
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

args = getArgs()
# Connect to S3 using AWS config and return buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    print("")
    print("Bucket: " +bucket["Name"])
    print("Creation Date: " + str(bucket["CreationDate"]))

    # Loop through files to parse their data, try to catch empty puckets without this key
    try:
        objs = s3.list_objects_v2(Bucket=bucket["Name"])['Contents']
        print ("Total Files: " + str(len(objs)))

        # Here we calculate the sum of all files in the bucket, and convert the bytes to a human readable unit if requested
        # We also find the largest single file in the bucket and its size.
        size = 0
        largest = {'Size': '0', 'Key': 'None'}
        for obj in objs:
            size = size + obj['Size']
            if int(obj['Size']) >= int(largest['Size']):
                largest['Size'] = obj['Size']
                largest['Key'] = obj['Key']
        if args.human_readable:
            size = convert_size(size)
            largest['Size'] = convert_size(largest['Size'])
        print ("Total Size: " + str(size))
        print ("Largest File: " + str(largest['Key']))
        print ("Largest File Size: " + str(largest['Size']))


        # Here we get the last modified file and its modify date
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        last_modified_name = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)][0]
        last_modified_date = [obj['LastModified'] for obj in sorted(objs, key=get_last_modified, reverse=True)][0]
        print("Last modified file: " + last_modified_name)
        print("Last modified date: " + str(last_modified_date))

    # If Contents key was missing, bucket is either empty or you have bad permissions.
    except KeyError:
        print "This bucket appears to be empty. Check permissions if this is unexpected"