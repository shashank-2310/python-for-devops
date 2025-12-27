import boto3

class AWSutils:
    def __init__(self) -> None:
        self.s3 = boto3.client("s3")
        self.ec2 = boto3.client("ec2")


    def get_connection(self, service):
        return boto3.client(service)


    def show_buckets(self):
        response = self.s3.list_buckets()
        for bucket in response["Buckets"]:
            print(bucket["Name"])


    def create_bucket(self, bucket_name):
        response = self.s3.create_bucket(
            Bucket = bucket_name, 
            CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
            },)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("\nBucket created successfully!")
        else:
            print("\nError occurred!")


    def upload_to_bucket(self, file_path, bucket_name, key_name):
        self.s3.upload_file(file_path, bucket_name, key_name)
        print("File uploaded!")


    def show_regions(self):
        response = self.ec2.describe_regions()
        for region in response["Regions"]:
            print(region["RegionName"])


if __name__ == "__main__":
    aws = AWSutils()
# s3 = get_connection("s3")
# ec2 = get_connection("ec2")

# create_bucket(s3, "demo-demo-demo-create-2")
# show_buckets(s3)
# show_regions(ec2)
# upload_to_bucket(s3_client=s3, file_path="D:/DevOps/python-for-devops/day-07/design.md", bucket_name="demo-demo-demo-create-2", key="file.md")
