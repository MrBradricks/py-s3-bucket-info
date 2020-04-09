### Summary: 
This script allows for viewing select metadata about Amazon S3 buckets you are authorized to see.

### Setup: 
Run the `./setup.sh` script with sudo to configure the AWS CLI and install pip dependencies.
```
sudo ./setup.sh
```

The AWS CLI will need your **AWS Access Key ID** as well as your **AWS Secret Access Key**.
It will also prompt for a **Default region name**, and **Default output format** but these are not required to view information on S3 buckets. They can safely be left blank.

If you already have the aws CLI configured it will not reinstall it, and you will be given the option to skip user configuration. If still choose to proceed and an existing configuration exists, the defaults will be auto-populated as the previous values.

You can read more on the AWS CLI [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

### Usage: 
Run `./buckets.py` to see information about s3 buckets the authorized AWS user can see.
```
./buckets.py
```

-h, --help Will show a help menu with useful info
-H will convert the bucket byte size into a human readable format 

### Limitations: 
This is untested on Darwin systems, but there should be no incompatibilities

There may be edge cases 