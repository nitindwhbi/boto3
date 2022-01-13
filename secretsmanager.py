import boto3
import json
import base64
from botocore.exceptions import ClientError


def get_secret(secret_name,region_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
            print (e)
    else:
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
        else:
            secret = json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))
    return secret


#v_secret = get_secret('mysecretid','us-east-1')
#print (v_secret)
#print (v_secret['host'])
