####prepare common/shared resources
###assumes python3 is installed

#get boto3
pip3 install boto3

#install docker (https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)
sudo apt-get remove docker docker-engine docker.io containerd runc
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

#check for a single test instance with the right name,  and create cacerts from it
test_host = `python3 get-test-instance-ip.py TestVPN_appsymphony_ubuntu_test_instance_2.13.0-RELEASE`

#build docker container that creates volume to share cacerts
cd pki
docker build -t pkivolume .
#run docker container to create pki volume /mas/application/.ssl containing cacerts
docker run -d --name examples-pki-volume --mount source=pki-volume,destination=/mas/application/.ssl pkivolume:latest
docker volume ls

#### test each example

#Example 1
cd ../example1
#curl deploy app to docker Example 1
curl --insecure -o  example1image.tar  --location --request GET 'https://${test_host}:9090/repositorymanager/artifacts/com.optensity%3AExample-1---Hello-World%3A3.2.6-RELEASE/image' --header 'Content-Type: application/json' --data-raw '["-Djavax.net.ssl.trustStore=/mas/application/.ssl/cacerts","-Djavax.net.ssl.trustStorePassword=changeit"]'


#docker put resulting image into local repo
docker load < example1image.tar

#docker run example1 with pki volume
sudo docker run --name=example1-test --mount source=pki-volume,destination=/mas/application/.ssl example-1---hello-world:latest