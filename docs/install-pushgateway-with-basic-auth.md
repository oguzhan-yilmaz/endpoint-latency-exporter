

- Get a debian 12 vm
-
## INSTALL PUSH GATEWAY


```bash
sudo su

apt update -y 
apt upgrade -y 
apt install -y curl apache2-utils


useradd -M -r -s /bin/false pushgateway

# go and find the correct url: https://github.com/prometheus/pushgateway/releases
wget https://github.com/prometheus/pushgateway/releases/download/v1.8.0/pushgateway-1.8.0.linux-amd64.tar.gz 

tar xvfz pushgateway-1.8.0.linux-amd64.tar.gz 
cp pushgateway-1.8.0.linux-amd64/pushgateway /usr/local/bin/

chown pushgateway:pushgateway /usr/local/bin/pushgateway

# generate a password interactively
htpasswd -nBC 10 "" | tr -d ':\n'


PGW_USERNAME='lambda'
PGW_PASSWORD='--copy-your-generated-pass-here--'
mkdir /etc/pushgateway/
cat << EOF >  /etc/pushgateway/web.config
basic_auth_users:
  $PGW_USERNAME: $PGW_PASSWORD 
EOF
cat /etc/pushgateway/web.config


# add systemd service

cat << EOF >  /etc/systemd/system/pushgateway.service
[Unit]
Description=Prometheus Pushgateway
Wants=network-online.target
After=network-online.target

[Service]
User=pushgateway
Group=pushgateway
Type=simple
ExecStart=/usr/local/bin/pushgateway --web.config.file /etc/pushgateway/web.config

[Install]
WantedBy=multi-user.target
EOF

cat /etc/systemd/system/pushgateway.service

systemctl enable pushgateway --now

systemctl start pushgateway

systemctl status pushgateway

# test the pushgateway
curl -U "$PGW_USERNAME:$PGW_PASSWORD" localhost:9091/metrics

# get ip addr
ip a | grep inet
```



## INSTALL PROMETHEUS

```bash
sudo su

apt update -y 
apt upgrade -y 
apt install prometheus


cat << EOF >  /etc/default/prometheus
ARGS="--web.config.file=/etc/pushgateway/web.config"
EOF
cat /etc/default/prometheus

systemctl enable prometheus --now
```