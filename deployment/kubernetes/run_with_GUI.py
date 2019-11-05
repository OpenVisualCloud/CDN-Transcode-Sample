#!/usr/bin/python3

import wx
from frame_index import MyFrame_Index

if __name__ == '__main__':
    app = wx.App()
    dlg = MyFrame_Index(None)
    dlg.Show(True)
    app.MainLoop()
