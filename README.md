# endpoint-latency-exporter


- Python script calculates the HTTP GET latency of an endpoint list
- Uses a Prometheus Push Gateway to have push based metric collection from Lambda Functions
- Deploys Lambda Functions across AWS Regions with Chalice
- Requires minimal configuration to get up and running

## Installation


### Chalice

```bash
pip3 install chalice
```

### Create AWS Profile per Region

Chalice doesn't have a good way of ascertain different regions on an AWS Profile.

We must create as many Profiles as Regions with regions defined in the `~/.aws/credentials` file.

Your `~/.aws/credentials` file should look like this before continuing.

```txt
[yourprofilename-us-west-1]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = us-west-1

[yourprofilename-us-west-2]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = us-west-2

[yourprofilename-us-east-1]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = us-east-1

[yourprofilename-us-east-2]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = us-east-2

[yourprofilename-eu-west-1]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = eu-west-1

[yourprofilename-eu-west-2]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = eu-west-2

[yourprofilename-eu-central-1]
aws_access_key_id = AKIA----------------
aws_secret_access_key = vBXPp----------------------------------
region = eu-central-1
```


### Edit the Chalice Config

- **environment_variables**:
    - `ENDPOINT_LIST`: Comma separated http urls to calculate the latency for
    - `PUSHGATEWAY_ENDPOINT`: Your Prometheus PushGateway endpoint
    - `LAMBDA_RATE_MINUTES`: Automatically call the lambda functions per N minutes
    - `PUSHGATEWAY_USERNAME`: (Do not define on no basic auth) PushGateway username
    - `PUSHGATEWAY_PASSWORD`: (Do not define on no basic auth) PushGateway password
- **stages**:
    - Chalice will manage each region in separate stages
    - We just need to add the region names as in the example config

### Deploy Chalice Lambda Functions

```bash
chalice deploy --stage us-west-1 --profile yourprofilename-us-west-1
chalice deploy --stage us-west-2 --profile yourprofilename-us-west-2
chalice deploy --stage us-east-1 --profile yourprofilename-us-east-1
chalice deploy --stage us-east-2 --profile yourprofilename-us-east-2
chalice deploy --stage eu-west-1 --profile yourprofilename-eu-west-1
chalice deploy --stage eu-west-2 --profile yourprofilename-eu-west-2
chalice deploy --stage eu-central-1 --profile yourprofilename-eu-central-1
```

### Add Grafana Dashboards 




### Delete Chalice Lambda Functions 

```bash
chalice delete --stage us-west-1 --profile yourprofilename-us-west-1
chalice delete --stage us-west-2 --profile yourprofilename-us-west-2
chalice delete --stage us-east-1 --profile yourprofilename-us-east-1
chalice delete --stage us-east-2 --profile yourprofilename-us-east-2
chalice delete --stage eu-west-1 --profile yourprofilename-eu-west-1
chalice delete --stage eu-west-2 --profile yourprofilename-eu-west-2
chalice delete --stage eu-central-1 --profile yourprofilename-eu-central-1
```

### (optional) manually trigger Lambda Functions

```bash
chalice invoke --name latency-exporter  --stage us-west-1 --profile yourprofilename-us-west-1
chalice invoke --name latency-exporter  --stage us-west-2 --profile yourprofilename-us-west-2
chalice invoke --name latency-exporter  --stage us-east-1 --profile yourprofilename-us-east-1
chalice invoke --name latency-exporter  --stage us-east-2 --profile yourprofilename-us-east-2
chalice invoke --name latency-exporter  --stage eu-west-1 --profile yourprofilename-eu-west-1
chalice invoke --name latency-exporter  --stage eu-west-2 --profile yourprofilename-eu-west-2
chalice invoke --name latency-exporter  --stage eu-central-1 --profile yourprofilename-eu-central-1
```
