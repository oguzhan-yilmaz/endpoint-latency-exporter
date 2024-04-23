from chalice import Chalice, Rate
from pprint import pprint
import requests, json, logging, os
from datetime import timedelta
from prometheus_client import pushadd_to_gateway, CollectorRegistry, Gauge, push_to_gateway, Histogram, Info,Summary
from prometheus_client.exposition import basic_auth_handler
from time import sleep 

_INF = float("inf")
app = Chalice(app_name='endpoint-latency-exporter')
app.log.setLevel(logging.DEBUG)

registry = CollectorRegistry()
response_latency = Histogram(
    'response_latency_seconds',
    'Histogram of response latency in seconds',
    buckets=(1, 2, 4, 6, 8, 10, _INF),
    labelnames=['endpoint', 'region', 'instance'],
)

registry.register(response_latency)


def get_endpoints_from_env_var():
    endpoints_raw = os.environ.get("ENDPOINT_LIST", False)
    if not endpoints_raw:
        app.log.error(f"Env Var: {env_var_name} is not set properly.")
        return []
    endpoints_list = []
    for endpoint in endpoints_raw.split(','):
        endpoint = endpoint.strip()
        if endpoint:
            endpoints_list.append(endpoint)
    app.log.info(f"Got endpoint list: {str(endpoints_list)}.")
    return endpoints_list
    

def prom_pushgateway_auth_handler(url, method, timeout, headers, data):
    PUSHGATEWAY_USERNAME = os.environ.get("PUSHGATEWAY_USERNAME", False)
    PUSHGATEWAY_PASSWORD = os.environ.get("PUSHGATEWAY_PASSWORD", False)
    headers.append(('User-Agent', 'EndpointLatencyExporter/1.0'))  
    # pprint(headers)
    return basic_auth_handler(url, method, timeout, headers, data, PUSHGATEWAY_USERNAME, PUSHGATEWAY_PASSWORD)


def custom_push_to_gateway(registry, endpoint, region, elapsed_seconds):
    env = os.environ
    # PUSHGATEWAY_JOB_NAME = env.get("PUSHGATEWAY_JOB_NAME", "latency-exporter")
    PUSHGATEWAY_JOB_NAME = region # env.get("PUSHGATEWAY_JOB_NAME", "latency-exporter")
    PUSHGATEWAY_ENDPOINT = os.environ.get("PUSHGATEWAY_ENDPOINT")
    # push_to_gateway(PUSHGATEWAY_ENDPOINT, job=PUSHGATEWAY_JOB_NAME, registry=registry, handler=prom_pushgateway_auth_handler)
    pgw_username = env.get("PUSHGATEWAY_USERNAME", False)
    does_pushgateway_has_basic_auth = pgw_username and env.get("PUSHGATEWAY_PASSWORD", False)
     
    if does_pushgateway_has_basic_auth:
        app.log.info(f"Pushing to Prometheus job {PUSHGATEWAY_JOB_NAME} :: {endpoint} :: {region} region :: {elapsed_seconds} sec to server: {PUSHGATEWAY_ENDPOINT} using user: {pgw_username}" ) 
        push_to_gateway(PUSHGATEWAY_ENDPOINT, job=PUSHGATEWAY_JOB_NAME, registry=registry, handler=prom_pushgateway_auth_handler)
    else:
        app.log.info(f"Pushing to Prometheus job {PUSHGATEWAY_JOB_NAME} :: {endpoint} :: {region} region :: {elapsed_seconds} sec to server: {PUSHGATEWAY_ENDPOINT}" ) 
        push_to_gateway(PUSHGATEWAY_ENDPOINT, job=PUSHGATEWAY_JOB_NAME, registry=registry)
    
    
def calculate_latency_to_endpoint(endpoint) :
    result = requests.get(endpoint)
    elapsed_timedelta = result.elapsed
    elapsed_seconds = elapsed_timedelta / timedelta(seconds=1)
    app.log.debug(f"Call time: {endpoint} :: {elapsed_seconds}") 
    region = os.environ.get('AWS_REGION', 'NoRegion')
    labels={"endpoint":endpoint, "instance": region, "region": region}
    response_latency.labels(**labels).observe(elapsed_seconds)
    custom_push_to_gateway(registry, endpoint, region, elapsed_seconds)
    return endpoint, elapsed_seconds

# @app.lambda_function(name='latency-exporter')
# def latency_exporter_lambda_handler(event, context):

def get_lambda_rate_from_env():
    rate_minutes = int(os.environ.get("LAMBDA_RATE_MINUTES", "5"))
    return Rate(rate_minutes, unit=Rate.MINUTES)
    
def latency_exporter():
    PUSHGATEWAY_ENDPOINT = os.environ.get("PUSHGATEWAY_ENDPOINT")
    app.log.debug(f"PUSHGATEWAY_ENDPOINT={PUSHGATEWAY_ENDPOINT}")
    for endpoint in get_endpoints_from_env_var():
        calculate_latency_to_endpoint(endpoint)
    return {"success": True}

@app.schedule(get_lambda_rate_from_env(), name='latency-exporter')
def latency_exporter_lambda_handler(event):
    app.log.debug(f"event: {str(event)}")
    return latency_exporter()


def run_locally():
    os.environ['ENDPOINT_LIST']="https://api.binance.com,https://api-gcp.binance.com,https://api1.binance.com,https://api2.binance.com,https://api3.binance.com,https://api4.binance.com"
    os.environ['PUSHGATEWAY_ENDPOINT']="https://pgw.zabumafu.dev/"
    os.environ['PUSHGATEWAY_USERNAME']="lambda"
    os.environ['PUSHGATEWAY_PASSWORD']="hoplaziplaatbitakla"
    os.environ['AWS_REGION']="abc.local"

    for _ in range(1000):
        print("*********")
        latency_exporter()
        sleep(30)

if __name__ == "__main__":
    run_locally()    
