#!/usr/bin/python3

import yaml_utils
import update_yaml
import os
import re
import copy
import subprocess
import sys
import socket
import functools
sys.path.append(sys.argv[1])

def ping(host):
    cmd = 'ping -c %d %s' % (1, host)
    p = subprocess.Popen(args=cmd, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

def get_volume_directory(nfs_server, is_localhost):
    video_list = []

    if is_localhost:
        volume_directory = os.path.dirname(os.path.dirname(sys.argv[1]))

        for i in os.listdir(os.path.join(volume_directory, "volume/video/archive")):
            if os.path.splitext(i)[1] == '.mp4':
                video_list.append(i)
        return volume_directory, video_list

    volume_directory = input(
        "Please input CDN-Transcode-Sample volume directory path on NFS server: ")
    while True:
        if not os.path.isabs(volume_directory):
            volume_directory = input(
                "Input error, please input CDN-Transcode-Sample volume directory path on NFS server again: ")
        else:
            if re.match(".+/$", volume_directory):
                volume_directory = volume_directory[:-1]
            break

    username = input("Please input NFS server username: ")
    while True:
        if re.match(r"[^\s]+$", username):
            exec_cmd = os.popen("fab -u %s -H %s -- 'ls %s'" % (username, nfs_server,
                                                                os.path.join(volume_directory, "volume/video/archive")))
            result = [re.findall(r'[^\\\s/:\*\?"<>\|]+', i)
                      for i in re.findall(r'out:(.+)\n', exec_cmd.read())]
            video_list = [i for i in functools.reduce(
                lambda x, y:x+y, result) if os.path.splitext(i)[1] == '.mp4']
            break
        else:
            username = input(
                "Input error, please input NFS server username again: ")
    return volume_directory, video_list

def configure_basic_module(node_num):
    if node_num > 1:
        nfs_server = input(
            "Please input where the video clips server is ([NFS server IP address]): ")
        while True:
            if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$", nfs_server):
                if not ping(nfs_server):
                    nfs_server = input(
                        "Can't ping your NFS server ip address, please input where the video clips server is again ([NFS server IP address]): ")
                    continue
                volume_directory, video_list = get_volume_directory(
                    nfs_server, False)
                break
            else:
                nfs_server = input(
                    "Input error, please input where the video clips server is again ([NFS server IP address]): ")
    else:
        nfs_server = input(
            "Please input where the video clips server is ([localhost] or [NFS server IP address]): ")
        while True:
            if nfs_server == "localhost":
                volume_directory, video_list = get_volume_directory(
                    nfs_server, True)
                break
            elif re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))", nfs_server):
                if not ping(nfs_server):
                    nfs_server = input(
                        "Can't ping your NFS server IP address, please input where the video clips server is again ([localhost] or [NFS server IP address]): ")
                    continue
                volume_directory, video_list = get_volume_directory(
                    nfs_server, False)
                break
            else:
                nfs_server = input(
                    "Input error, please input where the video clips server is again ([localhost] or [NFS server IP address]): ")
    if not video_list:
        print("\033[0;31;40mNo video clips were found!!!\033[0m")
        os._exit(1)
    return nfs_server, volume_directory, video_list

def input_node_name(service_name, pods_dict, image_name="sw"):
    node_name_list = sw_node_name_list

    if image_name == "hw":
        node_name_list = hw_node_name_list

    if node_num == 1:
        node_name = node_name_list[0]
    else:
        node_name = input("Please input run " + service_name +
                          " node name (" + str(node_name_list)[1:-1] + "): ")
        while True:
            if node_name == "":
                node_name = node_name_list[0]
            if node_name in node_name_list:
                break
            else:
                node_name = input("Input error, please input run " + service_name +
                                  " node name again (" + str(node_name_list)[1:-1] + "): ")

    if image_name == "hw":
        hw_node_name_list.remove(node_name)

    pods_dict[service_name]["node"] = node_name
    return pods_dict

def input_request_cpu(service_name, node_dict, pods_dict, cpu_quota):
    if re.match(r"\d{1,2}(\.\d+)?$", cpu_quota) and node_dict[pods_dict[service_name]["node"]]["cpu"] > float(cpu_quota) > 0:
        node_dict[pods_dict[service_name]
                  ["node"]]["cpu"] -= float(cpu_quota)
        pods_dict[service_name]["cpu"] = float(cpu_quota)
    else:
        print("Error: Overload! Pleaes redistribute cpu request in cpu_mem_managerment.cfg")
        os._exit()
    return node_dict, pods_dict

def input_request_mem(service_name, node_dict, pods_dict, mem_quota):
    if re.match(r"\d{3,5}$", mem_quota) and node_dict[pods_dict[service_name]["node"]]["memory"] > int(mem_quota) > 0:
        node_dict[pods_dict[service_name]["node"]
                  ]["memory"] -= int(mem_quota)
        pods_dict[service_name]["memory"] = int(mem_quota)
    else:
        print("Error: Overload! Pleaes redistribute memory request in cpu_mem_managerment.cfg")
        os._exit()
    return node_dict, pods_dict

