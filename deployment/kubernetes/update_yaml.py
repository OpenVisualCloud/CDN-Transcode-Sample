#!/usr/bin/python3

import os
import re
import copy
import subprocess
import sys
import socket
import functools


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    finally:
        s.close()
    return host_ip


def update_yaml(nfs_server, volume_directory, dir_path, pods, pods_dict, node_dict,trans_cfg_dict):
    host_ip = get_host_ip()
    sys.path.append(dir_path)
    import yaml_utils
    if re.search("live\d+", str(pods)):
        print("\n\033[0;31;40mThe live video playlist URL are below:\033[0m")
    for pod in pods:
        node_name = pods_dict[pod]["node"]
        node = node_dict[node_name]
        limit_cpu = 2 * float(pods_dict[pod]["cpu"]) if 2 * float(
            pods_dict[pod]["cpu"]) < node["cpu"] else node["cpu"] - 1
        limit_memory = 2 * int(pods_dict[pod]["memory"]) if 2 * int(
            pods_dict[pod]["memory"]) < node["memory"] else node["memory"] - 1

        yaml_file = os.path.join(dir_path, re.match(
            "([A-Za-z]+)\d*$", pod).group(1) + "-service-deployment.yaml")
        data = yaml_utils.load_yaml_file(yaml_file)
        data = yaml_utils.update_resource_quotas(
            data, pods_dict[pod]["cpu"], limit_cpu, pods_dict[pod]["memory"], limit_memory)
        data = yaml_utils.update_nodeSelector(data, node_name)

        if pod == "cdn":
            data = yaml_utils.add_volumeMounts(data, True)
            data = yaml_utils.add_volumes(
                data, nfs_server, True, volume_directory)

            node_port = 443
            service_file = dir_path + "/cdn-service-service.yaml"
            service_data = yaml_utils.load_yaml_file(service_file)
            service_data = yaml_utils.set_nodePort(service_data, node_port)
            yaml_utils.dump_yaml_file(service_data, service_file)

        if re.search("((vod)|(live))\d+", pod):
            data = yaml_utils.update_imageName(
                data, pods_dict[pod]["mode"].lower(), True if re.search("vod\d+", pod) else False)
            data = yaml_utils.add_volumeMounts(data, False)
            data = yaml_utils.add_volumes(
                data, nfs_server, False, volume_directory)
            data = yaml_utils.update_service_name(
                data, pod + "-service")
            yaml_file = os.path.join(dir_path, pod + "-service-deployment.yaml")

            if re.search("live\d", pod):
                live_args = {
                    'input_video': pods_dict[pod]["input"], "output_dict": {}}
                if trans_cfg_dict[pod]['hwaccel'] == 'false':
                    if trans_cfg_dict[pod]['protocol'] == 'DASH':
                        if trans_cfg_dict[pod]['encoder_type'] == 'AVC' or trans_cfg_dict[pod]['encoder_type'] == 'HEVC' or trans_cfg_dict[pod]['encoder_type'] == 'AV1':
                            codec_dict = {"AVC": "libx264", "HEVC": "libsvt_hevc", "AV1": "libsvt_av1"}
                        else:
                            print("Error: Only support AVC/HEVC/AV1! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                            os._exit()
                    elif trans_cfg_dict[pod]['protocol'] == 'HLS':
                        if trans_cfg_dict[pod]['encoder_type'] == 'AVC' or trans_cfg_dict[pod]['encoder_type'] == 'HEVC':
                            codec_dict = {"AVC": "libx264", "HEVC": "libsvt_hevc"}
                        else:
                            print("Error: Only support AVC/HEVC! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                            os._exit()
                    else:
                        print("Error: Please input correct protocol(HLS/DASH) in transcode.cfg (" + pod + ")")
                        os._exit()
                elif trans_cfg_dict[pod]['hwaccel'] == 'true':
                    if trans_cfg_dict[pod]['encoder_type'] == 'AVC' or trans_cfg_dict[pod]['encoder_type'] == 'HEVC':
                        codec_dict = {"AVC": "h264_vaapi", "HEVC": "hevc_vaapi"}
                    else:
                        print("Error: Only support AVC/HEVC! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                        os._exit()
                for num in range(4):
                    if pods_dict[pod].get("transcode" + str(num), None) and pods_dict[pod]["transcode" + str(num)].get("protocol", None) and pods_dict[pod]["transcode" + str(num)].get("resolution", None) and pods_dict[pod]["transcode" + str(num)].get("bitrate", None) and pods_dict[pod]["transcode" + str(num)].get("codec", None) and pods_dict[pod]["transcode" + str(num)].get("output", None):

                        live_args["output_dict"][pods_dict[pod]["transcode" + str(num)]["output"] + "_" + re.search("live(\d+)", pod).group(1) + "_" + str(num)] = [pods_dict[pod]["transcode" + str(num)]["protocol"].lower(), pods_dict[pod]["transcode" + str(num)]["resolution"], pods_dict[pod]["transcode" + str(num)]["bitrate"], codec_dict[pods_dict[pod]["transcode" + str(num)]["codec"]], pods_dict[pod]["transcode" + str(num)]["framerate"], pods_dict[pod]["transcode" + str(num)]["gop"], pods_dict[pod]["transcode" + str(num)]["maxbFrames"], pods_dict[pod]["transcode" + str(num)]["refsNum"], pods_dict[pod]["transcode" + str(num)]["preset"]]

                        print("\033[0;31;40mhttps://%s/%s/%s/index.%s\033[0m" % (host_ip, pods_dict[pod]["transcode" + str(num)]["protocol"].lower(), pods_dict[pod]["transcode" + str(num)]
                                                                                 ["output"] + "_" + re.search("live(\d+)", pod).group(1) + "_" + str(num), "m3u8" if pods_dict[pod]["transcode" + str(num)]["protocol"].lower() == "hls" else "mpd"))
                data = yaml_utils.update_command(
                    data, pods_dict[pod]["mode"].lower(), live_args)

        yaml_utils.dump_yaml_file(data, yaml_file)

    subprocess.call("rm -rf %s/vod-service-deployment.yaml" % dir_path, shell=True)
    subprocess.call("rm -rf %s/live-service-deployment.yaml" % dir_path, shell=True)
