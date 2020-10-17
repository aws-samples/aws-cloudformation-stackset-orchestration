# AWS CloudFormation StackSet Orchestration: Automated deployment using AWS Step Functions

This project allows you to orchestrate AWS CloudFormation StackSet instance creation by using YAML files on an Amazon S3 bucket.

For further information, see the [blog post related to this repository](https://aws.amazon.com/blogs/mt/aws-cloudformation-stackset-orchestration-automated-deployment-using-aws-step-functions/).

## Purposes

We often use StackSets to automatically deploy infrastructure into many different accounts. Whether they
are Control-Tower-managed or Organizations-managed accounts, StackSets provide a simple and automated
way to handle the creation of resources and infrastructure right after provisioning a new account.

You can automatically deploy StackSets to accounts which belong to one or many specific Organizational Units
in [AWS Organizations](https://aws.amazcom/about-aws/whats-new/2020/02/aws-cloudformation-stacksets-introduces-automatic-deployments-across-accounts-and-regions-through-aws-organizations/).
Nevertheless, this workflow is not suitable for every use-case, specially when you need to override parameters of
the StackSets depending on the target account.

To provide a solution to this issue, we have created this project which allows you to automatically deploy StackSet
instances into specific accounts by using S3, AWS Step Functions and YAML configuration files. We used this implementation
because it allowed us to specify the StackSet deployment configuration of our accounts as source code files, which
is a characteristic of the Infrastructure as Code paradigm, and it goes along with the DevOps culture.

## Security considerations

The implementation is safe security-wise due to the automation of all of the deployment and deletion operations.
The remaining risk surface is the input of files to the S3 bucket, which can be protected using standard S3
security mechanisms (such as S3 Bucket policies or IAM policies), or whichever method you see fit.

This example uses an IAM Role (StacksetAdministrator), created with a Trust Relationship which allows an AWS Principal
specified as a parameter at deployment time to assume it and put objects in the Bucket.

## Requirements

- This implementation uses the AWS Serverless Application Model (SAM) (https://aws.amazon.com/serverless/sam/)  in order to deploy the required infrastructure. Be sure to install the SAM CLI if you want to deploy the code. Follow the recommended installation procedure (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) according to your Operating System.

- Docker is also needed since it is used for the SAM build (--use-container) to locally compiles the lambda functions in a Docker container that functions like a Lambda environment, so they are in the right format when you deploy them to the AWS Cloud.

- An S3 bucket is needed, which will be used by the SAM CLI to upload the Lambda packages that will be used to provision the Lambda functions. This is not to be confused with the bucket which will contain the YAML configuration files, which will be created by the CloudFormation template at deployment time.

- Also, make (https://www.gnu.org/software/make/) is used to deploy the resources, wrapping the SAM CLI commands. If you do not have make on your workstation, or you do not wish to install it, you can run the commands that are specified inside of the Makefile manually.

## Deployment

In order to deploy the implementation, follow these steps:

```
# Clone the respository
git clone https://github.com/aws-samples/aws-cloudformation-stackset-orchestration

# Move to the repository's directory
cd aws-cloudformation-stackset-orchestration

# Use the deploy target on the provided Makefile, provide your own bucket name
make deploy s3-bucket=yourbucketname stackset_administrator_principal=arn:aws:iam::123456789012:role/Admin
```

Be sure to configure your AWS credentials before running the previous step. This
will package all of the Lambda functions, and upload them to the specified S3 bucket.
Once the deployment is done, you can move ahead and use the implementation.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

