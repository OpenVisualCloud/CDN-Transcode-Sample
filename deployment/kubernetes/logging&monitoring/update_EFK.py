#!/usr/bin/python3

import os
import sys
sys.path.append(sys.argv[1])
sys.path.append(sys.argv[1] + "../")
import yaml_utils

def input_node_name(service_name):
    if len(node_name_list) == 1:
        node_name = node_name_list[0]
    else:
        node_name = input("Please input run " + service_name + " node name (" + str(node_name_list)[1:-1] + "):")
        while True:
            if node_name == "":
                node_name = node_name_list[0]
            if node_name in node_name_list:
                break
            else:
                node_name = input("Error, please input run " + service_name + " node name again (" + str(node_name_list)[1:-1] + "):")
    return node_name

def elasticsearch_config(node_name):
    data = yaml_utils.load_yaml_file(yaml_file)
    data = yaml_utils.update_nodeSelector(data, node_name)
    data = yaml_utils.update_service_name(data, service_name + "-" + str(i))
    fileName = yaml_file.rsplit(".")[0] + "-" + str(i) + ".yaml"
    yaml_utils.dump_yaml_file(data, fileName)
    print("The elasticsearch-" + str(i) + " service deployment done!")

master_node_name = os.popen("kubectl get node | awk '{print $1,$3}' | grep -E 'master'").read().split(" ")[0]
node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
node_name_list = list(filter(None, node_name_list))

#kibana
yaml_file = sys.argv[1] + "kibana-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, master_node_name)
data["spec"]["template"]["spec"]["volumes"][1]["hostPath"]["path"] = sys.argv[1] + "config"
yaml_utils.dump_yaml_file(data, yaml_file)

#elasticsearch
service_name = "elasticsearch-service"
yaml_file = sys.argv[1] + "elasticsearch.yml"
i = 0
if len(node_name_list) == 0:
    print("Not found nodes!!!")
    os._exit(1)
else:
    node_name = input_node_name(service_name)
    elasticsearch_config(node_name)
