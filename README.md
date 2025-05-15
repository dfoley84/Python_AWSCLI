# Python_AWSCLIPython AWS CLI Tool
A command-line interface tool for managing AWS resources using Python and Typer.

Overview
This tool provides a convenient command-line interface for common AWS management tasks, focusing on RDS (Relational Database Service) operations. It leverages the AWS SDK for Python (boto3) to interact with AWS services.

Features
Currently, the tool supports the following AWS RDS operations:

Change Instance Type: Modify the instance class of an RDS database
Change Engine Version: Upgrade or downgrade the engine version of an RDS database
Installation
Clone the repository:

Install the required dependencies:

Configure AWS credentials:

Make sure you have valid AWS credentials configured in ~/.aws/credentials or set as environment variables
You can also use the AWS CLI to configure credentials using aws configure
Usage
Basic Usage
Available Commands
RDS Commands
Change Instance Type:

Change Engine Version:

Help
For more information about available commands and options:

Requirements
Python 3.7+
boto3 1.28.0
typer 0.9.0
requests 2.31.0
Project Structure
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.