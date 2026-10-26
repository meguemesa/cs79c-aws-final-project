# Biomedical Laboratory Antibody Inventory Tracker

**AWS Cloud Architecture Portfolio Project | Santa Monica College — CS79C**

## Project Overview

This project demonstrates a serverless antibody inventory tracking application built using Amazon Web Services (AWS). The application stores antibody information, retrieves inventory records, adds new antibodies, and updates remaining quantities.

I chose this project because I work in biomedical research and am responsible for managing an antibody repository. Part of my work involves keeping track of antibody names, clones, fluorophores, and available quantities. I wanted to build an application that relates to my work while learning how AWS services can be used to store, manage, and update inventory information.

The application uses fictional antibody inventory data for demonstration purposes.

## Architecture

The application follows a serverless architecture:

**Client → Amazon API Gateway → AWS Lambda → Amazon DynamoDB**

AWS Lambda also sends execution logs to Amazon CloudWatch for monitoring and troubleshooting.

The architecture diagram is included in this repository.

## AWS Services

| AWS Service | Purpose |
|---|---|
| Amazon API Gateway | Provides HTTP endpoints for inventory requests |
| AWS Lambda | Processes requests using Python |
| Amazon DynamoDB | Stores antibody inventory records |
| Amazon CloudWatch | Monitors Lambda execution logs and errors |
| AWS CloudFormation | Deploys infrastructure using a YAML template |
| AWS Identity and Access Management (IAM) | Controls Lambda permissions to access DynamoDB |

## Application Features

- **GET /antibodies:** Retrieves antibody inventory records.
- **POST /antibodies:** Adds a new antibody record.
- **PUT /antibodies:** Updates the remaining quantity of an existing antibody.
- Uses a unique antibody ID to identify each record.
- Records antibody name, clone, fluorophore, and remaining quantity.

## Infrastructure as Code

The `biomed-antibody-stack.yaml` file defines the infrastructure required to deploy a demonstration version of the application.

The CloudFormation stack successfully created 11 AWS resources, including DynamoDB, Lambda, API Gateway, IAM, and a CloudWatch alarm.

## Testing and Monitoring

The original application was tested using AWS Lambda test events, a web browser, and Windows PowerShell.

Testing included retrieving inventory records, adding antibodies, and updating remaining quantities.

A separate application was deployed using CloudFormation. Its GET endpoint returned an empty JSON array (`[]`), confirming successful retrieval from its new, empty DynamoDB table.

CloudWatch recorded Lambda execution events, including START, END, and REPORT entries. A CloudWatch alarm was configured to monitor Lambda errors.

## Security and Limitations

- IAM permissions restrict Lambda access to the application's DynamoDB table.
- DynamoDB uses encryption at rest.
- The demonstration API is publicly accessible and does not currently require authentication.
- Only fictional sample data should be used.
- A production application would require authentication and additional security controls.

## Repository Files

- `README.md` — Project overview and documentation.
- `biomed-antibody-stack.yaml` — CloudFormation infrastructure template.
- Architecture diagram — Visual representation of the serverless application.

## Project Status

The application has been deployed and tested successfully. CloudFormation deployment and CloudWatch monitoring have also been verified.

This project was developed for educational purposes as part of Santa Monica College CS79C.
