#!/usr/bin/python3

from ruamel import yaml

def load_yaml_file(fileName):
    with open(fileName, 'r', encoding='utf8') as infile:
        data = yaml.load(infile, Loader=yaml.RoundTripLoader)
    return data

def dump_yaml_file(data, fileName):
    with open(fileName, 'w', encoding='utf8') as outfile:
        yaml.dump(
            data,
            outfile,
            Dumper=yaml.RoundTripDumper,
            default_flow_style=False,
            allow_unicode=True)

def update_command(data, bisHW, live_args):
    data['spec']['template']['spec']['containers'][0]['lifecycle'] = { 'preStop': { 'exec': {'command': [ 'rm', 'rf' ] } } }
    scale_dict = {'false': 'scale', 'true': 'scale_vaapi'}
    if bisHW == "true":
        command = 'ffmpeg -re -stream_loop -1 -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi -i /var/www/archive/' + live_args['input_video']
    else:
        command = 'ffmpeg -re -stream_loop -1 -i /var/www/archive/' + live_args['input_video']
    for key, value in live_args['output_dict'].items():
        data['spec']['template']['spec']['containers'][0]['lifecycle']['preStop']['exec']['command'].append( " /var/www/" + value[0] + '/' + key )
        thread = " -thread_count 96" if value[3].find('libsvt') != -1 else ""
        command += ' -vf ' + scale_dict[bisHW] + '=' + value[1] + ' -c:v ' + value[3] + ' -b:v ' + value[2] + ' -r ' + value[4] + ' -g ' + value[5] + ' -bf ' + value[6] + ' -refs ' + value[7] + ' -preset ' + value[8] + ' -forced-idr 1' + thread + ' -an -f flv rtmp://cdn-service/' + value[0] + '/' + key

    command_caps = ['bash', '-c', command + ' -abr_pipeline']
    data['spec']['template']['spec']['containers'][0].update(
        {'args': command_caps})
    return data

def update_resource_quotas(
        data, request_cpu, limit_cpu, request_memory, limit_memory):
    data["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"] = {
        "cpu": str(int(float(request_cpu) * 1000)) + "m",
        "memory": str(request_memory)
    }
    data["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"] = {
        "cpu": str(int(float(limit_cpu) * 1000)) + "m",
        "memory": str(limit_memory)
    }
    return data
