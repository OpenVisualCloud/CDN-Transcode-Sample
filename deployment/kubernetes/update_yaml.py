#!/usr/bin/python3

import os
import re
import sys
import subprocess
from ruamel import yaml

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

def load_yaml_file(fileName):
    with open(fileName, 'r', encoding='utf8') as infile:
        data = yaml.load(infile, Loader=yaml.RoundTripLoader)
    return data

def update_command(data, fileName, imageName):
    if imageName == "hw":
        command_caps = [ 'bash', '-c', 'ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i /var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4 -vf scale_vaapi=w=2560:h=1440 -c:v h264_vaapi -b:v 15M -f flv rtmp://cdn-service/hls/big_buck_bunny_2560x1440 -vf scale_vaapi=w=1920:h=1080 -c:v h264_vaapi -b:v 10M -f flv rtmp://cdn-service/hls/big_buck_bunny_1920x1080 -vf scale_vaapi=w=1280:h=720 -c:v h264_vaapi -b:v 8M -f flv rtmp://cdn-service/hls/big_buck_bunny_1280x720 -vf scale_vaapi=w=854:h=480 -c:v h264_vaapi -b:v 6M -f flv rtmp://cdn-service/hls/big_buck_bunny_854x480 -abr_pipeline' ]
    else:
        command_caps = [ 'bash', '-c', 'ffmpeg -re -stream_loop -1 -i /var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4 -vf scale=2560:1440 -c:v libsvt_hevc -b:v 15M -f flv rtmp://cdn-service/hls/big_buck_bunny_2560x1440 -vf scale=1920:1080 -c:v libsvt_hevc -b:v 10M -f flv rtmp://cdn-service/hls/big_buck_bunny_1920x1080 -vf scale=1280:720 -c:v libx264 -b:v 8M -f flv rtmp://cdn-service/hls/big_buck_bunny_1280x720 -vf scale=854:480 -c:v libx264 -b:v 6M -f flv rtmp://cdn-service/hls/big_buck_bunny_854x480 -abr_pipeline' ]
    data['spec']['template']['spec']['containers'][0].update({'args' : command_caps})
    with open(fileName, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def update_imageName(data, fileName, imageName):
    data['spec']['template']['spec']['containers'][0]['image'] = "ovc_transcode_" + imageName + ":latest"
    if imageName == "hw":
        limits_caps = [ {'limits':
                        {'gpu.intel.com/i915': 1} } ]
        data['spec']['template']['spec']['containers'][0]['resources'] = limits_caps
    with open(fileName, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def update_nodeSelector(data, fileName, nodeName):
    data['spec']['template']['spec']['nodeSelector']['kubernetes.io/hostname'] = nodeName
    with open(fileName, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def add_volumeMounts(data, fileName, isCDN):
    if (isCDN):
        volumemounts_caps = [ {'name': 'archive',
                               'mountPath': '/var/www/archive',
                               'readOnly': True},
                              {'name': 'dash',
                               'mountPath': '/var/www/dash',
                               'readOnly': False},
                              {'name': 'hls',
                               'mountPath': '/var/www/hls',
                               'readOnly': False},
                              {'name': 'html',
                               'mountPath': '/var/www/html',
                               'readOnly': True},
                              {'name': 'secrets',
                               'mountPath': '/var/www/secrets',
                               'readOnly': True} ]
    else:
        volumemounts_caps = [ {'name': 'archive',
                               'mountPath': '/var/www/archive',
                               'readOnly': True},
                              {'name': 'dash',
                               'mountPath': '/var/www/dash',
                               'readOnly': False},
                              {'name': 'hls',
                               'mountPath': '/var/www/hls',
                               'readOnly': False} ]
    data['spec']['template']['spec']['containers'][0].update({'volumeMounts' : volumemounts_caps})
    with open(fileName, "w", encoding="utf-8") as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def add_volumes(data, fileName, isCDN):
    if nfs_server == "localhost" and not isCDN:
        volumes_caps = [ {'name': 'archive',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/archive'} },
                         {'name': 'dash',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/dash'} },
                         {'name': 'hls',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/hls'} } ]
    elif nfs_server == "localhost" and isCDN:
        volumes_caps = [ {'name': 'archive',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/archive'} },
                         {'name': 'dash',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/dash'} },
                         {'name': 'hls',
                          'hostPath':
                          {'path': cdn_directory + '/volume/video/hls'} },
                         {'name': 'html',
                          'hostPath':
                          {'path': cdn_directory + '/volume/html'} },
                         {'name': 'secrets',
                          'hostPath':
                          {'path': cdn_directory + '/self-certificates'} } ]
    elif isCDN:
        volumes_caps = [ {'name': 'archive',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/archive',
                           'server': nfs_server} },
                         {'name': 'dash',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/dash',
                           'server': nfs_server} },
                         {'name': 'hls',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/hls',
                           'server': nfs_server} },
#                         {'name': 'html',
#                          'nfs':
#                          {'path': cdn_directory + '/volume/html',
#                           'server': nfs_server} },
#                         {'name': 'secrets',
#                          'nfs':
#                          {'path': cdn_directory + '/self-certificates',
#                           'server': nfs_server} }]
                         {'name': 'html',
                          'hostPath':
                          {'path': cdn_directory + '/volume/html'} },
                         {'name': 'secrets',
                          'hostPath':
                          {'path': cdn_directory + '/self-certificates'} } ]
    else:
        volumes_caps = [ {'name': 'archive',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/archive',
                           'server': nfs_server} },
                         {'name': 'dash',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/dash',
                           'server': nfs_server} },
                         {'name': 'hls',
                          'nfs':
                          {'path': cdn_directory + '/volume/video/hls',
                           'server': nfs_server} } ]
    data['spec']['template']['spec'].update({'volumes' : volumes_caps})
    with open(fileName, "w", encoding="utf-8") as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

node_num = int(os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
print("There are " + str(node_num) + " kubernetes nodes on your host server!!!")

node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
node_name_list = list(filter(None, node_name_list))

nfs_server = input("Please choose the sharing mode of the video clips server (localhost or remote NFS server ip adress):")
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
           nfs_server = input("Can't ping your NFS server ip address, Please choose the sharing mode of the video clips server again (localhost or remote NFS server ip adress):")
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
        nfs_server = input("Input error, Please choose the sharing mode of the video clips server again (localhost or remote NFS server ip adress):")

#zookeeper
node_name = input_node_name("zookeeper")

yaml_file = sys.argv[1] + "/zookeeper-service-deployment.yaml"
data = load_yaml_file(yaml_file)
update_nodeSelector(data, yaml_file, node_name)

# kafka
node_name = input_node_name("kafka")

yaml_file = sys.argv[1] + "/kafka-service-deployment.yaml"
data = load_yaml_file(yaml_file)
update_nodeSelector(data, yaml_file, node_name)

# cdn
node_name = input_node_name("cdn")

yaml_file = sys.argv[1] + "/cdn-service-deployment.yaml"
data = load_yaml_file(yaml_file)
update_nodeSelector(data, yaml_file, node_name)
add_volumeMounts(data, yaml_file, True)
add_volumes(data, yaml_file, True)

#vod transcode
node_name = input_node_name("vod transcode")

image_name = input("Please choose the transcode mode of the vod transcode server (hw or sw):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server (hw or sw):")

yaml_file = sys.argv[1] + "/vod-transcode-service-deployment.yaml"
data = load_yaml_file(yaml_file)
update_imageName(data, yaml_file, image_name.lower())
update_nodeSelector(data, yaml_file, node_name)
add_volumeMounts(data, yaml_file, False)
add_volumes(data, yaml_file, False)

#live_transcode
node_name = input_node_name("live transcode")

image_name = input("Please choose the transcode mode of the live transcode server (hw or sw):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server (hw or sw):")

yaml_file = sys.argv[1] + "/live-transcode-service-deployment.yaml"
data = load_yaml_file(yaml_file)
update_imageName(data, yaml_file, image_name.lower())
update_command(data, yaml_file, image_name.lower())
update_nodeSelector(data, yaml_file, node_name)
add_volumeMounts(data, yaml_file, False)
add_volumes(data, yaml_file, False)
