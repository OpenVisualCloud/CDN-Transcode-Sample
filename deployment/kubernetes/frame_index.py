#!/usr/bin/python3

import wx
import wx.xrc
import re
import os
import sys
import functools
from frame_config import MyFrame_Config

class MyFrame_Index (wx.Frame):

    def __init__(self, parent):
        self.errwin = wx.MessageDialog(
            parent=None,
            message=u"Invalid parameter, Please input a integer ...",
            caption=u"ERROR",
            style=wx.OK)

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"NFS Server Configuration",
                          pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText1 = wx.StaticText(
            self, wx.ID_ANY, u"IP address:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        gSizer1.Add(self.m_staticText1, 0, wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(
            self, wx.ID_ANY, u"Username:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        gSizer1.Add(self.m_staticText3, 0, wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(
            self, wx.ID_ANY, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        gSizer1.Add(self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        gSizer1.Add(self.m_textCtrl3, 0, wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(
            self, wx.ID_ANY, u"Project directory path:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        gSizer1.Add(self.m_staticText5, 0, wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl4, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, u"cancel", wx.DefaultPosition, wx.DefaultSize, 0)

        self.Bind(wx.EVT_BUTTON, self.cancelEvent, self.m_button1)
        gSizer1.Add(self.m_button1, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, u"save", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.sureEvent, self.m_button2)
        gSizer1.Add(self.m_button2, 0, wx.ALL, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def OnClose(self, event):
        sys.exit(1)

    def sureEvent(self, event):
        self.nfs_server = self.m_textCtrl1.GetValue()
        self.username = self.m_textCtrl2.GetValue()
        self.password = self.m_textCtrl3.GetValue()
        self.volume_directory = self.m_textCtrl4.GetValue()

        check_info = self.check_info()
        if not check_info == "OK":
            self.errwin.SetMessage(check_info)
            self.errwin.ShowModal()
            return

        try:
            exec_cmd = os.popen("fab -u %s -p %s -H %s -- 'ls %s'" % (self.username, self.password,
                                                                      self.nfs_server, os.path.join(self.volume_directory, "volume/video/archive")))
            result = [re.findall(r'[^\\\s/:\*\?"<>\|]+', i)
                      for i in re.findall(r'out:(.+)\n', exec_cmd.read())]
            video_list = [i for i in functools.reduce(
                lambda x, y:x+y, result) if os.path.splitext(i)[1] == '.mp4']
        except:
            self.errwin.SetMessage("connect error")
            self.errwin.ShowModal()
            return

        if len(video_list) == 0:
            self.errwin.SetMessage("no video")
            self.errwin.ShowModal()
            return

        self.Destroy()
        frame_config = MyFrame_Config(None, nfs_server=self.nfs_server,
                                      volume_directory=self.volume_directory, video_list=video_list)
        frame_config.Show(True)

    def cancelEvent(self, event):
        sys.exit(1)

    def check_info(self):
        if not re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$", self.nfs_server):
            return "ip is error"
        for info in ["username", "password", "volume_directory"]:
            if not re.search("^([\w_\-\&/]+)+$", getattr(self, info)):
                return info + " error"

        if not os.path.isabs(self.volume_directory):
            return "not abs"
        elif re.match(".+/$", self.volume_directory):
            self.volume_directory = self.volume_directory[:-1]

        return "OK"
