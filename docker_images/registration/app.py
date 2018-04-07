import docker

print('Connecting...')

#client = docker.DockerClient(base_url='unix://tmp/docker.sock')
client = docker.from_env()

print('...connected')

for event in client.events():
    print(event)



# @docker_events.start.subscribe
# def set_skydns_record(client, docker_event, config):
#     # get ip of container
#     container = client.inspect_container(docker_event['id'])

#     container_name = container['Name'].strip("/")

#     print container
# #--volume=/var/run/docker.sock:/tmp/docker.sock