#!/usr/bin/python3

import os
import re
import sys
import socket
import functools
import yaml_utils

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    finally:
        s.close()
    return host_ip

def update_yaml(dir_path, pods, pods_dict,trans_cfg_dict):
    host_ip = get_host_ip()
    sys.path.append(dir_path)

    if re.search("live\d+", str(pods)):
        print("\n\033[0;31;40mThe live video playlist URL are below:\033[0m")
    for pod in pods:
        limit_cpu = 2 * float(pods_dict[pod]["cpu"])
        limit_memory = str(2 * int(str(pods_dict[pod]["memory"])[0:-2])) + str(pods_dict[pod]["memory"])[-2:]

        yaml_file = os.path.join(dir_path, re.findall(
            "([A-Za-z]+-*\d*$)", pod)[0] + "-deploy.yaml")
        data = yaml_utils.load_yaml_file(yaml_file)
        data = yaml_utils.update_resource_quotas(
            data, pods_dict[pod]["cpu"], limit_cpu, pods_dict[pod]["memory"], limit_memory)

        if re.search("((vod)|(live-))\d+", pod):
            yaml_file = os.path.join(dir_path, pod + "-deploy.yaml")
            if re.search("live-\d", pod):
                live_args = {
                    'input_video': pods_dict[pod]["input"], "output_dict": {}}
                if trans_cfg_dict[pod]['hwaccel'] == 'false':
                    if trans_cfg_dict[pod]['protocol'] == 'DASH':
                        if trans_cfg_dict[pod]['encodetype'] == 'AVC' or trans_cfg_dict[pod]['encodetype'] == 'HEVC' or trans_cfg_dict[pod]['encodetype'] == 'AV1':
                            codec_dict = {"AVC": "libx264", "HEVC": "libsvt_hevc", "AV1": "libsvt_av1"}
                        else:
                            print("Error: Only support AVC/HEVC/AV1! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                            os._exit()
                    elif trans_cfg_dict[pod]['protocol'] == 'HLS':
                        if trans_cfg_dict[pod]['encodetype'] == 'AVC' or trans_cfg_dict[pod]['encodetype'] == 'HEVC':
                            codec_dict = {"AVC": "libx264", "HEVC": "libsvt_hevc"}
                        else:
                            print("Error: Only support AVC/HEVC! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                            os._exit()
                    else:
                        print("Error: Please input correct protocol(HLS/DASH) in transcode.cfg (" + pod + ")")
                        os._exit()
                elif trans_cfg_dict[pod]['hwaccel'] == 'true':
                    if trans_cfg_dict[pod]['encodetype'] == 'AVC' or trans_cfg_dict[pod]['encodetype'] == 'HEVC':
                        codec_dict = {"AVC": "h264_vaapi", "HEVC": "hevc_vaapi"}
                    else:
                        print("Error: Only support AVC/HEVC! Please input correct encoder_type in transcode.cfg (" + pod + ")")
                        os._exit()
                for num in range(4):
                    if pods_dict[pod].get("transcode" + str(num), None) and pods_dict[pod]["transcode" + str(num)].get("protocol", None) and pods_dict[pod]["transcode" + str(num)].get("resolution", None) and pods_dict[pod]["transcode" + str(num)].get("bitrate", None) and pods_dict[pod]["transcode" + str(num)].get("codec", None) and pods_dict[pod]["transcode" + str(num)].get("output", None):

                        live_args["output_dict"][pods_dict[pod]["transcode" + str(num)]["output"] + "_" + re.search("live-(\d+)", pod).group(1) + "_" + str(num)] = [pods_dict[pod]["transcode" + str(num)]["protocol"].lower(), pods_dict[pod]["transcode" + str(num)]["resolution"], pods_dict[pod]["transcode" + str(num)]["bitrate"], codec_dict[pods_dict[pod]["transcode" + str(num)]["codec"]], pods_dict[pod]["transcode" + str(num)]["framerate"], pods_dict[pod]["transcode" + str(num)]["gop"], pods_dict[pod]["transcode" + str(num)]["maxbFrames"], pods_dict[pod]["transcode" + str(num)]["refsNum"], pods_dict[pod]["transcode" + str(num)]["preset"]]

                        print("\033[0;31;40mhttps://%s/%s/%s/index.%s\033[0m" % (host_ip, pods_dict[pod]["transcode" + str(num)]["protocol"].lower(), pods_dict[pod]["transcode" + str(num)]
                                                                                 ["output"] + "_" + re.search("live-(\d+)", pod).group(1) + "_" + str(num), "m3u8" if pods_dict[pod]["transcode" + str(num)]["protocol"].lower() == "hls" else "mpd"))
                data = yaml_utils.update_command(
                    data, trans_cfg_dict[pod]['hwaccel'], live_args)

        yaml_utils.dump_yaml_file(data, yaml_file)
