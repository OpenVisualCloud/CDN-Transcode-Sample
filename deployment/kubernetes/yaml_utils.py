#!/usr/bin/python3

from ruamel import yaml

def load_yaml_file(fileName):
    with open(fileName, 'r', encoding='utf8') as infile:
        data = yaml.load(infile, Loader=yaml.RoundTripLoader)
    return data

def dump_yaml_file(data, fileName):
    with open(fileName, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def update_service_name(data, service_name):
    data["metadata"]["name"] = service_name
    data["spec"]["template"]["metadata"]["labels"]["io.kompose.service"] = service_name
    data["metadata"]["labels"]["io.kompose.service"] = service_name
    data["spec"]["template"]["spec"]["containers"][0]["name"] = service_name
    return data

def update_command(data, imageName, num):
    if imageName == "hw":
        command_caps = [ 'bash', '-c', 'ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i /var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4 -vf scale_vaapi=w=2560:h=1440 -c:v h264_vaapi -b:v 15M -f flv rtmp://cdn-service/hls/big_buck_bunny_2560x1440_' + str(num) + ' -vf scale_vaapi=w=1920:h=1080 -c:v h264_vaapi -b:v 10M -f flv rtmp://cdn-service/hls/big_buck_bunny_1920x1080_' + str(num) + ' -vf scale_vaapi=w=1280:h=720 -c:v h264_vaapi -b:v 8M -f flv rtmp://cdn-service/hls/big_buck_bunny_1280x720_' + str(num) + ' -vf scale_vaapi=w=854:h=480 -c:v h264_vaapi -b:v 6M -f flv rtmp://cdn-service/hls/big_buck_bunny_854x480_' + str(num) + ' -abr_pipeline' ]
    else:
        command_caps = [ 'bash', '-c', 'ffmpeg -re -stream_loop -1 -i /var/www/archive/bbb_sunflower_1080p_30fps_normal.mp4 -vf scale=2560:1440 -c:v libsvt_hevc -b:v 15M -f flv rtmp://cdn-service/hls/big_buck_bunny_2560x1440_' + str(num) + ' -vf scale=1920:1080 -c:v libsvt_hevc -b:v 10M -f flv rtmp://cdn-service/hls/big_buck_bunny_1920x1080_' + str(num) + ' -vf scale=1280:720 -c:v libx264 -b:v 8M -f flv rtmp://cdn-service/hls/big_buck_bunny_1280x720_' + str(num) + ' -vf scale=854:480 -c:v libx264 -b:v 6M -f flv rtmp://cdn-service/hls/big_buck_bunny_854x480_' + str(num) + ' -abr_pipeline' ]
    data['spec']['template']['spec']['containers'][0].update({'args' : command_caps})
    return data

def update_imageName(data, imageName, isVOD):
    if imageName == "hw" or not isVOD:
        replicas_caps = 1
    else:
        replicas_caps = 2
    data['spec']['replicas'] = replicas_caps
    data['spec']['template']['spec']['containers'][0]['image'] = "ovc_transcode_" + imageName + ":latest"
    if imageName == "hw":
        limits_caps = { 'limits': {'gpu.intel.com/i915': 1} }
        data['spec']['template']['spec']['containers'][0]['resources'] = limits_caps
    return data

def update_nodeSelector(data, nodeName):
    data['spec']['template']['spec']['nodeSelector']['kubernetes.io/hostname'] = nodeName
    return data


def add_volumeMounts(data, isCDN):
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
                               'mountPath': '/var/run/secrets',
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
    return data

def add_volumes(data, nfs_server, isCDN, cdn_directory):
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
                          'secret': {'secretName': 'ssl-key-secret'} } ]
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
                         {'name': 'html',
                          'hostPath':
                          {'path': cdn_directory + '/volume/html'} },
                         {'name': 'secrets',
                          'secret': {'secretName': 'ssl-key-secret'} } ]
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
    return data

def set_nodePort(data, port):
    data['spec']['ports'][0].update({'nodePort' : port})
    return data
