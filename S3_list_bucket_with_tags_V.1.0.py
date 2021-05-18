'''Version 1.0 Owned By Vitalii Fedorak
To use it, shoud be installed aws cli and configured
Install required python libs before execution.
Run the script with the parameter " > s3list.txt" or "s3list.csv" to save the output to a file.
After the script finished, you may convert the file to *.xslx .  
With formating data by ","  you will receive row |bucket_name|creation_date|tag1|tag2|tag3|tagn|

To improve the speed of execution the script you may run it from the EC2 instance'''

import boto3
from botocore.exceptions import ClientError


s3 = boto3.client('s3')

#function to get and filter tags
def get_tags(bucket_name,bucket_creation): 

    #defining required tags for filtering in the list
    Org = None
    Product = None
    Env = None
    DevTeam = None
    OpTeam = None
    EpDevTeam = None
    OtherTags = None
    try:
        s3bucket = boto3.resource('s3')
        tag_get = s3bucket.BucketTagging(bucket_name).tag_set
        #Conditions for tag value
        for tag in tag_get:
            tag_values = list(tag.values())
            if tag_values[0] == 'Organization':
                Org = tag_values[1]
            elif tag_values[0] == 'Product':
                Product = tag_values[1]
            elif tag_values[0] == 'Environment':
                Env = tag_values[1]
            elif tag_values[0] == 'DevelopmentTeam':
                DevTeam = tag_values[1]  
            elif tag_values[0] == 'OperationsTeam':
                OpTeam = tag_values[1]                
            elif tag_values[0] == 'EPAMDevelopmentTeam':
                EpDevTeam = tag_values[1]
            elif tag_values[0] != ('Organization', 'Product','Environment','DevelopmentTeam','OperationsTeam','EPAMDevelopmentTeam'):
                OtherTags = tag_values   
        # sorting tag in the list
        bucket_tags = [Org, Product, Env, DevTeam, OpTeam, EpDevTeam, OtherTags]        
        #Printing the S3 Buckets, Creation Date  with its tags            
        print(bucket_name,',', bucket_creation,',', bucket_tags)      
    except ClientError as e:
        pass
        #Printing the S3 Bucket, Creation Date without tags
        print(bucket_name,',', bucket_creation)
#Function to get S3 BucketName from the list of Buckets
def get_bucket():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        bucket_name = bucket['Name']
        bucket_creation = bucket['CreationDate'].date()
        get_tags(bucket_name,bucket_creation)          

if __name__ == '__main__':
    print(get_bucket())

    
