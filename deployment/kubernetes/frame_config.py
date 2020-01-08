#!/usr/bin/python3

import wx
import wx.xrc
import re
import threading
import os
import sys
from functools import reduce
import update_yaml

class MyFrame_Config (wx.Frame):

    def __init__(self, parent, nfs_server, volume_directory, video_list):
        self.nfs_server = nfs_server
        self.volume_directory = volume_directory
        self.video_list = video_list

        self.choice_list = []
        self.node_dict = {}
        basic_info = os.popen("kubectl describe node").read()
        index_list = [i.start() for i in re.finditer("Name:", basic_info)]
        for i in range(len(index_list)):
            cpu_info = re.findall(
                "(\d+)", os.popen("kubectl describe node | awk -F ' ' '$1==\"cpu\"' |awk 'NR==" + str(i+1) + "'").read())
            memory_info = re.findall(
                "(\d+)", os.popen("kubectl describe node | awk -F ' ' '$1==\"memory\" {print $0}'").read())
            cpu = int(int(re.search(
                "cpu:\s+(\d+)", basic_info[index_list[i]: -1]).group(1)) - int(cpu_info[0])/1000)
            memory = int((int(re.search(
                "memory:\s+(\d+)", basic_info[index_list[i]: -1]).group(1)) / 1024 - int(memory_info[0])))
            if cpu > 0 and memory > 0:
                self.choice_list.append({"nodename": re.search(
                    "Name:\s+(.+)", basic_info[index_list[i]: -1]).group(1), "cpu": cpu, "memory": memory})
                self.node_dict[re.search(
                    "Name:\s+(.+)", basic_info[index_list[i]: -1]).group(1)] = {"cpu": cpu, "memory": memory}

        self.setsize_num = 0
        self.live_num = 0
        self.vod_num = 0
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"config", pos=wx.DefaultPosition, size=wx.Size(
            924, 525), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        frame_bSizer = wx.BoxSizer(wx.VERTICAL)

        self.config_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_RAISED)
        config_bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.pod_panel = wx.ScrolledWindow(
            self.config_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.pod_panel.SetScrollRate(5, 5)
        pod_bSizer = wx.BoxSizer(wx.VERTICAL)

        self.modulelist = ["cdn", "redis", "zookeeper", "kafka", "vod", "live"]
        self.creat_modules_button(pod_bSizer)

        self.pod_panel.SetSizer(pod_bSizer)
        self.pod_panel.Layout()
        pod_bSizer.Fit(self.pod_panel)
        config_bSizer.Add(self.pod_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.arguments_panel = wx.Panel(
            self.config_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        arguments_bSizer = wx.BoxSizer(wx.VERTICAL)

        arguments_label = wx.StaticBoxSizer(wx.StaticBox(
            self.arguments_panel, wx.ID_ANY, u"cdn_config"), wx.VERTICAL)
        self.arguments_label = arguments_label

        self.pods_dict = {"cdn": {}, "redis": {},
                          "zookeeper": {}, "kafka": {}, "vod": {}, "live": {}}
        for key, value in self.pods_dict.items():
            self.create_pod_panel(key, arguments_label)

        arguments_bSizer.Add(arguments_label, 1, wx.EXPAND, 5)

        self.arguments_panel.SetSizer(arguments_bSizer)
        self.arguments_panel.Layout()
        arguments_bSizer.Fit(self.arguments_panel)
        config_bSizer.Add(self.arguments_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.config_panel.SetSizer(config_bSizer)
        self.config_panel.Layout()
        config_bSizer.Fit(self.config_panel)
        frame_bSizer.Add(self.config_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.menu_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.menu_panel.SetMaxSize(wx.Size(-1, 50))

        menu_bSizer = wx.BoxSizer(wx.VERTICAL)

        menu_sdbSizer = wx.StdDialogButtonSizer()
        self.menu_sdbSizerOK = wx.Button(self.menu_panel, wx.ID_OK)
        menu_sdbSizer.AddButton(self.menu_sdbSizerOK)
        self.menu_sdbSizerCancel = wx.Button(self.menu_panel, wx.ID_CANCEL)
        menu_sdbSizer.AddButton(self.menu_sdbSizerCancel)
        menu_sdbSizer.Realize()

        menu_bSizer.Add(menu_sdbSizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.menu_panel.SetSizer(menu_bSizer)
        self.menu_panel.Layout()
        menu_bSizer.Fit(self.menu_panel)
        frame_bSizer.Add(self.menu_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.log_panel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        log_bSizer = wx.BoxSizer(wx.VERTICAL)

        self.log_textCtrl = wx.TextCtrl(
            self.log_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        log_bSizer.Add(self.log_textCtrl, 1, wx.ALL | wx.EXPAND, 5)

        self.log_panel.SetSizer(log_bSizer)
        self.log_panel.Layout()
        log_bSizer.Fit(self.log_panel)
        frame_bSizer.Add(self.log_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(frame_bSizer)
        self.Layout()

        self.Centre(wx.VERTICAL)

        self.menu_sdbSizerCancel.Bind(
            wx.EVT_BUTTON, self.menu_sdbSizerOnCancelButtonClick)
        self.menu_sdbSizerOK.Bind(
            wx.EVT_BUTTON, self.menu_sdbSizerOnOKButtonClick)

        MyFrame_Config.show_pod_panel("cdn")(self, wx.EVT_BUTTON)

    def __del__(self):
        pass

    def OnClose(self, event):
        sys.exit(1)

    def creat_modules_button(self, pod_bSizer):
        for i in self.modulelist:
            setattr(self, i + "_button", wx.Button(self.pod_panel,
                                                   wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0))
            pod_bSizer.Add(getattr(self, i + "_button"), 0, wx.ALL, 5)

    def create_pod_panel(self, podname, arguments_label):
        if podname == "live" or podname == "vod":
            self.creat_module_panel(arguments_label, podname)
            self.pods_dict[podname] = {
                'node': None, 'cpu': None, 'memory': None}
        else:
            setattr(self, podname + "_panel", wx.ScrolledWindow(arguments_label.GetStaticBox(),
                                                                wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL))
            getattr(self, podname + "_panel").SetScrollRate(5, 5)
            globals()[podname + "_bSizer"] = wx.BoxSizer(wx.VERTICAL)
            for j in ["node", "cpu", "memory"]:
                setattr(self, podname + "_" + j + "_panel", wx.Panel(getattr(self, podname +
                                                                             "_panel"), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL))
                globals()[podname + "_" + j +
                          "_gSizer"] = wx.GridSizer(0, 2, 0, 0)
                setattr(self, podname + "_" + j + "_staticText", wx.StaticText(getattr(self,
                                                                                       podname + "_" + j + "_panel"), wx.ID_ANY, j, wx.DefaultPosition, wx.DefaultSize, 0))
                getattr(self, podname + "_" + j + "_staticText").Wrap(-1)
                globals()[podname + "_" + j + "_gSizer"].Add(getattr(self,
                                                                     podname + "_" + j + "_staticText"), 0, wx.ALL, 5)
                globals()[podname + "_" + "node" + "_choiceChoices"] = [node_dict["nodename"]
                                                                        for node_dict in self.choice_list]

                globals()[podname + "_" + j + "_choiceChoices"] = [item["nodename"]
                                                                   for item in self.choice_list] if j == "node" else []
                setattr(self, podname + "_" + j + "_choice", wx.Choice(getattr(self, podname + "_" + j + "_panel"),
                                                                       wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, globals()[podname + "_" + j + "_choiceChoices"], 0))
                getattr(self, podname + "_" + j + "_choice").SetSelection(-1)
                globals()[podname + "_" + j + "_gSizer"].Add(getattr(self,
                                                                     podname + "_" + j + "_choice"), 0, wx.ALL, 5)
                getattr(self, podname + "_" + j + "_panel").SetSizer(globals()
                                                                     [podname + "_" + j + "_gSizer"])
                getattr(self, podname + "_" + j + "_panel").Layout()
                globals()[
                    podname + "_" + j + "_gSizer"].Fit(getattr(self, podname + "_" + j + "_panel"))
                globals()[podname + "_bSizer"].Add(getattr(self,
                                                           podname + "_" + j + "_panel"), 1, wx.EXPAND | wx.ALL, 5)
                self.pods_dict[podname][j] = None

            if re.search("[live|vod]\d", podname):
                self.choice_dict = {"input": self.video_list, "mode": {"sw": ["AVC", "HEVC", "AV1"], "hw": ["AVC", "HEVC"]}, "protocol": [
                    "HLS", "DASH"], "resolution": ["856:480", "1280:720", "1920:1080", "2560:1440"], "bitrate": [str(i+5) for i in range(15)]}
                panel_list = ["mode", "input"] if re.search(
                    "live\d", podname) else ["mode"]

                self.pods_dict[podname]["mode"] = None
                if re.search("live\d", podname):
                    self.pods_dict[podname]['input'] = None
                    for num in range(4):
                        self.pods_dict[podname]['transcode' + str(num)] = {
                            "codec": None, "protocol": None, "resolution": None, "bitrate": None, "output": None}

                for panel_name in panel_list:
                    setattr(self, podname + "_" + panel_name + "_panel", wx.Panel(getattr(self, podname +
                                                                                          "_panel"), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL))
                    globals()[podname + "_" + panel_name +
                              "_gSizer"] = wx.GridSizer(0, 2, 0, 0)

                    setattr(self, podname + "_" + panel_name + "_staticText", wx.StaticText(getattr(self, podname +
                                                                                                    "_" + panel_name + "_panel"), wx.ID_ANY, panel_name, wx.DefaultPosition, wx.DefaultSize, 0))
                    getattr(self, podname + "_" +
                            panel_name + "_staticText").Wrap(-1)

                    globals()[podname + "_" + panel_name + "_gSizer"].Add(getattr(self,
                                                                                  podname + "_" + panel_name + "_staticText"), 0, wx.ALL, 5)

                    globals()[podname + "_" + panel_name +
                              "_choiceChoices"] = self.choice_dict[panel_name] if panel_name == "input" else ["SW", "HW"]
                    setattr(self, podname + "_" + panel_name + "_choice", wx.Choice(getattr(self, podname + "_" + panel_name + "_panel"),
                                                                                    wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, globals()[podname + "_" + panel_name + "_choiceChoices"], 0))
                    getattr(self, podname + "_" + panel_name +
                            "_choice").SetSelection(-1)
                    globals()[podname + "_" + panel_name + "_gSizer"].Add(getattr(self,
                                                                                  podname + "_" + panel_name + "_choice"), 0, wx.ALL, 5)

                    getattr(self, podname + "_" + panel_name + "_panel").SetSizer(
                        globals()[podname + "_" + panel_name + "_gSizer"])
                    getattr(self, podname + "_" +
                            panel_name + "_panel").Layout()
                    globals()[podname + "_" + panel_name + "_gSizer"].Fit(
                        getattr(self, podname + "_" + panel_name + "_panel"))
                    globals()[podname + "_bSizer"].Add(getattr(self, podname +
                                                               "_" + panel_name + "_panel"), 1, wx.EXPAND | wx.ALL, 5)

                    if panel_name == "mode" and re.search("live\d", podname):
                        setattr(MyFrame_Config, podname + "_mode_choiceOnChoice",
                                MyFrame_Config.mode_choiceOnChoice(podname))
                        getattr(self, podname + "_mode_choice").Bind(wx.EVT_CHOICE,
                                                                     getattr(self, podname + "_mode_choiceOnChoice"))

                if re.search("live\d", podname):
                    for num in range(4):
                        setattr(self, podname + "_transcode" + str(num) + "_panel", wx.Panel(getattr(
                            self, podname + "_panel"), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL))
                        globals()[podname + "_transcode" + str(num) +
                                  "_bSizer"] = wx.BoxSizer(wx.HORIZONTAL)

                        for option in ["codec", "protocol", "resolution", "bitrate"]:
                            if option == "codec":
                                globals()["%s_transcode%d_%s_choiceChoices" % (
                                    podname, num, option)] = []
                            else:
                                globals()["%s_transcode%d_%s_choiceChoices" % (
                                    podname, num, option)] = self.choice_dict[option]

                            setattr(self, podname + "_transcode" + str(num) + "_" + option + "_choice", wx.Choice(getattr(self, podname + "_transcode" + str(
                                num) + "_panel"), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, globals()["%s_transcode%d_%s_choiceChoices" % (podname, num, option)], 0))

                            getattr(self, "%s_transcode%d_%s_choice" %
                                    (podname, num, option)).SetSelection(-1)
                            globals()[podname + "_transcode" + str(num) + "_bSizer"].Add(getattr(
                                self, "%s_transcode%d_%s_choice" % (podname, num, option)), 0, wx.ALL, 5)

                        setattr(self, podname + "_transcode" + str(num) + "_output_textCtrl", wx.TextCtrl(getattr(self, podname +
                                                                                                                  "_transcode" + str(num) + "_panel"), wx.ID_ANY, "output_name", wx.DefaultPosition, wx.DefaultSize, 0))
                        globals()[podname + "_transcode" + str(num) + "_bSizer"].Add(getattr(
                            self, podname + "_transcode" + str(num) + "_output_textCtrl"), 0, wx.ALL, 5)

                        getattr(self, podname + "_transcode" + str(num) + "_panel").SetSizer(
                            globals()[podname + "_transcode" + str(num) + "_bSizer"])
                        getattr(self, podname + "_transcode" +
                                str(num) + "_panel").Layout()
                        globals()[podname + "_transcode" + str(num) + "_bSizer"].Fit(
                            getattr(self, podname + "_transcode" + str(num) + "_panel"))
                        globals()[podname + "_bSizer"].Add(getattr(self, podname +
                                                                   "_transcode" + str(num) + "_panel"), 1, wx.EXPAND | wx.ALL, 5)

                globals()[podname + "_sdbSizer"] = wx.StdDialogButtonSizer()
                setattr(self, podname + "_sdbSizerSave",
                        wx.Button(getattr(self, podname + "_panel"), wx.ID_SAVE))
                globals()[
                    podname + "_sdbSizer"].AddButton(getattr(self, podname + "_sdbSizerSave"))
                setattr(self, podname + "_sdbSizerCancel",
                        wx.Button(getattr(self, podname + "_panel"), wx.ID_CANCEL))
                globals()[podname + "_sdbSizer"].AddButton(getattr(self,
                                                                   podname + "_sdbSizerCancel"))
                globals()[podname + "_sdbSizer"].Realize()
                globals()[podname + "_bSizer"].Add(globals()
                                                   [podname + "_sdbSizer"], 1, wx.EXPAND, 5)

                setattr(MyFrame_Config, podname + "_sdbSizerOnSaveButtonClick",
                        MyFrame_Config.show_pod_panel(re.split("\d+", podname)[0]))
                getattr(self, podname + "_sdbSizerSave").Bind(wx.EVT_BUTTON,
                                                              getattr(self, podname + "_sdbSizerOnSaveButtonClick"))
                setattr(MyFrame_Config, podname + "_sdbSizerOnCancelButtonClick",
                        MyFrame_Config.cancel_pod_panel(podname))
                getattr(self, podname + "_sdbSizerCancel").Bind(wx.EVT_BUTTON,
                                                                getattr(self, podname + "_sdbSizerOnCancelButtonClick"))

            setattr(MyFrame_Config, podname + "_node_choiceOnChoice",
                    MyFrame_Config.node_choiceOnChoice(podname))
            getattr(self, podname + "_node_choice").Bind(wx.EVT_CHOICE,
                                                         getattr(self, podname + "_node_choiceOnChoice"))

            getattr(self, podname + "_panel").SetSizer(globals()
                                                       [podname + "_bSizer"])
            getattr(self, podname + "_panel").Layout()
            globals()[podname + "_bSizer"].Fit(getattr(self, podname + "_panel"))
            arguments_label.Add(
                getattr(self, podname + "_panel"), 1, wx.EXPAND | wx.ALL, 5)
            getattr(self, podname + "_panel").Hide()

        setattr(MyFrame_Config, podname + "_buttonOnButtonClick",
                MyFrame_Config.show_pod_panel(podname))
        getattr(self, podname + "_button").Bind(wx.EVT_BUTTON,
                                                getattr(self, podname + "_buttonOnButtonClick"))

    def loginfo(self):
        self.node_info = {}
        for key, value in self.pods_dict.items():
            if not (key == "live" or key == "vod"):
                getattr(self, key + "_button").SetBackgroundColour("#00FFFF")
                for i in value.keys():
                    if i.find("transcode") == -1:
                        value[i] = getattr(
                            self, key + "_" + i + "_choice").GetStringSelection()
                    else:
                        globals()[key + i + "_isready"] = True
                        for option in value[i].keys():
                            if option == "output":
                                value[i][option] = getattr(
                                    self, key + "_" + i + "_output_textCtrl").GetValue()
                            else:
                                value[i][option] = getattr(
                                    self, key + "_" + i + "_" + option + "_choice").GetStringSelection()
                            if len(value[i][option]) == 0:
                                globals()[key + i + "_isready"] = False

                    if len(value[i]) == 0 or value[i] == "0":
                        getattr(
                            self, key + "_button").SetBackgroundColour("#FFFFFF")

            if re.search("live\d", key) and not (globals()[key + "transcode0_isready"] or globals()[key + "transcode1_isready"] or globals()[key + "transcode2_isready"] or globals()[key + "transcode3_isready"]):
                getattr(self, key + "_button").SetBackgroundColour("#FFFFFF")

        for node in self.choice_list:
            self.node_info[node["nodename"]] = {
                "modules": [], "cpu": 0, "memory": 0}
            for key, value in self.pods_dict.items():
                if value["node"] == node["nodename"] and getattr(self, key + "_button").GetBackgroundColour() == "#00FFFF":
                    self.node_info[node["nodename"]]["modules"].append(key)
                    self.node_info[node["nodename"]]["cpu"] += float(
                        value["cpu"]) if len(value["cpu"]) > 0 else 0
                    self.node_info[node["nodename"]]["memory"] += int(
                        value["memory"]) if len(value["memory"]) > 0 else 0

        text_info = ""
        for item in self.choice_list:
            text_info += "Name:             %s\nPods:               %s\nCPU:                 capacity:  %-10d used:    %.1f\nMEMORY:      capacity:  %-8d used:    %8d\n" % (item['nodename'], reduce(
                lambda x, y: x + '   ' + y, self.node_info[item['nodename']]['modules']) if len(self.node_info[item['nodename']]['modules']) else None, item['cpu'], self.node_info[item['nodename']]['cpu'], item['memory'], self.node_info[item['nodename']]['memory'])
            text_info += "ERROR cpu undercapacity \n" if item['cpu'] < self.node_info[item['nodename']]['cpu'] else ""
            text_info += "ERROR memory undercapacity \n" if item['memory'] < self.node_info[item['nodename']]['memory'] else ""
        text_info += "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n"

        self.log_textCtrl.AppendText(text_info)


    @staticmethod
    def node_choiceOnChoice(podname):
        def fun(self, event):
            getattr(self, podname + "_cpu_choice").SetItems([["0.5"] + [str(num) for num in range(1, node["cpu"])]
                                                             for node in self.choice_list if node["nodename"] == getattr(self, podname + "_node_choice").GetStringSelection()][0])
            getattr(self, podname + "_memory_choice").SetItems([["500"] + [str(num) for num in range(1000, node["memory"], 500)]
                                                                for node in self.choice_list if node["nodename"] == getattr(self, podname + "_node_choice").GetStringSelection()][0])
        return fun

    @staticmethod
    def mode_choiceOnChoice(podname):
        def fun(self, event):
            codec_list = ["AVC", "HEVC"] if getattr(
                self, podname + "_mode_choice").GetStringSelection() == "HW" else ["AVC", "HEVC", "AV1"]
            for num in range(4):
                getattr(self, "%s_transcode%d_codec_choice" %
                        (podname, num)).SetItems(codec_list)
        return fun

    @staticmethod
    def cancel_pod_panel(podname):
        def fun(self, event):
            for i in ["node", "cpu", "memory", "mode", "input"]:
                getattr(self, podname + "_" + i + "_choice").SetSelection(-1)
            if re.search("live\d", podname):
                for num in range(4):
                    for option in ["codec", "protocol", "resolution", "bitrate"]:
                        getattr(self, "%s_transcode%d_%s_choice" %
                                (podname, num, option)).SetSelection(-1)
            self.loginfo()
        return fun

    @staticmethod
    def show_pod_panel(podname):
        def fun(self, event):
            for key, value in self.pods_dict.items():
                try:
                    getattr(self, key + "_panel").Hide()
                except:
                    pass
            self.arguments_label.StaticBox.SetLabel(podname + "_config")
            getattr(self, podname + "_panel").Show()
            if re.search("[(vod)|(live)]\d", podname):
                self.setsize()
            self.loginfo()
        return fun

    def setsize(self):
        self.arguments_panel.SetSize(self.arguments_panel.GetSize(
        )[0] + (-1 if self.setsize_num % 2 else 1), self.arguments_panel.GetSize()[1])
        self.setsize_num += 1

    @staticmethod
    def creat_buttonOnButtonClick(modulename):
        def fun(self, event):
            setattr(self, modulename + str(getattr(self, modulename + "_num")) + "_button", wx.Button(getattr(self, modulename + "_scrolledWindow"),
                                                                                                      wx.ID_ANY, modulename + str(getattr(self, modulename + "_num")), (20, getattr(self, modulename + "_num") * 60), wx.DefaultSize, 0))
            getattr(self, modulename + "_list_wSizer").Add(getattr(self, modulename +
                                                                   str(getattr(self, modulename + "_num")) + "_button"), 0, wx.ALL, 5)
            self.pods_dict[modulename +
                           str(getattr(self, modulename + "_num"))] = {}
            self.create_pod_panel(
                modulename + str(getattr(self, modulename + "_num")), self.arguments_label)
            setattr(self, modulename + "_num",
                    getattr(self, modulename + "_num") + 1)
            self.setsize()
        return fun

    def creat_module_panel(self, arguments_label, modulename):
        setattr(self, modulename + "_panel", wx.ScrolledWindow(arguments_label.GetStaticBox(),
                                                               wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL))
        getattr(self, modulename + "_panel").SetScrollRate(5, 5)
        globals()[modulename + "_bSizer"] = wx.BoxSizer(wx.VERTICAL)

        setattr(self, modulename + "_scrolledWindow", wx.ScrolledWindow(getattr(self, modulename +
                                                                                "_panel"), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL))
        getattr(self, modulename + "_scrolledWindow").SetScrollRate(5, 5)
        globals()[modulename + "_list_wSizer"] = wx.WrapSizer(wx.HORIZONTAL,
                                                              wx.WRAPSIZER_DEFAULT_FLAGS)
        setattr(self, modulename + "_list_wSizer",
                globals()[modulename + "_list_wSizer"])

        getattr(self, modulename + "_scrolledWindow").SetSizer(globals()
                                                               [modulename + "_list_wSizer"])
        getattr(self, modulename + "_scrolledWindow").Layout()
        globals()[modulename + "_list_wSizer"].Fit(getattr(self,
                                                           modulename + "_scrolledWindow"))
        globals()[modulename + "_bSizer"].Add(getattr(self,
                                                      modulename + "_scrolledWindow"), 1, wx.EXPAND | wx.ALL, 5)

        setattr(self, modulename + "_creat_button", wx.Button(getattr(self, modulename +
                                                                      "_panel"), wx.ID_ANY, u"creat", wx.DefaultPosition, wx.DefaultSize, 0))
        globals()[modulename + "_bSizer"].Add(getattr(self,
                                                      modulename + "_creat_button"), 0, wx.ALL, 5)
        setattr(self, modulename + "_bSizer",
                globals()[modulename + "_bSizer"])

        getattr(self, modulename + "_panel").SetSizer(globals()
                                                      [modulename + "_bSizer"])
        getattr(self, modulename + "_panel").Layout()
        globals()[modulename + "_bSizer"].Fit(getattr(self, modulename + "_panel"))
        arguments_label.Add(
            getattr(self, modulename + "_panel"), 1, wx.EXPAND | wx.ALL, 5)

        setattr(MyFrame_Config, modulename + "_creat_buttonOnButtonClick",
                MyFrame_Config.creat_buttonOnButtonClick(modulename))
        getattr(self, modulename + "_creat_button").Bind(wx.EVT_BUTTON,
                                                         getattr(self, modulename + "_creat_buttonOnButtonClick"))

    def menu_sdbSizerOnCancelButtonClick(self, event):
        sys.exit(1)

    def menu_sdbSizerOnOKButtonClick(self, event):
        self.loginfo()
        pods = []
        for key, value in self.node_info.items():
            for pod in value["modules"]:
                if getattr(self, pod + "_button").GetBackgroundColour() == (0, 255, 255, 255):
                    pods.extend(value["modules"])
                    pods = list(set(pods))

        for module in ["cdn", "redis", "zookeeper", "kafka"]:
            if module not in pods:
                self.log_textCtrl.AppendText(module + " not config\n")
                return

        update_yaml.update_yaml(nfs_server=self.nfs_server, volume_directory=self.volume_directory, dir_path = sys.argv[1],
                                pods=pods, pods_dict=self.pods_dict, node_dict=self.node_dict)
        self.Destroy()
