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

def update_command(data, imageName, num, live_args_list):
    scale_dict = {'sw': 'scale', 'hw': 'scale_vaapi'}
    if imageName == "hw":
        command = 'ffmpeg -re -stream_loop -1 -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i /var/www/archive/' + live_args_list[num]['input_video']
    else:
        command = 'ffmpeg -re -stream_loop -1 -i /var/www/archive/' + live_args_list[num]['input_video']
    for key, value in live_args_list[num]['output_dict'].items():
        command += ' -vf ' + scale_dict[imageName] + '=' + value[1] + ' -c:v ' + live_args_list[num]['codec_type'] + ' -b:v ' + value[2] + 'M -g 32 -forced-idr 1 -an -f flv rtmp://cdn-service/' + value[0] + '/' + key + "_" + str(num)
    command_caps = [ 'bash', '-c', command + ' -abr_pipeline']
    data['spec']['template']['spec']['containers'][0].update({'args' : command_caps})
    return data

def update_imageName(data, imageName, isVOD):
    if imageName == "hw":
        limits_caps = { 'limits': {'gpu.intel.com/i915': 1} }
        data['spec']['template']['spec']['containers'][0]['resources'] = limits_caps

    if imageName == "sw":
        data['spec']['template']['spec']['containers'][0]['resources'].clear()

    return data

def update_nodeSelector(data, nodeName):
    data['spec']['template']['spec']['nodeSelector']['kubernetes.io/hostname'] = nodeName
    return data


def add_volumeMounts(data, isCDN):
    volumemounts_caps = [ {'name': 'archive',
                           'mountPath': '/var/www/archive',
                           'readOnly': False},
                          {'name': 'dash',
                           'mountPath': '/var/www/dash',
                           'readOnly': False},
                          {'name': 'hls',
                           'mountPath': '/var/www/hls',
                           'readOnly': False} ]

    if isCDN:
        volumemounts_caps += [ {'name': 'html',
                                'mountPath': '/var/www/html',
                                'readOnly': True},
                               {'name': 'secrets',
                                'mountPath': '/var/run/secrets',
                                'readOnly': True} ]
    data['spec']['template']['spec']['containers'][0].update({'volumeMounts' : volumemounts_caps})
    return data

def add_volumes(data, nfs_server, isCDN, volume_directory):
    if nfs_server == "localhost" :
        volumes_caps = [ {'name': 'archive',
                          'hostPath':
                          {'path': volume_directory + '/volume/video/archive'} },
                         {'name': 'dash',
                          'hostPath':
                          {'path': volume_directory + '/volume/video/dash'} },
                         {'name': 'hls',
                          'hostPath':
                          {'path': volume_directory + '/volume/video/hls'} } ]

        if isCDN:
            volumes_caps += [{'name': 'html',
                              'hostPath':
                              {'path': volume_directory + '/volume/html'} },
                             {'name': 'secrets',
                              'secret': {'secretName': 'ovc-ssl-certificates'} } ]
    else:
        volumes_caps = [ {'name': 'archive',
                          'nfs':
                          {'path': volume_directory + '/volume/video/archive',
                           'server': nfs_server} },
                         {'name': 'dash',
                          'nfs':
                          {'path': volume_directory + '/volume/video/dash',
                           'server': nfs_server} },
                         {'name': 'hls',
                          'nfs':
                          {'path': volume_directory + '/volume/video/hls',
                           'server': nfs_server} } ]

        if isCDN:
            volumes_caps += [ {'name': 'html',
                               'nfs':
                               {'path': volume_directory + '/volume/html',
                                'server': nfs_server} },
                              {'name': 'secrets',
                               'secret': {'secretName': 'ovc-ssl-certificates'} } ]
    data['spec']['template']['spec'].update({'volumes' : volumes_caps})
    return data

def set_nodePort(data, port):
    data['spec']['ports'][0].update({'nodePort' : port})
    return data
