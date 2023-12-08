#!/bin/bash

# Verificar si Nginx está instalado
echo "Verificando si nginx está instalado..."
if ! [ -x "$(command -v nginx)" ]; then
  echo 'nginx no está instalado. Instalando...'
  apt-get install nginx -y
  echo "Se ha instalado Nginx."
else
  echo "Nginx ya está instalado."
fi

# Verificar si Java está instalado
echo "Verificando si Java está instalado..."
if ! [ -x "$(command -v java)" ]; then
  echo 'Java no está instalado. Instalando...'
  apt-get install default-jre -y
  echo "Se ha instalado Java."
else
  echo "Java ya está instalado."
fi

# Obtener la dirección IP de la interfaz de red que se usará
host_ip=$(ip route get 1 | awk '{print $NF;exit}')

# Instalar Elasticsearch
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install -y elasticsearch

# Configurar Elasticsearch
sudo sed -i 's/#network.host: 192.168.0.1/network.host: 0.0.0.0/' /etc/elasticsearch/elasticsearch.yml

# Iniciar Elasticsearch
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch

# Instalar Kibana
sudo apt install -y kibana

# Configurar Kibana
echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users
sudo tee /etc/nginx/sites-available/kibana <<EOF
server {
    listen 80;

    server_name _;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/kibana /etc/nginx/sites-enabled/kibana
sudo nginx -t
sudo systemctl reload nginx

# Iniciar Kibana
sudo systemctl start kibana
sudo systemctl enable kibana

# Instalar Logstash
sudo apt install -y logstash

# Configurar Logstash
sudo tee /etc/logstash/conf.d/02-beats-input.conf <<EOF
input {
  beats {
    port => 5044
  }
}
EOF

sudo tee /etc/logstash/conf.d/30-elasticsearch-output.conf <<EOF
output {
  if [@metadata][pipeline] {
    elasticsearch {
      hosts => ["localhost:9200"]
      manage_template => false
      index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
      pipeline => "%{[@metadata][pipeline]}"
    }
  } else {
    elasticsearch {
      hosts => ["localhost:9200"]
      manage_template => false
      index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    }
  }
}
EOF

sudo systemctl start logstash
sudo systemctl enable logstash

# Instalar Filebeat
sudo apt install -y filebeat

# Configurar Filebeat
sudo sed -i 's/#output.elasticsearch:/output.elasticsearch:/' /etc/filebeat/filebeat.yml
sudo sed -i 's/#hosts: \["localhost:9200"\]/hosts: \["localhost:5044"\]/' /etc/filebeat/filebeat.yml
sudo filebeat modules enable system
sudo filebeat setup --pipelines --modules system
sudo filebeat setup --index-management -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["localhost:9200"]'
sudo filebeat setup -E output.logstash.enabled=false -E output.elasticsearch.hosts=['localhost:9200'] -E setup.kibana.host=localhost:5601

# Iniciar Filebeat
sudo systemctl start filebeat
sudo systemctl enable filebeat

# Mostrar mensaje con la URL de Kibana
echo "La instalación ha finalizado. Puedes acceder a Kibana en la siguiente URL:"
echo "http://${host_ip}/status"
