#!/bin/bash

# pip installs
pip install boto3 # AWS Python SDK

# Check if aws CLI already installed
command -v aws >/dev/null 2>&1 
if [ "$?" -ne 0 ] ; then
    echo "AWS CLI not found, installing..."
    # This section is untested. 
    if [ "$(uname)" = "Darwin" ]; then # Install AWS CLI for MacOS
        curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
        installer -pkg AWSCLIV2.pkg -target / 

    # This section was tested on an Ubuntu system. 
    elif [ "$(uname)" = "Linux" ] ; then # Install AWS CLI for Linux flavors
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        ./aws/install
    fi
else
    echo "AWS CLI found, not re-installing..."
fi

# Configure credentials for AWS CLI (used by boto3) if needed
read -r -p "Would you like to configure aws credentials? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY]) 
        aws configure
        ;;
    *)
        echo "Exiting without configuring credentials..."
        ;;
esac