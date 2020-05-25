#!/usr/bin/python3

import yaml_utils
import update_yaml
import re
import sys
import configparser
sys.path.append(sys.argv[1])

def configure_live_transcode_args(service_name, trans_cfg_dict):
    pods_dict[service_name]["input"] = trans_cfg_dict[service_name]['url']
    for trans_num in range(int(trans_cfg_dict[service_name]['density'])):
        pods_dict[service_name]["transcode" + str(trans_num)] = {
        'codec': trans_cfg_dict[service_name]['encodetype'], 'protocol': trans_cfg_dict[service_name]['protocol'], 'resolution': trans_cfg_dict[service_name]['width'] + "x" + trans_cfg_dict[service_name]['height'], 'bitrate': trans_cfg_dict[service_name]['bitrate'], 'framerate':trans_cfg_dict[service_name]['framerate'], 'gop': trans_cfg_dict[service_name]['gop'], 'maxbFrames': trans_cfg_dict[service_name]['maxbframes'], 'refsNum': trans_cfg_dict[service_name]['refsnum'], 'preset': trans_cfg_dict[service_name]['preset'], 'output': 'output_name'}
    return

def configure_live_transcode_service(num, trans_cfg_dict):
    for i in range(int(num)):
       service_name_index = "live-" + str(i)
       pods.append(service_name_index)
       pods_dict[service_name_index] = {}

       configure_live_transcode_args(
               service_name_index, trans_cfg_dict)

def get_request_cpu(service_name, pods_dict, cpu_quota):
    if re.match(r"\d{1,2}(\.\d+)?$", cpu_quota):
        pods_dict[service_name]["cpu"] = float(cpu_quota)
    else:
        print("Error: Pleaes redistribute CPU request in cpu_mem_management.cfg")
        os._exit()
    return pods_dict

def get_request_mem(service_name, pods_dict, mem_quota):
    if re.match(r"\d{3,5}[MKG]i", mem_quota):
        pods_dict[service_name]["memory"] = str(mem_quota)
    else:
        print("Error: Pleaes redistribute memory request in cpu_mem_management.cfg")
        os._exit()
    return pods_dict

def get_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    config_dict = dict(config._sections)
    for k in config_dict:
        config_dict[k] = dict(config_dict[k])
    return config_dict

DIRS = sys.argv[1]
NVODS = sys.argv[2]
NLIVES = sys.argv[3]

pods_dict = {"cdn": {}, "redis": {}, "zookeeper": {}, "kafka": {}}
pods = ["cdn", "redis", "zookeeper", "kafka"]

cpu_mem_cfg = DIRS + '/cpu_mem_management.cfg'
cpu_mem_cfg_dict = get_config(cpu_mem_cfg)
live_transcode_cfg = {}
live_trans_cfg_dict = {}

if int(NVODS) > 0:
   pods.append("vod")
   pods_dict["vod"] = {}

if int(NLIVES) > 0:
   live_transcode_cfg = DIRS + '/live-transcode.cfg'
   live_trans_cfg_dict = get_config(live_transcode_cfg) 
   configure_live_transcode_service(NLIVES, live_trans_cfg_dict)

for pod in pods:
    print(pod);
    pods_dict = get_request_cpu(pod, pods_dict, cpu_mem_cfg_dict[pod]['cpu'])
    pods_dict = get_request_mem(pod, pods_dict, cpu_mem_cfg_dict[pod]['mem'])

update_yaml.update_yaml(sys.argv[1], pods, pods_dict, live_trans_cfg_dict)
