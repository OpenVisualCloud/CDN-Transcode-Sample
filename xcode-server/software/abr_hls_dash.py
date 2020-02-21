#!/usr/bin/python3

import subprocess
import json

RENDITIONS_SAMPLE = (
    # resolution  bitrate(kbps)  audio-rate(kbps)
    [3840, 2160, 14000000, 192000],
    [2560, 1440, 10000000, 192000],
    [1920, 1080, 5000000, 192000],
    [1280, 720, 2800000, 192000],
    [842, 480, 1400000, 128000],
    [640, 360, 800000, 128000]
)

def to_kps(bitrate):
    return str(int(bitrate/1000))+"k"

def GetABRCommand(in_file, target, streaming_type, renditions=RENDITIONS_SAMPLE, duration=2,
                  segment_num=0):
    ffprobe_cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
                   "-show_streams", in_file]

    process_id = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE)
    # the `multiprocessing.Process` process will wait until
    # the call to the `subprocess.Popen` object is completed
    process_id.wait()
    clip_info = json.loads(process_id.stdout.read().decode("utf-8"))

    keyframe_interval = 0
    frame_height = 0
    clip_v_duration = 0
    clip_a_duration = 0

    segment_target_duration = duration       # try to create a new segment every X seconds
    max_bitrate_ratio = 1.07          # maximum accepted bitrate fluctuations
    rate_monitor_buffer_ratio = 1.5   # maximum buffer size between bitrate conformance checks

    for item in clip_info["streams"]:
        if item["codec_type"] == "video":
            keyframe_interval = int(eval(item["avg_frame_rate"])+0.5)
            frame_height = item["height"]
            clip_v_duration = eval(item["duration"])
        if item["codec_type"] == "audio":
            clip_a_duration = eval(item["duration"])

    if segment_num != 0:
        segment_duration = (int)((clip_v_duration+2.0)/segment_num)
        if segment_duration < segment_target_duration:
            segment_target_duration = segment_duration

    cmd = []
    cmd_abr = []
    cmd_base = ["ffmpeg", "-hide_banner", "-y", "-i", in_file]
    cmd_static = ["-c:v", "libx264", "-profile:v", "main", "-sc_threshold", "0", "-strict", "-2"]
    cmd_static += ["-g", str(keyframe_interval), "-keyint_min", str(keyframe_interval)]
    cmd_dash = ["-use_timeline", "1", "-use_template", "1", "-seg_duration",
                str(segment_target_duration)]
    cmd_hls = ["-hls_time", str(segment_target_duration), "-hls_list_size", "0"]
    cmd_fade_in_out = ["-an"]

    master_playlist = "#EXTM3U" + "\n" + "#EXT-X-VERSION:3" +"\n" + "#" + "\n"

    count = 0
    default_threshold = 4

    for item in renditions:
        width = item[0]
        height = item[1]
        v_bitrate = to_kps(item[2])
        a_bitrate = to_kps(item[3])
        maxrate = to_kps(item[2] * max_bitrate_ratio)
        bufsize = to_kps(item[2] * rate_monitor_buffer_ratio)
        name = str(height) + "p"

        if frame_height < height:
            continue

        cmd_1 = []
        cmd_2 = []
        cmd_3 = []
        cmd_4 = []

        if streaming_type == "hls":
            cmd_1 = ["-vf", "scale=w="+str(width)+":"+"h="+str(height)+":"+"force_original_aspect_ratio=decrease"
                     +","+ "pad=w="+str(width)+":"+"h="+str(height)+":"+"x=(ow-iw)/2"+":"+"y=(oh-ih)/2"]
            cmd_2 = ["-b:v", v_bitrate, "-maxrate", maxrate, "-bufsize", bufsize]
            cmd_3 = ["-f", streaming_type]
            cmd_4 = ["-hls_segment_filename", target+"/"+name+"_"+"%03d.ts", target+"/"+name+".m3u8"]
            master_playlist += "#EXT-X-STREAM-INF:BANDWIDTH="+str(item[2])+","+"RESOLUTION="+str(width)+"x"+str(height)+"\n"+name+".m3u8"+"\n"
            cmd_abr += cmd_static + cmd_1 + cmd_2 + cmd_fade_in_out + cmd_3 + cmd_hls + cmd_4

        if streaming_type == "dash":
            cmd_1 = ["-map", "0:v", "-b:v"+":"+str(count), v_bitrate, "-s:v"+":"+str(count), str(width)+"x"+str(height),
                     "-maxrate"+":"+str(count), maxrate, "-bufsize"+":"+str(count), bufsize]
            cmd_2 = ["-an"]
            cmd_3 = ["-f", streaming_type]
            cmd_4 = ["-init_seg_name", name+"-init-stream$RepresentationID$.m4s", "-media_seg_name",
                     name+"-chunk-stream$RepresentationID$-$Number%05d$.m4s", "-y", target+"/"+name+".mpd"]
            if clip_a_duration == 0:
                cmd_1 = ["-map", "0:v", "-b:v"+":"+str(count), v_bitrate, "-s:v"+":"+str(count), str(width)+"x"+str(height),
                         "-maxrate"+":"+str(count), maxrate, "-bufsize"+":"+str(count), bufsize]
                cmd_2 = []
            cmd_abr += cmd_1 + cmd_2

        count += 1
        if default_threshold < count:
            break

    if streaming_type == "hls":
        cmd = cmd_base + cmd_abr
    elif streaming_type == "dash":
        cmd = cmd_base + cmd_static + cmd_abr +["-f", "dash"] + cmd_dash + ["-y", target+"/"+"index.mpd"]

    #generate master m3u8 file
    if streaming_type == "hls":
        with open(target+"/"+"index.m3u8", "w", encoding='utf-8') as f:
            f.write(master_playlist)

    return cmd
