#!/usr/bin/python3

import os
import sys
sys.path.append(sys.argv[1])

import yaml_utils

#dashboard
master_node_name = os.popen("kubectl get node | awk '{print $1,$3}' | grep -E 'master'").read().split(" ")[0]
yaml_file = sys.argv[1] + "dashboard/monitoring-grafana.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, master_node_name)

yaml_file = sys.argv[1] + "dashboard/heapster.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, master_node_name)

yaml_file = sys.argv[1] + "dashboard/monitoring-influxdb.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, master_node_name)

yaml_file = sys.argv[1] + "dashboard/kubernetes-dashboard.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, master_node_name)
