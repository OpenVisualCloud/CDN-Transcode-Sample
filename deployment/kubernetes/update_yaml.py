#!/usr/bin/python3

import os
import re
import copy
import subprocess
import sys
sys.path.append(sys.argv[1])

import yaml_utils

def ping(host):
    cmd = 'ping -c %d %s'%(1, host)
    p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.read().decode()

    reg_receive = "(\d+) received"
    match_receive = re.search(reg_receive, out)
    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group().split(' ')[0])
    if receive_count > 0:
        return True
    else:
        return False

#input_node_name
def input_node_name(service_name, image_name="sw"):
    global hw_node_name_list

    node_name_list = sw_node_name_list

    if image_name == "hw":
        node_name_list = hw_node_name_list

    if node_num == 1:
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

    if image_name == "hw":
        hw_node_name_list.remove(node_name)

    return node_name

node_num = int(os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
print("There are " + str(node_num) + " kubernetes nodes on your host server!!!")

if node_num == 0:
    os._exit(0)

sw_node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
sw_node_name_list = list(filter(None, sw_node_name_list))
hw_node_name_list = copy.deepcopy(sw_node_name_list)

if node_num > 1:
    nfs_server = input("Please input where the video clips server is ([NFS server IP address]):")
    while True:
        if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
            if not ping(nfs_server):
               nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([NFS server IP address]):")
               continue
            cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
            while True:
                if not os.path.isabs(cdn_directory):
                    cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
                else:
                    if re.match(".+/$", cdn_directory):
                        cdn_directory = cdn_directory[:-1]
                    break
            break
        else:
            nfs_server = input("Input error, Please input where the video clips server is again ([NFS server IP address]):")
else:
    nfs_server = input("Please input where the video clips server is ([localhost] or [NFS server IP address]):")
    while True:
        if nfs_server == "localhost":
           cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
           while True:
               if not (os.path.isdir(cdn_directory) and os.path.isabs(cdn_directory)):
                   cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
               else:
                   if re.match(".+/$", cdn_directory):
                       cdn_directory = cdn_directory[:-1]
                   break
           break
        elif re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
            if not ping(nfs_server):
               nfs_server = input("Can't ping your NFS server IP address, Please input where the video clips server is again ([localhost] or [NFS server IP address]):")
               continue
            cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
            while True:
                if not os.path.isabs(cdn_directory):
                    cdn_directory = input("Please input CDN-Transcode-Sample directory path:")
                else:
                    if re.match(".+/$", cdn_directory):
                        cdn_directory = cdn_directory[:-1]
                    break
            break
        else:
            nfs_server = input("Input error, Please input where the video clips server is again ([localhost] or [NFS server IP address]):")

#zookeeper
node_name = input_node_name("zookeeper service")

yaml_file = sys.argv[1] + "/zookeeper-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
yaml_utils.dump_yaml_file(data, yaml_file)

# kafka
node_name = input_node_name("kafka service")

yaml_file = sys.argv[1] + "/kafka-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
yaml_utils.dump_yaml_file(data, yaml_file)

# cdn
node_name = input_node_name("cdn service")

yaml_file = sys.argv[1] + "/cdn-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
data = yaml_utils.add_volumeMounts(data, True)
data = yaml_utils.add_volumes(data, nfs_server, True, cdn_directory)
yaml_utils.dump_yaml_file(data, yaml_file)

node_port = 443
yaml_file = sys.argv[1] + "/cdn-service-service.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.set_nodePort(data, node_port)
yaml_utils.dump_yaml_file(data, yaml_file)

#vod transcode
yaml_file = sys.argv[1] + "/vod-transcode-service-0-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.add_volumeMounts(data, False)
data = yaml_utils.add_volumes(data, nfs_server, False, cdn_directory)
i = 0
while True:
    if len(hw_node_name_list) > 0:
        image_name = input("Please choose the transcode mode of the vod transcode server ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
        while True:
            if image_name.lower() == "sw" or  image_name.lower() == "hw":
                break
            else:
                image_name = input("Please choose the transcode mode of the vod transcode server again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
    else:
        image_name = "sw"
    node_name = input_node_name("vod transcode", image_name.lower())

    data = yaml_utils.update_imageName(data, image_name.lower(), False)
    data = yaml_utils.update_nodeSelector(data, node_name)
    service_name = "vod-transcode-service-" + str(i)
    data = yaml_utils.update_service_name(data,service_name)

    if i == 0:
        fileName = yaml_file
    else:
        fileName = yaml_file.rsplit("0")[0] + str(i) + "-deployment.yaml"

    yaml_utils.dump_yaml_file(data, fileName)
    i += 1
    create_node = input("Do you still need to deploy the vod transcode service? ([y] or [n]):")
    while True:
        if create_node.lower() == "y" or create_node.lower() == "n":
            break
        else:
            create_node = input("Input error, Do you still need to deploy the vod transcode service? ([y] or [n]):")
    if create_node.lower() == "n":
        break

#live_transcode
yaml_file = sys.argv[1] + "/live-transcode-service-0-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.add_volumeMounts(data, False)
data = yaml_utils.add_volumes(data, nfs_server, False, cdn_directory)
i = 0
while True:
    if len(hw_node_name_list) > 0:
        image_name = input("Please choose the transcode mode of the live transcode service ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
        while True:
            if image_name.lower() == "sw" or  image_name.lower() == "hw":
                break
            else:
                image_name = input("Please choose the transcode mode of the live transcode service again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
    else:
        image_name = "sw"
    node_name = input_node_name("live transcode", image_name.lower())

    data = yaml_utils.update_imageName(data, image_name.lower(), False)
    data = yaml_utils.update_command(data, image_name.lower(), i)
    data = yaml_utils.update_nodeSelector(data, node_name)
    service_name = "live-transcode-service-" + str(i)
    data = yaml_utils.update_service_name(data,service_name)

    if i == 0:
        fileName = yaml_file
    else:
        fileName = yaml_file.rsplit("0")[0] + str(i) + "-deployment.yaml"

    yaml_utils.dump_yaml_file(data, fileName)
    i += 1
    create_node = input("Do you still need to deploy the live transcode service? ([y] or [n]):")
    while True:
        if create_node.lower() == "y" or create_node.lower() == "n":
            break
        else:
            create_node = input("Do you still need to deploy the live transcode service? ([y] or [n]):")
    if create_node.lower() == "n":
        break
