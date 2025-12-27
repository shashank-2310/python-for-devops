
---

# Day 08 – AWS Automation with Python (Boto3)

## 📌 Overview

This project demonstrates how Python can be used to **automate AWS infrastructure discovery** using **Boto3**, AWS’s official SDK for Python.

The script safely connects to an AWS account and **reads information only** (no create/update/delete actions), making it beginner-friendly and production-safe.

It reflects common real-world DevOps tasks such as:

* Validating AWS credentials
* Querying AWS services via APIs
* Structuring and exporting infrastructure data

---

## 🎯 Objectives Achieved

* Connect to AWS using Boto3
* Validate AWS credentials using STS
* List:

  * EC2 instances (ID, state, type, AZ, Name tag)
  * S3 buckets (bucket names)
* Print results to the terminal
* Export results to JSON files
* Prevent duplicate data on repeated runs

---

## 🧠 Design Approach

### 1. Credential Validation

Before making any AWS API calls, the script validates credentials using a **lightweight STS call**:

```python
sts.get_caller_identity()
```

This ensures:

* AWS credentials exist
* The script fails fast if credentials are misconfigured

The validation method is intentionally kept **private** and used only during initialization.

---

### 2. EC2 Instance Discovery

The script fetches EC2 instance details including:

* Instance ID
* Instance Name (from tags)
* Instance type
* Availability Zone
* Instance state

AWS tags are safely handled and converted into a dictionary for easy access.

---

### 3. S3 Bucket Discovery

The script lists all S3 buckets in the account and extracts:

* Bucket names only

This keeps the output clean and focused.

---

### 4. Output Handling

The results are:

* Printed in a readable JSON format in the terminal
* Exported to separate JSON files:

  * `instances.json`
  * `buckets.json`

If the files already exist:

* EC2 instances are deduplicated using `InstanceId`
* S3 bucket names are deduplicated using set logic

This allows safe re-runs without corrupting data.

---

## 📂 Project Structure

```
.
├── aws_utils.py        # Main Python script
└── solution.md
```

---

## ▶️ How to Run

### 1️⃣ Prerequisites

* Python 3.8+
* AWS account
* AWS credentials configured using one of:

  * `aws configure`
  * Environment variables
  * IAM role (EC2 / CI/CD)

### 2️⃣ Install Dependencies

```bash
pip install boto3
```

### 3️⃣ Run the Script

```bash
python aws_utils.py
```

---

## 🖨️ Sample Output (Terminal)

```json
[
    {
        "id": "i-0123456789abxxxxx",
        "name": "web-server",
        "type": "t2.micro",
        "az": "ap-south-1a",
        "state": "running"
    }
]
```

---

## 🛡️ Safety Notes

* ❌ No resources are created, modified, or deleted
* ✅ Read-only AWS API calls
* ✅ Safe for learning and experimentation

---

## 🚀 Key Learnings

* How AWS services expose data via APIs
* How Boto3 interacts with AWS infrastructure
* How DevOps engineers automate visibility tasks
* How to structure reusable and defensive Python code

---

## 🔮 Possible Enhancements

* Add EC2 paginator for large accounts
* Add multi-region support
* Export data to S3 instead of local files
* Convert script into a CLI using `argparse`
* Add IAM role assumption for multi-account access

---

## ✅ Conclusion

This project provides a practical introduction to **AWS automation using Python**, mirroring how DevOps engineers interact with cloud infrastructure in real-world environments.

It builds a strong foundation for:

* Infrastructure automation
* Monitoring scripts
* CI/CD cloud integrations