def configure_live_transcode_args(service_name, num, trans_cfg_dict, image_name):
    pods_dict[service_name]["input"] = trans_cfg_dict[service_name]['url']
    for trans_num in range(int(trans_cfg_dict[service_name]['density'])):
        pods_dict[service_name]["transcode" + str(trans_num)] = {
        'codec': trans_cfg_dict[service_name]['encoder_type'], 'protocol': trans_cfg_dict[service_name]['protocol'], 'resolution': trans_cfg_dict[service_name]['width_height'], 'bitrate': trans_cfg_dict[service_name]['bitrate'], 'framerate':trans_cfg_dict[service_name]['framerate'], 'gop': trans_cfg_dict[service_name]['gop'], 'maxbFrames': trans_cfg_dict[service_name]['maxbframes'], 'refsNum': trans_cfg_dict[service_name]['refsnum'], 'preset': trans_cfg_dict[service_name]['preset'], 'output': 'output_name'}
    return

def configure_transcode_service(service_name, num, trans_cfg_dict):
    global hw_node_num

    for i in range(int(num)):
       service_name_index = re.search(
           "((vod)|(live))(\d*)", service_name).group(1) + str(i)
       pods.append(service_name_index)
       pods_dict[service_name_index] = {}
       if hw_node_num > 0:
           if trans_cfg_dict[service_name_index]['hwaccel'] == 'true':
               image_name = "hw"
           elif trans_cfg_dict[service_name_index]['hwaccel'] == 'false':
               image_name = "sw"
           while True:
               if image_name.lower() == "sw" or image_name.lower() == "hw":
                   hw_node_num -= 1 if image_name.lower() == "hw" else 0
                   break
               else:
                   image_name = input("Input error, please choose the transcode mode of the " + str(i) + "th" + service_name +
                                      " again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5): ")
       else:
           image_name = "sw"
       pods_dict[service_name_index]["mode"] = image_name

       if re.search("live\d+", service_name_index):
           configure_live_transcode_args(
               service_name_index, num, trans_cfg_dict, image_name.lower())

def get_node_information(description):
    node_dict={}
    for line in description.split("\n"):
        fields=line.split()
        if fields[2].endswith("Ki"): memory=int(fields[2][:-2])/1024
        if fields[2].endswith("Mi"): memory=int(fields[2][:-2])
        if fields[2].endswith("Gi"): memory=int(fields[2][:-2])*1024
        node_dict[fields[0]]={ "cpu": int(fields[1]), "memory": int(memory) }
    return node_dict

def get_config(config_file):
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    config_dict = dict(config._sections)
    for k in config_dict:
        config_dict[k] = dict(config_dict[k])
    return config_dict

sw_node_name_list = sys.argv[4].split(" ")
node_num=len(sw_node_name_list)
sw_node_name_list = list(filter(None, sw_node_name_list))
hw_node_name_list = copy.deepcopy(sw_node_name_list)
hw_node_num = len(hw_node_name_list)
nfs_server, volume_directory, video_list = configure_basic_module(node_num)

pods_dict = {"cdn": {}, "redis": {}, "zookeeper": {}, "kafka": {}}
node_dict = get_node_information(sys.argv[5])
pods = ["cdn", "redis", "zookeeper", "kafka"]

DIRS = sys.argv[1]
NVODS = sys.argv[2]
NLIVES = sys.argv[3]
NNODES = sys.argv[4]
NODE_DESCRIPTION = sys.argv[5]

live_transcode_cfg = DIRS + '/live-transcode.cfg'
vod_transcode_cfg = DIRS + '/vod-transcode.cfg'
cpu_mem_cfg = DIRS + '/cpu_mem_managerment.cfg'
live_trans_cfg_dict = get_config(live_transcode_cfg)
vod_trans_cfg_dict = get_config(vod_transcode_cfg)
cpu_mem_cfg_dict = get_config(cpu_mem_cfg)
trans_cfg_dict = {**live_trans_cfg_dict, **vod_trans_cfg_dict}

configure_transcode_service("vod", NVODS, vod_trans_cfg_dict)
configure_transcode_service("live", NLIVES, live_trans_cfg_dict)

for pod in pods:
    pods_dict = input_node_name(pod, pods_dict)
    node_dict, pods_dict = input_request_cpu(pod, node_dict, pods_dict, cpu_mem_cfg_dict[pod]['cpu'])
    node_dict, pods_dict = input_request_mem(pod, node_dict, pods_dict, cpu_mem_cfg_dict[pod]['mem'])

update_yaml.update_yaml(nfs_server, volume_directory, sys.argv[1], pods, pods_dict, get_node_information(),trans_cfg_dict)
