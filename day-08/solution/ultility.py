import boto3
import botocore.exceptions
import json
import sys
from pathlib import Path

class AWSUtils:
    def __init__(self, export_json: bool) -> None:
        try:
            self.session = boto3.Session()
            self.__validate_creds()

            self.s3 = self.session.client("s3")
            self.ec2 = self.session.client("ec2")
            
            self.export_json = export_json

        except botocore.exceptions.ClientError as e:
            print("Error occurred creating AWS clients: ", e)
            sys.exit(1)
    

    def __validate_creds(self):
        # Validate credentials by making a lightweight STS call (meant for internal-use only)
        try:
            sts = self.session.client("sts")
            sts.get_caller_identity()
        
        except botocore.exceptions.NoCredentialsError:
            print("AWS credentials not found. Configure credentials or set environment variables.")
            sys.exit(1)
        
        except botocore.exceptions.ClientError as e:
            print("AWS client error during credential check: ", e)
            sys.exit(1)
        
        except Exception as e:
            print("Unexpected error while checking credentials: ", e)
            sys.exit(1)
    

    def get_buckets(self):
        try:
            response = self.s3.list_buckets()
        
        except Exception as e:
            print("Error listing S3 buckets:", e)
            return []

        buckets = []
        for bucket in response.get("Buckets", []):
            buckets.append(bucket.get("Name", "N/A"))

        return buckets
    

    def get_instances(self):
        try:
            response = self.ec2.describe_instances()
        
        except Exception as e:
            print("Error describing instances:", e)
            return []

        instance_data = []
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = {tag.get('Key'): tag.get('Value') for tag in instance.get('Tags', [])}
                data = {
                    "id": instance.get('InstanceId', "N/A"),
                    "name": tags.get('Name', 'N/A'),
                    "type": instance.get('InstanceType', "N/A"),
                    "az": instance.get('Placement', {}).get('AvailabilityZone', "N/A"),
                    "state": instance.get('State', {}).get('Name', "N/A")
                }
                instance_data.append(data)

        return instance_data
    

    def display(self, lst: list, filename: str):
        print(json.dumps(lst, indent=4))

        if not self.export_json:
            return
        
        base_dir: Path = Path(__file__).parent
        json_file: Path = base_dir / filename

        try:

            if json_file.exists():
                existing_data = json.loads(json_file.read_text())
            else:
                existing_data = []

            #Prevents duplication of data in JSON files
            if filename == "instances.json":
                existing_ids = {item["id"] for item in existing_data if "id" in item}
                new_items = [item for item in lst if item["id"] not in existing_ids]
                existing_data.extend(new_items)

            elif filename == "buckets.json":
                existing_data = sorted(set(existing_data + lst))

            else:
                existing_data.extend(lst)
            
            json_file.write_text(json.dumps(existing_data, indent=4))
            print(f"Exported to {filename}")

        except Exception as e:
            print(f"Failed to write {filename}:", e)


def main():
    aws = AWSUtils(True)
    
    buckets = aws.get_buckets()
    instances = aws.get_instances()

    aws.display(instances,"instances.json")
    aws.display(buckets, "buckets.json")

if __name__ == "__main__":
    main()