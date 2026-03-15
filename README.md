# Amazon EventBridge Scheduler to Amazon API Gateway

This pattern demonstrates how to use Amazon EventBridge Scheduler to invoke Amazon API Gateway REST API endpoints on a schedule. The pattern is deployed using the AWS Serverless Application Model (SAM).

Learn more about this pattern at Serverless Land Patterns: [https://serverlessland.com/patterns](https://serverlessland.com/patterns)

Important: this application uses various AWS services and there are costs associated with these services after the Free Tier usage - please see the [AWS Pricing page](https://aws.amazon.com/pricing/) for details. You are responsible for any AWS costs incurred. No warranty is implied in this example.

## Requirements

* [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and log in. The IAM user that you use must have sufficient permissions to make necessary AWS service calls and manage AWS resources.
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed and configured
* [Git Installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (AWS SAM) installed

## Deployment Instructions

1. Create a new directory, navigate to that directory in a terminal and clone the GitHub repository:
    ``` 
    git clone https://github.com/aws-samples/serverless-patterns
    ```
1. Change directory to the pattern directory:
    ```
    cd eventbridge-schedule-to-apigw-sam-python
    ```
1. From the command line, use AWS SAM to deploy the AWS resources for the pattern as specified in the template.yaml file:
    ```
    sam deploy --guided
    ```
1. During the prompts:
    * Enter a stack name
    * Enter the desired AWS Region
    * Allow SAM CLI to create IAM roles with the required permissions.

    Once you have run `sam deploy --guided` mode once and saved arguments to a configuration file (samconfig.toml), you can use `sam deploy` in future to use these defaults.

1. Note the outputs from the SAM deployment process. These contain the resource names and/or ARNs which are used for testing.

## How it works

This pattern showcases EventBridge Scheduler's ability to invoke API Gateway endpoints on a schedule using the AWS SDK integration.

### Architecture Flow

1. EventBridge Scheduler triggers every 5 minutes based on the configured schedule expression
2. Scheduler uses the AWS SDK integration to invoke the API Gateway endpoint
3. API Gateway receives the POST request and routes it to the Lambda function
4. Lambda function processes the request and returns a response
5. The response is logged and can be monitored through CloudWatch

### Key Features

EventBridge Scheduler invokes API Gateway using the `aws-sdk:apigateway:invoke` target, which provides:
- Direct API Gateway invocation without requiring a public endpoint
- Built-in retry mechanism with configurable attempts
- Flexible scheduling with rate or cron expressions
- Dynamic payload construction with scheduler variables

The Lambda function behind API Gateway processes the scheduled requests and can be extended to perform various tasks such as:
- Data processing and transformation
- External API calls
- Database operations
- Report generation
- System health checks

## Testing

### Test Automatic Scheduled Invocation

The schedule runs automatically every 5 minutes. View the Lambda function logs:

```bash
# Get function name from stack outputs
FUNCTION_NAME=$(aws cloudformation describe-stacks \
  --stack-name <your-stack-name> \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiFunctionName`].OutputValue' \
  --output text)

# Tail logs
aws logs tail /aws/lambda/${FUNCTION_NAME} --follow
```

### Test Manual API Gateway Invocation

Test the API Gateway endpoint manually:

```bash
# Get API Gateway URL from stack outputs
API_URL=$(aws cloudformation describe-stacks \
  --stack-name <your-stack-name> \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
  --output text)

# Invoke the endpoint
curl -X POST ${API_URL} \
  -H "Content-Type: application/json" \
  -d '{"source": "manual-test", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'
```

Expected response:
```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {
    "requestsProcessed": 1,
    "source": "manual-test",
    "receivedAt": "2026-03-04T10:00:00Z",
    "processedAt": "2026-03-04T10:00:01Z",
    "status": "success"
  }
}
```

### Monitor Scheduled Invocations

Check CloudWatch Logs for scheduled invocations:

```bash
# View recent logs
aws logs tail /aws/lambda/${FUNCTION_NAME} --since 10m
```

Look for log entries with `"source": "EventBridge Scheduler"` to identify scheduled invocations.

### Verify Schedule Status

Check the schedule status:

```bash
SCHEDULE_NAME=$(aws cloudformation describe-stacks \
  --stack-name <your-stack-name> \
  --query 'Stacks[0].Outputs[?OutputKey==`ScheduleName`].OutputValue' \
  --output text)

aws scheduler get-schedule --name ${SCHEDULE_NAME}
```

## Cleanup
 
1. Delete the stack
    ```bash
    sam delete --stack-name <your-stack-name>
    ```
1. Confirm the stack has been deleted
    ```bash
    aws cloudformation list-stacks --query "StackSummaries[?contains(StackName,'<your-stack-name>')].StackStatus"
    ```
----
Copyright 2026 Amazon.com, Inc. or its affiliates. All Rights Reserved.

SPDX-License-Identifier: MIT-0
