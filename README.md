# OpenSSH authorization via AWS IAM

> !!! This is here for demonstration purpose only.

## Building and testing

This example is bundled as a Docker image for easy testing.

```
$ docker build -t openssh-iam .
```

The image will need some configuration to reach out to IAM:

**IAM_GROUP_NAME** - this is the group name in IAM that will be queried for the list of users to be added and allowed to authenticate and access the system.

If you run this on a system that is not in EC2 or does not have an InstanceRole attached you will have to provide **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY** environment variables that have policies to allow reads in IAM.

```
$ docker run --rm -it -P \
  -e AWS_ACCESS_KEY_ID=<your key id> \
  -e AWS_SECRET_ACCESS_KEY=<your secret key> \
  -e IAM_GROUP_NAME=<the IAM group with users> \
  openssh-iam
```

On startup it will connect out to IAM and request a list of users that are part of the given group. It will create system accounts for those users and allow them to connect via the exposed SSH port.
