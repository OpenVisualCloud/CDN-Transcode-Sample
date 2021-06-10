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

default_params={
    "hls_dash_params": {
        "duration": 2,
        "segment_num": 0
    },
    "tc_params": {
        "renditions":[[1920, 1080, 5000000, 192000]],
        "codec_type":"AVC",
        "gop_size": "100",
        "framerate": "30",
        "bframe": "2",
        "preset": "veryfast",
        "profile": "578",
        "level": "30",
        "refs": "2",
        "forced_idr": "1",
        "target_type": "mp4"
    }
}

codec_setting={
    "sw": {
        "AVC": "libx264",
        "HEVC": "libsvt_hevc"
    },
    "vaapi": {
        "AVC": "h264_vaapi",
        "HEVC": "hevc_vaapi"
    },
    "qsv": {
        "AVC": "h264_qsv",
        "HEVC": "hevc_qsv"
    }
}
class FFMpegCmd:
    def __init__(self, in_params, out_params, streaming_type, params, loop=0, acc_type="sw", device=None):
        self._in_file=in_params
        self._target=out_params
        self._tc_params=params if params else default_params["tc_params"]
        self._hls_dash_params=params["hls_dash_params"] if "hls_dash_params" in params.keys() else default_params["hls_dash_params"]
        self._acc_type=acc_type

        self._segment_num=self._hls_dash_params["segment_num"]
        self._duration=self._hls_dash_params["duration"]

        self._stream_info=None
        self._streaming_type=streaming_type

        self._renditions=self._tc_params["renditions"] if self._tc_params["renditions"] else RENDITIONS_SAMPLE

        self._codec_type = self._tc_params["codec_type"]

        self._cmd_base=["ffmpeg", "-hide_banner", "-y"]
        if loop:
            self._cmd_base = self._cmd_base + ["-stream_loop", "-1"]

        self._device=device
        if not device and self._acc_type != "sw":
            self._device = "/dev/dri/renderD128"

        if self._acc_type == "vaapi":
            self._cmd_base = self._cmd_base +  ["-hwaccel", "vaapi", "-hwaccel_device", self._device, "-hwaccel_output_format", "vaapi"]
        elif self._acc_type == "qsv":
            self._cmd_base = self._cmd_base +  ["-hwaccel", "qsv", "-qsv_device", self._device, "-c:v", "h264_qsv"]

        self._cmd_base = self._cmd_base + ["-i", self._in_file]

        self._keyframe_interval = 0
        self._frame_height = 0
        self._clip_v_duration = 0
        self._clip_a_duration = 0

        self._segment_target_duration = self._duration       # try to create a new segment every X seconds
        self._max_bitrate_ratio = 1.07          # maximum accepted bitrate fluctuations
        self._rate_monitor_buffer_ratio = 1.5   # maximum buffer size between bitrate conformance checks

        self._default_threshold = 4
        self.stream_info(self._in_file)
        self._codec = self._get_codec()
        # hls and dash
        self._cmd_static = ["-c:v", self._codec, "-profile:v", "main", "-sc_threshold", "0", "-strict", "-2"]
        if self._acc_type != "sw":
            self._cmd_static = ["-profile:v", "main", "-c:v", self._codec]
        self._cmd_static += ["-g", str(self._keyframe_interval)]


    def _to_kps(self, bitrate):
        return str(int(bitrate/1000))+"k"

    def _get_codec(self):
        return codec_setting[self._acc_type][self._codec_type]

    def stream_info(self, in_file):
        ffprobe_cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", in_file]
        p = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE)
        p.wait()
        clip_info = json.loads(p.stdout.read().decode("utf-8"))

        for item in clip_info["streams"]:
            if item["codec_type"] == "video":
                self._keyframe_interval = int(eval(item["avg_frame_rate"])+0.5)
                self._frame_height = item["height"]
                self._clip_v_duration = eval(item["duration"])
            if item["codec_type"] == "audio":
                self._clip_a_duration = eval(item["duration"])

        if self._segment_num != 0:
            segment_duration = (int)((self._clip_v_duration+2.0)/self._segment_num)
            if segment_duration < self._segment_target_duration:
                self._segment_target_duration = segment_duration

    def _hls(self):
        cmd_hls = ["-hls_time", str(self._segment_target_duration), "-hls_list_size", "0"]
        cmd_fade_in_out = ["-an"]
        cmd_abr=[]
        master_playlist = "#EXTM3U" + "\n" + "#EXT-X-VERSION:3" +"\n" + "#" + "\n"
        count = 0
        for item in self._renditions:
            width = item[0]
            height = item[1]
            v_bitrate = self._to_kps(item[2])
            a_bitrate = self._to_kps(item[3])
            maxrate = self._to_kps(item[2] * self._max_bitrate_ratio)
            name = str(height) + "p"
            if self._frame_height < height:
                continue

            cmd_1 = ["-vf", "scale=w="+str(width)+":"+"h="+str(height)]
            if self._acc_type == "vaapi":
                cmd_1 = ["-vf", "scale_vaapi=w="+str(width)+":"+"h="+str(height)+":format=nv12"]
            elif self._acc_type == "qsv":
                cmd_1 = ["-vf", "scale_qsv=w="+str(width)+":"+"h="+str(height)+":format=nv12"]

            cmd_2 = ["-b:v", v_bitrate, "-maxrate", maxrate]
            cmd_3 = ["-f", self._streaming_type]
            cmd_4 = ["-hls_segment_filename", self._target+"/"+name+"_"+"%03d.ts", self._target+"/"+name+".m3u8"]
            master_playlist += "#EXT-X-STREAM-INF:BANDWIDTH="+str(item[2])+","+"RESOLUTION="+str(width)+"x"+str(height)+"\n"+name+".m3u8"+"\n"
            cmd_abr += cmd_1 + self._cmd_static + cmd_2 + cmd_fade_in_out + cmd_3 + cmd_hls + cmd_4

            count += 1
            if count > self._default_threshold:
                break
        with open(self._target+"/"+"index.m3u8", "w", encoding='utf-8') as f:
            f.write(master_playlist)
        return cmd_abr

    def _dash(self):
        cmd_dash = ["-use_timeline", "1", "-use_template", "1", "-seg_duration", str(self._segment_target_duration), "-adaptation_sets", "id=0,streams=v"]
        cmd_abr=[]
        cmd_scale=[]

        count = 0
        for item in self._renditions:
            width = item[0]
            height = item[1]
            v_bitrate = self._to_kps(item[2])
            a_bitrate = self._to_kps(item[3])
            maxrate = self._to_kps(item[2] * self._max_bitrate_ratio)
            if self._frame_height < height:
                continue
            cmd_1 = ["-map", "[out"+str(count) +"]", "-b:v"+":"+str(count), v_bitrate, "-maxrate"+":"+str(count), maxrate]
            if self._acc_type == "vaapi":
                cmd_scale += [";", "[mid"+str(count) +"]", "scale_vaapi=w="+str(width)+":"+"h="+str(height)+":format=nv12","[out"+str(count) +"]"]
            elif self._acc_type == "qsv":
                cmd_scale += [";", "[mid"+str(count) +"]", "scale_qsv=w="+str(width)+":"+"h="+str(height)+":format=nv12","[out"+str(count) +"]"]
            else:
                cmd_scale += [";", "[mid"+str(count) +"]", "scale=w="+str(width)+":"+"h="+str(height),"[out"+str(count) +"]"]
            cmd_abr += cmd_1
            count += 1
            if count > self._default_threshold:
                break
        cmd_scale = ["[0:v]split="+str(count)]+["[mid"+str(_id) +"]" for _id in range(count)]+cmd_scale
        return ["-filter_complex"] +["".join(cmd_scale)]+ self._cmd_static + cmd_abr +["-f", "dash"] + cmd_dash + ["-y", self._target+"/"+"index.mpd"]

    def _tc(self):
        cmd_1 = []
        params = self._tc_params
        stream_name = self._target.split("/")[-1].split(".")[0]
        for item in self._renditions:
            width = item[0]
            height = item[1]
            v_bitrate = self._to_kps(item[2])
            a_bitrate = self._to_kps(item[3])
            maxrate = self._to_kps(item[2] * self._max_bitrate_ratio)
            name= self._target+"/"+stream_name+self._codec_type+"_"+str(height)+"p."+self._streaming_type if self._streaming_type == "mp4" else self._target+"_"+self._codec_type+str(height)+"p"

            if self._acc_type == "vaapi":
                cmd_1 += ["-vf", "scale_vaapi=w="+str(width)+":"+"h="+str(height)+":format=nv12", "-c:v", self._codec]
                cmd_1 += ["-profile:v", "main", "-b:v", v_bitrate, "-maxrate", v_bitrate, "-r", params["framerate"],"-g", params["gop_size"], "-bf", params["bframe"], "-an", "-f", self._streaming_type, name]
            elif self._acc_type == "qsv":
                cmd_1 += ["-vf", "scale_qsv=w="+str(width)+":"+"h="+str(height)+":format=nv12", "-c:v", self._codec]
                cmd_1 += ["-profile:v", "main", "-b:v", v_bitrate, "-maxrate", v_bitrate, "-r", params["framerate"],"-g", params["gop_size"], "-bf", params["bframe"], "-an", "-f", self._streaming_type, name]
            else:
                cmd_1 += ["-vf", "scale=w="+str(width)+":"+"h="+str(height),"-c:v", self._codec, "-b:v", v_bitrate]
                cmd_1 += ["-r", params["framerate"],"-g", params["gop_size"], "-bf", params["bframe"], "-refs", params["refs"], "-preset", params["preset"], "-forced-idr", params["forced_idr"], "-an", "-f", self._streaming_type, name]

        return  cmd_1

    def cmd(self):
        cmd = []
        if self._streaming_type == "hls":
            cmd = self._cmd_base + self._hls()
        if self._streaming_type == "dash":
            cmd = self._cmd_base + self._dash()
        elif self._streaming_type == "mp4":
            cmd = self._cmd_base + self._tc()
        return cmd

