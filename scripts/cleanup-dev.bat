@echo off
echo 🧹 Cleaning up existing AWS resources for dev environment...

REM Set AWS region
set AWS_DEFAULT_REGION=us-east-1

REM Delete DynamoDB Tables
echo Deleting DynamoDB tables...
aws dynamodb delete-table --table-name oyins-journey-dev-skills 2>nul
aws dynamodb delete-table --table-name oyins-journey-dev-projects 2>nul
aws dynamodb delete-table --table-name oyins-journey-dev-adrs 2>nul
aws dynamodb delete-table --table-name oyins-journey-dev-versions 2>nul
aws dynamodb delete-table --table-name oyins-journey-dev-certifications 2>nul

REM Delete IAM Role and Policy
echo Deleting IAM resources...
aws iam delete-role-policy --role-name oyins-journey-dev-lambda-role --policy-name oyins-journey-dev-lambda-policy 2>nul
aws iam delete-role --role-name oyins-journey-dev-lambda-role 2>nul

REM Delete API Gateway
echo Deleting API Gateway...
for /f "tokens=*" %%i in ('aws apigateway get-rest-apis --query "items[?name=='oyins-journey-dev-api'].id" --output text') do (
    if not "%%i"=="" if not "%%i"=="None" (
        aws apigateway delete-rest-api --rest-api-id %%i
        echo Deleted API Gateway: %%i
    )
)

REM Delete S3 Buckets
echo Deleting S3 buckets...
for /f "tokens=3" %%i in ('aws s3 ls ^| findstr "oyins-journey-dev-"') do (
    echo Emptying and deleting bucket: %%i
    aws s3 rm s3://%%i --recursive 2>nul
    aws s3 rb s3://%%i 2>nul
)

echo ✅ Cleanup complete! You can now deploy with a clean slate.
pause