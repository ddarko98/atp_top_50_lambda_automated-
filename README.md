🎾**ATP Top 50 Lambda Function**

This AWS Lambda function processes ATP tennis match data from Kaggle, generates a Top 50 ATP Players Report, and uploads the results to Amazon S3. Notifications are sent via Amazon SNS upon success or failure.

🚀 **Workflow**

1. Dataset Download

Uses a custom AWS Lambda Layer with kagglehub
.

Downloads dataset:
dissfya/atp-tennis-2000-2023daily-pull

2. Data Processing (Pandas)

Cleans and parses match data.

Extracts winners for each match.

Classifies tournaments into:

Grand Slam

ATP 1000

ATP 500

Other

3. Statistics Aggregation
Calculates for each player:

Total wins

Grand Slam wins

ATP 1000 wins

ATP 500 wins

First recorded win

Last recorded win

4. Report Generation

Creates a CSV with the Top 50 players by total wins.

Uploads the file to S3:

s3://<your-s3-bucket>/final/atp-top-50-YYYY-MM-DD.csv


Example (sample only):

s3://my-bucket/final/atp-top-50-2025-08-17.csv


5. Notifications

Publishes a success or error message to an SNS Topic:

arn:aws:sns:us-east-1:<account-id>:ATPProcessingTopic

🕒 Scheduling

The Lambda is triggered by Amazon EventBridge with a cron expression:

0 4 ? * 2 *


This means: Every Monday at 04:00 UTC.

EventBridge Rule ARN (masked example):

arn:aws:events:us-east-1:<account-id>:rule/atp-top-50-triggering

🔑 IAM Permissions

The Lambda execution role requires these permissions:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::<your-s3-bucket>/final/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::<your-s3-bucket>"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:<account-id>:ATPProcessingTopic"
    }
  ]
}

🛠 Challenges

The biggest challenge was creating a custom AWS Lambda Layer for kagglehub.
It required multiple attempts to properly package and deploy dependencies.

📂 Project Structure
lambda_function.py     # Main Lambda code
layers/                # Custom kagglehub layer
requirements.txt       # Dependencies
README.md              # Documentation

✅ Example Lambda Output (Top 10 Players)
player_name	total_wins	grand_slam_wins	atp1000_wins	atp500_wins	first_win	last_win
Player A	870	25	38	22	2002-01-15	2023-10-01
Player B	755	20	32	18	2005-04-20	2023-09-25
...	...	...	...	...	...	...
📢 Notifications

On success → Publishes:
"ATP Top 50 report successfully created and uploaded to S3!"

On failure → Publishes full error message and traceback to the SNS topic.

⚡ How to Deploy

1. Prepare the Lambda Layer

Package kagglehub (and its dependencies) into a .zip.

Upload as a custom Lambda Layer.

2. Deploy the Lambda Function

Upload lambda_function.py to AWS Lambda.

Attach the execution role with the IAM policy above.

3. Configure Environment Variables

Set:

KAGGLEHUB_CACHE=/tmp/kagglehub


4. Connect to EventBridge

Create a rule with the cron expression 0 4 ? * 2 *.

5. Test

Run manually once.

Verify the CSV is uploaded to S3 and a notification is sent.
