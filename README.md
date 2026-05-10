# 🔍 AWS Cost Monitor

A Python CLI tool to monitor AWS resources and costs in real-time.

## Commands

```bash
# List all S3 buckets
python3 monitor.py buckets

# List all running EC2 instances  
python3 monitor.py instances

# Show AWS costs for current month
python3 monitor.py costs
```

## Tech Stack
- Python 3
- Boto3 (AWS SDK)
- Click (CLI framework)
- Rich (beautiful terminal output)

## Setup
```bash
pip install boto3 click rich
aws configure
python3 monitor.py --help
```

## Author
Prasad Sonar — github.com/prasad-sonar-code
