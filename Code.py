import docker
import subprocess
client = docker.from_env()

client.swarm.init() 

node = client.nodes.list()
attr = node[0].attrs
Created_Date = attr['CreatedAt']
Name = attr['Description']['Hostname']
ID = attr['ID']

ipam_pool = docker.types.IPAMPool(subnet='10.10.10.2/24', gateway='10.10.10.1',iprange='10.10.10.2/24')
ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
client.networks.create("se443_test_net", driver = "overlay", scope = "global", attachable = True,ipam=ipam_config )

subprocess.run(["docker","service","create","--name","broker","--replicas","3","--restart-condition","any","--network=se443_test_net","--mount","type=bind,source=/Users/sarahalsh/Desktop/MQTT/mosquitto.conf,destination=/mosquitto/config/mosquitto.conf","eclipse-mosquitto:latest"]) 

Sub = client.services.create("efrecon/mqtt-client",["sub","-h","10.10.10.4","-p","1883","-t","alfaisal_uni", "-v"],networks=['se443_test_net'],name = "subscriber")
Sub.scale(replicas = 3)


Pub = client.services.create("efrecon/mqtt-client",["pub","-h","10.10.10.4","-p","1883","-t","alfaisal_uni","-m","Sarah Alshaghroud 201520"],networks=['se443_test_net'], name= "publisher")
Pub.scale(replicas = 3)

print("\n")
print("Swarm Details: \n")
print("--> Host Name: "+Name+"\n--> ID: "+ ID+"\n--> Created At: "+ Created_Date )


print("\n")
print("Publisher's \nID, Name, Date of creation")
pub = subprocess.call('./pub-info.sh')
print("\n")


print("Subscriber's \nID, Name, Date of creation")
sub = subprocess.call('./sub-info.sh')
print("\n")

subprocess.call('./test.sh')