

- Get a debian 12 vm
- https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/


```bash
sudo su

apt update -y 
apt upgrade -y 

apt-get install -y apt-transport-https software-properties-common wget

mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | tee /etc/apt/keyrings/grafana.gpg > /dev/null




echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee -a /etc/apt/sources.list.d/grafana.list

# Updates the list of available packages
apt-get update -y
# Installs the latest OSS release:
apt-get install -y grafana 

 sudo /bin/
 sudo /bin/systemctl enable grafana-server
### You can start grafana-server by executing
 sudo /bin/systemctl start grafana-server

systemctl daemon-reload
systemctl enable grafana-server --now
systemctl status grafana-server


# get ip addr
ip a | grep inet
```