#import boto.ec2
import boto3
import string, sys
import os
import ssl

def usage():
   print ("Usage: get-test-instance-ip.py <INSTANCE_NAME>")
   exit(1)

#print(len(sys.argv)

if len(sys.argv) != 2:
    usage()

instance_name = sys.argv[1]

#print ("Connecting to AWS...")
client = boto3.client('ec2', region_name='us-east-1')
filters=[{'Name':'tag:Name','Values':[instance_name]}]
instance_ids = client.describe_instances(Filters=filters)['Reservations']
#print(str(len(instance_ids))+" instances with tag:Name="+instance_name+" found")
#print(instance_ids[0])
if len(instance_ids) > 1:
        sys.exit("multiple test instances with name "+instance_name+" found.  You need to pick one, rename others, and restart this Jenkins task")
if len(instance_ids) == 0:
        sys.exit("no test instances available")
else:
        target_instanceId = instance_ids[0]['Instances'][0]['InstanceId']
        test_host = instance_ids[0]['Instances'][0]['PrivateIpAddress']
#       print ("single test instance "+target_instanceId+" found with IPaddress= "+test_host)
        test_instance_cert = ssl.get_server_certificate((test_host, 8080))
#       print(test_instance_cert)
        text_file = open("test_instance_cert.pem", "w")
        n = text_file.write(test_instance_cert)
        text_file.close()
        os.system('rm -f ./pki/cacerts')
        os.system('keytool -noprompt -importcert -keystore ./pki/cacerts -file test_instance_cert.pem -storepass changeit 2> /dev/null')
        #sys.exit(test_host)
        print(test_host)
