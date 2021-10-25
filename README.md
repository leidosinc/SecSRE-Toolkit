# SecSRE-Toolkit

## Objective

Install, deploy and configure secure SRE-enabling tools that meet security standards. 

## Current SRE Tools included

### Grafana 
Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources. 

### Prometheus

Prometheus is a free software application used for event monitoring and alerting. It records real-time metrics in a time series database built using a HTTP pull model, with flexible queries and real-time alerting.

### Kibana

Kibana is a data visualization and exploration tool used for log and time-series analytics, application monitoring, and operational intelligence use cases. It offers powerful and easy-to-use features such as histograms, line graphs, pie charts, heat maps, and built-in geospatial support. Also, it provides tight integration with Elasticsearch, a popular analytics and search engine, which makes Kibana the default choice for visualizing data stored in Elasticsearch.

#### Node Exporter

Node Exporter is a Prometheus exporter for server level and OS level metrics with configurable metric collectors. It helps us in measuring various server resources such as RAM, disk space, and CPU utilization. Node exporter is a good solution to collect all the Linux server related metrics and statistics for monitoring.

## Security Configuration Tools Used

### Nginx

A web server used as a reverse proxy for authentication.

### Flask

Flask is a micro web framework written in Python that allows us to authenticate certificates via HTTPS.

## Requirements
* 	RPM-based Linux system
* 	RPMs for tools (grafana, prometheus, Nginx, node exporter, flask, python)

## Download Python packages
Before running the playbook, download the required python packages into files/pip:  
```
cd files/pip
python3 -m pip download -r requirements.txt
```  

## Run command
`sudo ansible-playbook –i inventory main.yaml`
