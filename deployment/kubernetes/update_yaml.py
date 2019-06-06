#!/usr/bin/python3

import os
import re
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
def input_node_name(service_name):
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
    return node_name

node_num = int(os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
print("There are " + str(node_num) + " kubernetes nodes on your host server!!!")

if node_num == 0:
    os._exit(0)

node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
node_name_list = list(filter(None, node_name_list))

if node_num > 1:
    nfs_server = input("Please input where the video clips server is ([remote NFS server ip adress]):")
    while True:
        if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
            if not ping(nfs_server):
               nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([remote NFS server ip adress]):")
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
            nfs_server = input("Input error, Please input where the video clips server is again ([remote NFS server ip adress]):")
else:
    nfs_server = input("Please input where the video clips server is ([localhost] or [remote NFS server ip adress]):")
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
               nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([localhost] or [remote NFS server ip adress]):")
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
            nfs_server = input("Input error, Please input where the video clips server is again ([localhost] or [remote NFS server ip adress]):")

#zookeeper
node_name = input_node_name("zookeeper")

yaml_file = sys.argv[1] + "/zookeeper-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

# kafka
node_name = input_node_name("kafka")

yaml_file = sys.argv[1] + "/kafka-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

# cdn
node_name = input_node_name("cdn")

yaml_file = sys.argv[1] + "/cdn-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, True)
yaml_utils.add_volumes(data, yaml_file, nfs_server, True, cdn_directory)

node_port = 443

yaml_file = sys.argv[1] + "/cdn-service-service.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.set_nodePort(data, yaml_file, node_port)

#vod transcode
node_name = input_node_name("vod transcode")

image_name = input("Please choose the transcode mode of the vod transcode server ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server again ([hw]: hardware is for E3/VCA2or [sw]: software is for E5):")

yaml_file = sys.argv[1] + "/vod-transcode-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_imageName(data, yaml_file, image_name.lower(), True)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, False)
yaml_utils.add_volumes(data, yaml_file, nfs_server, False, cdn_directory)

if image_name.lower() == "hw":
    node_name_list.remove(node_name)

#live_transcode
node_name = input_node_name("live transcode")

image_name = input("Please choose the transcode mode of the live transcode server ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")

yaml_file = sys.argv[1] + "/live-transcode-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_imageName(data, yaml_file, image_name.lower(), False)
yaml_utils.update_command(data, yaml_file, image_name.lower())
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, False)
yaml_utils.add_volumes(data, yaml_file, nfs_server, False, cdn_directory)
