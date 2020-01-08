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


def get_node_num():
    node_num = int(os.popen(
        "kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
    if node_num == 0:
        print("Error, no nodes were found, please check environment!!!")
        os._exit(1)
    print("There are " + str(node_num) +
          " kubernetes nodes on your host server!!!")
    return node_num

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

def input_request_cpu(service_name, node_dict, pods_dict):
    cpu_quota = input("Please input run " +
                      service_name + " request cpu core number: ")
    while True:
        if re.match(r"\d{1,2}(\.\d+)?$", cpu_quota) and node_dict[pods_dict[service_name]["node"]]["cpu"] > float(cpu_quota) > 0:
            node_dict[pods_dict[service_name]
                      ["node"]]["cpu"] -= float(cpu_quota)
            pods_dict[service_name]["cpu"] = float(cpu_quota)
            break
        else:
            cpu_quota = input("Input error, please input run " +
                              service_name + " request cpu core number again: ")
    return node_dict, pods_dict

def input_request_mem(service_name, node_dict, pods_dict):
    mem_quota = input("Please input run " + service_name +
                      " request memory quota(MiB): ")
    while True:
        if re.match(r"\d{3,5}$", mem_quota) and node_dict[pods_dict[service_name]["node"]]["memory"] > int(mem_quota) > 0:
            node_dict[pods_dict[service_name]["node"]
                      ]["memory"] -= int(mem_quota)
            pods_dict[service_name]["memory"] = int(mem_quota)
            break
        else:
            mem_quota = input("Input error, please input run " +
                              service_name + " request memory quota(MiB) again: ")
    return node_dict, pods_dict

def deploy_transcode_cluster(service_name):
    ret = input("Do you need to deploy the " + service_name +
                " transcode service? ([y] or [n]): ")
    while True:
        if ret.lower() == "y":
            configure_transcode_service(service_name)
            break
        elif ret.lower() == "n":
            break
        else:
            ret = input("Input error, do you need to deploy the " +
                        service_name + " transcode service? ([y] or [n]): ")

def configure_live_transcode_args(service_name, deploy_type, image_name):
    if deploy_type == "auto":
        pods_dict[service_name]["input"] = video_list[0]
        pods_dict[service_name]["transcode0"] = {
            'codec': 'AVC', 'protocol': 'HLS', 'resolution': '856:480', 'bitrate': '5', 'output': 'output_name'}
        return

    if len(video_list) == 1:
        input_video = video_list[0]
    else:
        input_video = input(
            "Please choose the one video clip to transcode (" + str(video_list)[1:-1] + "): ")
        while True:
            if input_video in video_list:
                break
            else:
                input_video = input(
                    "Input error, please choose the one video clip to transcode again (" + str(video_list)[1:-1] + "): ")
    pods_dict[service_name]["input"] = input_video

    output_channel = input("Please choose the output channel (1, 2 ,3, 4): ")
    while True:
        if output_channel in ["1", "2", "3", "4"]:
            break
        else:
            output_channel = input(
                "Input error, please choose the output channel again (1, 2 ,3, 4): ")

    output_dict = {}
    protocol_dict = {"a": "HLS", "b": "DASH"}
    protocol_str = ', '.join([("\033[0;31;40m" + key + "\033[0m: " + value)
                              for key, value in protocol_dict.items()])
    resolution_dict = {"a": ["hd480", "856:480"], "b": ["hd720", "1280:720"], "c": [
        "hd1080", "1920:1080"], "d": ["2kqhd", "2560:1440"]}
    resolution_str = ', '.join([("\033[0;31;40m" + key + "\033[0m: " + value[0])
                                for key, value in resolution_dict.items()])
    codec_dict = {"sw": {"AVC": "libx264", "HEVC": "libsvt_hevc",
                         "AV1": "libsvt_av1"}, "hw": {"AVC": "h264_vaapi", "HEVC": "hevc_vaapi"}}

    for i in range(int(output_channel)):
        pods_dict[service_name]["transcode" + str(i)] = {}
        codec = input("Please choose the %dth output encoder (%s): " % (
            i + 1, str(list(codec_dict[image_name].keys()))[1:-1]))
        while True:
            if codec_dict[image_name].get(codec.upper()):
                break
            else:
                codec = input("Input error, please choose the %dth output encoder again (%s): " % (
                    i + 1, str(list(codec_dict[image_name].keys()))[1:-1]))

        pods_dict[service_name]["transcode" + str(i)]["codec"] = codec.upper()

        resolution_key = input(
            "Please choose the %dth output resolution (%s): " % (i + 1, resolution_str))
        while True:
            if resolution_key.lower() in resolution_dict.keys():
                break
            else:
                resolution_key = input(
                    "Input error, please choose the %dth output resolution again(%s): " % (i + 1, resolution_str))

        pods_dict[service_name]["transcode" +
                                str(i)]["resolution"] = resolution_dict[resolution_key.lower()][1]

        bitrate = input(
            "Please enter the %dth output bitrate([1-20]Mbps): " % (i + 1))
        while True:
            if re.match(r"(([1-9])|(1\d))$", bitrate):
                break
            else:
                bitrate = input(
                    "Input error, please enter the %dth output bitrate again([1-20]Mbps): " % (i + 1))

        pods_dict[service_name]["transcode" + str(i)]["bitrate"] = bitrate

        protocol_key = input(
            "Please choose the %dth output streaming media communication protocol(%s): " % (i + 1, protocol_str))
        while True:
            if protocol_key.lower() in protocol_dict.keys():
                break
            else:
                protocol_key = input(
                    "Input error, please choose the %dth output streaming media communication protocol again (%s): " % (i + 1, protocol_str))

        pods_dict[service_name]["transcode" +
                                str(i)]["protocol"] = protocol_dict[protocol_key.lower()]

        output_name = input(
            "Please enter the %dth output video clip name: " % (i + 1))
        while True:
            if re.match(r'^[^\\\s/:\*\?"<>\|]+$', output_name):
                if output_name in output_dict.keys():
                    output_name = input(
                        "The output video clip name already exists, please enter the %dth output video clip name again: " % (i + 1))
                else:
                    break
            else:
                output_name = input(
                    "Input error, please enter the %dth output video clip name again: " % (i + 1))
        pods_dict[service_name]["transcode" + str(i)]["output"] = output_name
    return

def configure_transcode_service(service_name):
    global hw_node_num

    i = 0
    while True:
        service_name_index = re.search(
            "((vod)|(live))(\d*)", service_name).group(1) + str(i)
        pods.append(service_name_index)
        pods_dict[service_name_index] = {}
        if hw_node_num > 0:
            image_name = input("Please choose the transcode mode of the " + str(i) + "th" + service_name +
                               " ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5): ")
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
            deploy_type = input(
                "Do you need to deploy live-transcode-service by customizing parameters([y] or [n]): ")
            while True:
                if deploy_type.lower() == "y":
                    deploy_type = "manual"
                    break
                elif deploy_type.lower() == "n":
                    deploy_type = "auto"
                    break
                else:
                    deploy_type = input(
                        "Input error, do you need to deploy live-transcode-service by customizing parameters([y] or [n]): ")

            configure_live_transcode_args(
                service_name_index, deploy_type, image_name.lower())

        i += 1
        create_node = input("Do you still need to deploy the " +
                            str(i + 1) + "th " + service_name + "? ([y] or [n]): ")
        while True:
            if create_node.lower() == "y" or create_node.lower() == "n":
                break
            else:
                create_node = input("Input error, do you still need to deploy the " +
                                    str(i + 1) + "th " + service_name + "? ([y] or [n]): ")
        if create_node.lower() == "n":
            break

def get_node_information():
    node_dict = {}
    basic_info = os.popen("kubectl describe node").read()
    index_list = [i.start() for i in re.finditer("Name:", basic_info)]
    for i in range(len(index_list)):
        cpu_info = re.findall(
            "(\d+)", os.popen("kubectl describe node | awk -F ' ' '$1==\"cpu\"' |awk 'NR==" + str(i+1) + "'").read())
        memory_info = re.findall(
            "(\d+)", os.popen("kubectl describe node | awk -F ' ' '$1==\"memory\" {print $0}'").read())
        cpu = int(int(re.search(
            "cpu:\s+(\d+)", basic_info[index_list[i]: -1]).group(1)) - int(cpu_info[0])/1000)
        memory = int((int(re.search(
            "memory:\s+(\d+)", basic_info[index_list[i]: -1]).group(1)) / 1024 - int(memory_info[0])))
        if cpu > 0 and memory > 0:
            node_dict[re.search("Name:\s+(.+)", basic_info[index_list[i]: -1]
                                ).group(1)] = {"cpu": cpu, "memory": memory}
    return node_dict


node_num = get_node_num()

sw_node_name_list = os.popen(
    "kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
sw_node_name_list = list(filter(None, sw_node_name_list))
hw_node_name_list = copy.deepcopy(sw_node_name_list)
hw_node_num = len(hw_node_name_list)
nfs_server, volume_directory, video_list = configure_basic_module(node_num)

pods_dict = {"cdn": {}, "redis": {}, "zookeeper": {}, "kafka": {}}
node_dict = get_node_information()
pods = ["cdn", "redis", "zookeeper", "kafka"]

deploy_transcode_cluster("vod")
deploy_transcode_cluster("live")

for pod in pods:
    pods_dict = input_node_name(pod, pods_dict)
    node_dict, pods_dict = input_request_cpu(pod, node_dict, pods_dict)
    node_dict, pods_dict = input_request_mem(pod, node_dict, pods_dict)

update_yaml.update_yaml(nfs_server, volume_directory, sys.argv[1],
                        pods, pods_dict, get_node_information())
