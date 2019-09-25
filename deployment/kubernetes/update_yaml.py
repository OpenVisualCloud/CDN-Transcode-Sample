#!/usr/bin/python3

import os
import re
import copy
import subprocess
import sys
import socket
import functools
sys.path.append(sys.argv[1])

import yaml_utils

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    finally:
        s.close()
    return host_ip

def get_node_num():
    node_num = int(os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
    if node_num == 0:
        print("Error, no nodes were found, please check environment!!!")
        os._exit(1)
    print("There are " + str(node_num) + " kubernetes nodes on your host server!!!")
    return node_num

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

def get_live_video_URL(host_ip, live_args_list):
    if not live_args_list:
        return
    print("\n\033[0;31;40mThe live video playlist URL are below:\033[0m")
    for i in range(len(live_args_list)):
        for key, value in live_args_list[i]['output_dict'].items():
            if value[0] == "hls":
                extension = "m3u8"
            else:
                extension = "mpd"
            print("\033[0;31;40mhttps://%s/%s/%s_%s/index.%s\033[0m" % (host_ip, value[0], key, str(i), extension))
    print("\n")

def get_volume_directory(nfs_server, is_localhost):
    video_list = []

    if is_localhost:
        volume_directory = os.path.dirname(os.path.dirname(sys.argv[1]))
        for i in os.listdir(os.path.join(volume_directory, "volume/video/archive")):
            if os.path.splitext(i)[1] == '.mp4':
                video_list.append(i)
        return volume_directory, video_list

    volume_directory = input("Please input CDN-Transcode-Sample volume directory path on NFS server: ")
    while True:
        if not os.path.isabs(volume_directory):
            volume_directory = input("Input error, please input CDN-Transcode-Sample volume directory path on NFS server again: ")
        else:
            if re.match(".+/$", volume_directory):
                volume_directory = volume_directory[:-1]
            break

    username = input("Please input NFS server username: ")
    while True:
        if re.match(r"[^\s]+$", username):
            exec_cmd = os.popen("fab -u %s -H %s -- 'ls %s'" % (username, nfs_server, os.path.join(volume_directory, "volume/video/archive")))
            result = [re.findall(r'[^\\\s/:\*\?"<>\|]+', i) for i in re.findall(r'out:(.+)\n', exec_cmd.read())]
            video_list = [i for i in functools.reduce(lambda x,y:x+y, result)  if os.path.splitext(i)[1] == '.mp4']
            break
        else:
            username = input("Input error, Please input NFS server username again: ")
    return volume_directory, video_list

def configure_basic_module(node_num):
    if node_num > 1:
        nfs_server = input("Please input where the video clips server is ([NFS server IP address]): ")
        while True:
            if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
                if not ping(nfs_server):
                   nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([NFS server IP address]): ")
                   continue
                volume_directory, video_list = get_volume_directory(nfs_server, False)
                break
            else:
                nfs_server = input("Input error, Please input where the video clips server is again ([NFS server IP address]): ")
    else:
        nfs_server = input("Please input where the video clips server is ([localhost] or [NFS server IP address]): ")
        while True:
            if nfs_server == "localhost":
                volume_directory, video_list = get_volume_directory(nfs_server, True)
                break
            elif re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
                if not ping(nfs_server):
                   nfs_server = input("Can't ping your NFS server IP address, Please input where the video clips server is again ([localhost] or [NFS server IP address]): ")
                   continue
                volume_directory, video_list = get_volume_directory(nfs_server, False)
                break
            else:
                nfs_server = input("Input error, Please input where the video clips server is again ([localhost] or [NFS server IP address]): ")
    if not video_list:
        print("\033[0;31;40mNo video clips were found!!!\033[0m")
        os._exit(1)
    return nfs_server, volume_directory, video_list

def input_node_name(service_name, image_name="sw"):
    global hw_node_name_list

    node_name_list = sw_node_name_list

    if image_name == "hw":
        node_name_list = hw_node_name_list

    if node_num == 1:
        node_name = node_name_list[0]
    else:
        node_name = input("Please input run " + service_name + " node name (" + str(node_name_list)[1:-1] + "): ")
        while True:
            if node_name == "":
                node_name = node_name_list[0]
            if node_name in node_name_list:
                break
            else:
                node_name = input("Error, please input run " + service_name + " node name again (" + str(node_name_list)[1:-1] + "): ")

    if image_name == "hw":
        hw_node_name_list.remove(node_name)

    return node_name

def deploy_transcode_cluster(service_name):
    ret = input("Do you need to deploy the " + service_name + " transcode service? ([y] or [n]): ")
    while True:
        if ret.lower() == "y":
            configure_trancode_service(yaml_file, service_name + "-transcode-service")
            break
        elif ret.lower() == "n":
            subprocess.call("rm -rf " + yaml_file, shell=True)
            break
        else:
            ret = input("Input error, Do you need to deploy the " + service_name + " transcode service? ([y] or [n]): ")

def configure_live_transcode_args(deploy_type, image_name):
    if deploy_type == "auto":
        if image_name == "sw":
            live_args = {"input_video": "bbb_sunflower_1080p_30fps_normal.mp4", "output_dict": {"big_buck_bunny_2kqhd": ["hls", "2560:1440", "15"]}, "codec_type": "libsvt_hevc"}
        else:
            live_args = {"input_video": "bbb_sunflower_1080p_30fps_normal.mp4", "output_dict": {"big_buck_bunny_2kqhd": ["hls", "2560:1440", "15"]}, "codec_type": "h264_vaapi"}
        return live_args

    if len(video_list) == 1:
        input_video = video_list[0]
    else:
        input_video = input("Please choose the one video clip to transcode (" + str(video_list)[1:-1] + "): ")
        while True:
            if input_video in video_list:
                break
            else:
                input_video = input("Input error, please choose the one video clip to transcode again (" + str(video_list)[1:-1] + "): ")

    codec_dict = {"sw": {"AVC": "libx264", "HEVC": "libsvt_hevc", "AV1": "libsvt_av1"}, "hw": {"AVC": "h264_vaapi", "HEVC": "hevc_vaapi"}}
    codec = input("Please choose which encoder you want to use (" + str(list(codec_dict[image_name].keys()))[1:-1] + "): ")
    while True:
        if codec_dict[image_name].get(codec.upper()):
            break
        else:
            codec = input("Input error, please choose which encoder you want to use again (" + str(list(codec_dict[image_name].keys()))[1:-1] + "): ")

    output_channel = input("Please choose the output channel (1, 2 ,3, 4): ")
    while True:
        if output_channel in ["1", "2", "3", "4"]:
            break
        else:
            output_channel = input("Input error, please choose the output channel again (1, 2 ,3, 4): ")

    output_dict = {}
    protocol_dict = {"a": "HLS", "b": "DASH"}
    protocol_str = ', '.join([("\033[0;31;40m" + key + "\033[0m: " + value) for key, value in protocol_dict.items()])
    resolution_dict = {"a": ["hd480", "856:480"], "b": ["hd720", "1280:720"], "c": ["hd1080", "1920:1080"], "d": ["2kqhd", "2560:1440"]}
    resolution_str = ', '.join([("\033[0;31;40m" + key + "\033[0m: " + value[0]) for key, value in resolution_dict.items()])

    for i in range(int(output_channel)):
        codec_dict = {"sw": {"AVC": "libx264", "HEVC": "libsvt_hevc", "AV1": "libsvt_av1"}, "hw": {"AVC": "h264_vaapi", "HEVC": "hevc_vaapi"}}
        codec = input("Please choose which encoder you want to use (" + str(list(codec_dict[image_name].keys()))[1:-1] + "): ")
        while True:
            if codec_dict[image_name].get(codec.upper()):
                break
            else:
                codec = input("Input error, please choose which encoder you want to use again (" + str(list(codec_dict[image_name].keys()))[1:-1] + "): ")

        resolution_key = input("Please choose the output %d resolution (%s): " % (i + 1, resolution_str))
        while True:
            if resolution_key.lower() in resolution_dict.keys():
                break
            else:
                resolution_key = input("Input error, please choose the output %d resolution again(%s): " % (i + 1, resolution_str))

        bitrate = input("Please enter the output %d bitrate([1-20]Mbps): " % (i + 1))
        while True:
            if re.match(r'([1-9]|1\d)$', bitrate):
                break
            else:
                bitrate = input("Input error, please enter the output %d bitrate again([1-20]Mbps): " % (i + 1))

        protocol_key = input("Please choose the output %d streaming media communication protocol(%s): " % (i + 1, protocol_str))
        while True:
            if protocol_key.lower() in protocol_dict.keys():
                break
            else:
                protocol_key = input("Input error, please choose the output %d streaming media communication protocol again (%s): " % (i + 1, protocol_str))

        output_name = input("Please enter the output %d video clip name: " % (i + 1))
        while True:
            if re.match(r'^[^\\\s/:\*\?"<>\|]+$', output_name):
                if output_name in output_dict.keys():
                    output_name = input("The output video clip name already exists, please enter the output %d video clip name again: " % (i + 1))
                else:
                    break
            else:
                output_name = input("Input error, please enter the output %d video clip name again: " % (i + 1))

        output_dict[output_name] = [protocol_dict[protocol_key.lower()].lower(), resolution_dict[resolution_key.lower()][1], bitrate, codec_dict[image_name].get(codec.upper())]
    live_args = {"input_video": input_video, "output_dict": output_dict}
    return live_args

def configure_trancode_service(yaml_file, service_name):
    global live_args_list

    data = yaml_utils.load_yaml_file(yaml_file)
    data = yaml_utils.add_volumeMounts(data, False)
    data = yaml_utils.add_volumes(data, nfs_server, False, volume_directory)
    i = 0

    while True:
        if len(hw_node_name_list) > 0:
            image_name = input("Please choose the transcode mode of the " + service_name + " ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5): ")
            while True:
                if image_name.lower() == "sw" or  image_name.lower() == "hw":
                    break
                else:
                    image_name = input("Please choose the transcode mode of the " + service_name + " again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5): ")
        else:
            image_name = "sw"
        node_name = input_node_name(service_name, image_name.lower())

        data = yaml_utils.update_imageName(data, image_name.lower(), False if (service_name == "live-transcode-service") else True)
        data = yaml_utils.update_nodeSelector(data, node_name)
        if service_name == "live-transcode-service":
            deploy_type = input("Do you need to deploy live-transcode-service by customizing parameters([y] or [n]): ")
            while True:
                if deploy_type.lower() == "y":
                    deploy_type = "manual"
                    break
                elif deploy_type.lower() == "n":
                    deploy_type = "auto"
                    break
                else:
                    deploy_type = input("Input error, do you need to deploy live-transcode-service by customizing parameters([y] or [n]): ")
            live_args_list.append(configure_live_transcode_args(deploy_type, image_name.lower()))
            data = yaml_utils.update_command(data, image_name.lower(), i, live_args_list)

        data = yaml_utils.update_service_name(data, service_name + "-" + str(i))
        fileName = yaml_file.rsplit("0")[0] + str(i) + "-deployment.yaml"
        yaml_utils.dump_yaml_file(data, fileName)

        i += 1
        create_node = input("Do you still need to deploy the " + str(i + 1) +  " " + service_name + "? ([y] or [n]): ")
        while True:
            if create_node.lower() == "y" or create_node.lower() == "n":
                break
            else:
                create_node = input("Input error, Do you still need to deploy the " + str(i + 1) + " " + service_name + "? ([y] or [n]): ")
        if create_node.lower() == "n":
            break

#main
node_num = get_node_num()

sw_node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
sw_node_name_list = list(filter(None, sw_node_name_list))
hw_node_name_list = copy.deepcopy(sw_node_name_list)
nfs_server, volume_directory, video_list = configure_basic_module(node_num)

#zookeeper
node_name = input_node_name("zookeeper-service")

yaml_file = sys.argv[1] + "/zookeeper-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
yaml_utils.dump_yaml_file(data, yaml_file)

# kafka
node_name = input_node_name("kafka-service")

yaml_file = sys.argv[1] + "/kafka-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
yaml_utils.dump_yaml_file(data, yaml_file)

#redis
node_name = input_node_name("redis-service")

yaml_file = sys.argv[1] + "/redis-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
yaml_utils.dump_yaml_file(data, yaml_file)

# cdn
node_name = input_node_name("cdn-service")

yaml_file = sys.argv[1] + "/cdn-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.update_nodeSelector(data, node_name)
data = yaml_utils.add_volumeMounts(data, True)
data = yaml_utils.add_volumes(data, nfs_server, True, volume_directory)
yaml_utils.dump_yaml_file(data, yaml_file)

node_port = 443
yaml_file = sys.argv[1] + "/cdn-service-service.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data = yaml_utils.set_nodePort(data, node_port)
yaml_utils.dump_yaml_file(data, yaml_file)

#vod transcode
yaml_file = sys.argv[1] + "/vod-transcode-service-0-deployment.yaml"
deploy_transcode_cluster("vod")

#live transcode
yaml_file = sys.argv[1] + "/live-transcode-service-0-deployment.yaml"
live_args_list = []
deploy_transcode_cluster("live")
get_live_video_URL(get_host_ip(), live_args_list)
