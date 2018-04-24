import json
import os
import pprint
import sys

import docker
import requests

pp = pprint.PrettyPrinter(indent=4)

print('Connecting...')
env = dict(
    DOCKER_TLS_VERIFY="1",
    DOCKER_HOST="tcp://192.168.99.100:2376",
    DOCKER_CERT_PATH="/Users/rich/.minikube/certs",
    DOCKER_API_VERSION="1.23"
)


TRACKED_EVENTS = ['start', 'stop']
SYSTEM_NAMESPACES = ['kube-system', 'default', 'kube-public']
ENDPOINT = 'http://localhost:8000/webhooks/event'

TENSES = {
    'start': 'started',
    'stop': 'stopped'
}


def dispatch(event):
    container_attrs = event['Actor']['Attributes']
    if container_attrs['io.kubernetes.docker.type'] != 'podsandbox':
        return
    pp.pprint(container_attrs)
    payload = {
        'event_type': f"POD_{event['Action'].upper()}",
        'cluster_id': container_attrs["it.justcompile.aaas.cluster_id"],
        'data': container_attrs,
        'description': f'{TENSES[event["Action"]].title()} {container_attrs["role"]}'
    }
    pp.pprint(payload)
    # requests.post(ENDPOINT, json=payload)


def main(stream):
    for message in stream:
        event = json.loads(message.strip())
        if event['Type'] != 'container' or event['Action'] not in TRACKED_EVENTS:
            continue
        try:
            namespace = event['Actor']['Attributes']['io.kubernetes.pod.namespace']
            if namespace not in SYSTEM_NAMESPACES:
                dispatch(event)
        except KeyError:
            pass


if __name__ == '__main__':
    docker_client = docker.from_env(environment=env)
    print('...connected')
    event_stream = docker_client.events()
    try:
        main(event_stream)
    except KeyboardInterrupt:
        event_stream.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
