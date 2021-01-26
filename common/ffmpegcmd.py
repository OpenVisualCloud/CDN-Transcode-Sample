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
    "hw": {
        "AVC": "h264_vaapi",
        "HEVC": "hevc_vaapi"
    }
}
class FFMpegCmd:
    def __init__(self, in_params, out_params, streaming_type, params, loop=0, hw="false"):
        self._in_file=in_params
        self._target=out_params
        self._tc_params=params if params else default_params["tc_params"]
        self._hls_dash_params=params["hls_dash_params"] if "hls_dash_params" in params.keys() else default_params["hls_dash_params"]
        self._hw=hw
        self._platform="hw" if hw == "true" else "sw"

        self._segment_num=self._hls_dash_params["segment_num"]
        self._duration=self._hls_dash_params["duration"]

        self._stream_info=None
        self._streaming_type=streaming_type

        self._renditions=self._tc_params["renditions"] if self._tc_params["renditions"] else RENDITIONS_SAMPLE

        self._codec_type = self._tc_params["codec_type"]

        self._cmd_base=["ffmpeg", "-hide_banner", "-y"]
        if loop:
            self._cmd_base = self._cmd_base + ["-stream_loop", "-1"]
        if self._hw == "true":
            self._cmd_base = self._cmd_base +  ["-hwaccel", "vaapi", "-hwaccel_device", "/dev/dri/renderD128", "-hwaccel_output_format", "vaapi"]
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


    def _to_kps(self, bitrate):
        return str(int(bitrate/1000))+"k"

    def _get_codec(self):
        if self._streaming_type == "dash" or self._streaming_type == "hls":
            return "libx264"
        else:
            return codec_setting[self._platform][self._codec_type]

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

    def _hls_dash(self):
        cmd_static = ["-c:v", self._codec, "-profile:v", "main", "-sc_threshold", "0", "-strict", "-2"]
        cmd_static += ["-g", str(self._keyframe_interval), "-keyint_min", str(self._keyframe_interval)]
        cmd_dash = ["-use_timeline", "1", "-use_template", "1", "-seg_duration",
                    str(self._segment_target_duration), "-adaptation_sets", "id=0,streams=v"]
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
            bufsize = self._to_kps(item[2] * self._rate_monitor_buffer_ratio)
            name = str(height) + "p"
            if self._frame_height < height:
                continue
            cmd_1 = []
            cmd_2 = []
            cmd_3 = []
            cmd_4 = []
            if self._streaming_type == "hls":
                cmd_1 = ["-vf", "scale=w="+str(width)+":"+"h="+str(height)]
                cmd_2 = ["-b:v", v_bitrate, "-maxrate", maxrate, "-bufsize", bufsize]
                cmd_3 = ["-f", self._streaming_type]
                cmd_4 = ["-hls_segment_filename", self._target+"/"+name+"_"+"%03d.ts", self._target+"/"+name+".m3u8"]
                master_playlist += "#EXT-X-STREAM-INF:BANDWIDTH="+str(item[2])+","+"RESOLUTION="+str(width)+"x"+str(height)+"\n"+name+".m3u8"+"\n"
                cmd_abr += cmd_static + cmd_1 + cmd_2 + cmd_fade_in_out + cmd_3 + cmd_hls + cmd_4
            elif self._streaming_type == "dash":
                cmd_1 = ["-map", "0:v", "-b:v"+":"+str(count), v_bitrate, "-s:v"+":"+str(count), str(width)+"x"+str(height),
                         "-maxrate"+":"+str(count), maxrate, "-bufsize"+":"+str(count), bufsize]
                cmd_2 = ["-an"]
                cmd_3 = ["-f", self._streaming_type]
                cmd_4 = ["-init_seg_name", name+"-init-stream$RepresentationID$.m4s", "-media_seg_name",
                         name+"-chunk-stream$RepresentationID$-$Number%05d$.m4s", "-y", self._target+"/"+name+".mpd"]
                if self._clip_a_duration == 0:
                    cmd_1 = ["-map", "0:v", "-b:v"+":"+str(count), v_bitrate, "-s:v"+":"+str(count), str(width)+"x"+str(height),
                             "-maxrate"+":"+str(count), maxrate, "-bufsize"+":"+str(count), bufsize]
                    cmd_2 = []
                cmd_abr += cmd_1 + cmd_2

            count += 1
            if count > self._default_threshold:
                break

        if self._streaming_type == "hls":
            with open(self._target+"/"+"index.m3u8", "w", encoding='utf-8') as f:
                f.write(master_playlist)
            return cmd_abr
        elif self._streaming_type == "dash":
            return cmd_static + cmd_abr +["-f", "dash"] + cmd_dash + ["-y", self._target+"/"+"index.mpd"]

    def _tc(self):
        cmd_1 = []
        params = self._tc_params
        for item in self._renditions:
            width = item[0]
            height = item[1]
            v_bitrate = self._to_kps(item[2])
            a_bitrate = self._to_kps(item[3])
            maxrate = self._to_kps(item[2] * self._max_bitrate_ratio)
            bufsize = self._to_kps(item[2] * self._rate_monitor_buffer_ratio)
            name= self._target+"/"+self._codec_type+"_"+str(height)+"p."+self._streaming_type if self._streaming_type == "mp4" else self._target+"_"+self._codec_type+str(height)+"p"

            if self._hw == "true":
                cmd_1 += ["-vf", "scale_vaapi=w="+str(width)+":"+"h="+str(height)+":format=nv12", "-c:v", self._codec]
                cmd_1 += ["-profile", "578", "-level", "30", "-b:v", v_bitrate, "-maxrate", v_bitrate, "-r", params["framerate"],"-g", params["gop_size"], "-bf", params["bframe"], "-an", "-f", self._streaming_type, name]
            else:
                cmd_1 += ["-vf", "scale=w="+str(width)+":"+"h="+str(height),"-c:v", self._codec, "-b:v", v_bitrate]
                cmd_1 += ["-r", params["framerate"],"-g", params["gop_size"], "-bf", params["bframe"], "-refs", params["refs"], "-preset", params["preset"], "-forced-idr", params["forced_idr"], "-an", "-f", self._streaming_type, name]

        return  cmd_1 + ["-abr_pipeline"]

    def cmd(self):
        cmd = []
        if self._streaming_type == "hls" or self._streaming_type == "dash":
            cmd = self._cmd_base + self._hls_dash()
        elif self._streaming_type == "mp4":
            cmd = self._cmd_base + self._tc()
        return cmd

