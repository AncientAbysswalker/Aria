# -*- coding: utf-8 -*-
"""Main Interface Window and Application Launch"""

import sys
import wx

import pane
import mode

import config
import fn_path


class WindowFrame(wx.Frame):
    """Base class defining the application window (frame)"""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        wx.Frame.__init__(self, *args, **kwargs)

        # Define the two primary sizers for different panes
        # self.szr_login = wx.BoxSizer(wx.VERTICAL)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)

        # Define the main pane, hide until after login, add to sizer
        self.pane_main = pane.PaneMain(self)
        # self.pane_main.Hide()
        self.szr_main.Add(self.pane_main, proportion=1, flag=wx.EXPAND)

        # Define the login pane, add to sizer
        # self.pane_login = pane.PaneLogin(self, self.szr_main, self.pane_main)
        # self.szr_login.Add(self.pane_login, proportion=1, flag=wx.EXPAND)

        # Define lower status bar
        self.status = self.CreateStatusBar(1)
        self.status.SetStatusText("Written by Ancient Abysswalker")

        # Set icon
        self.SetIcon(wx.Icon(fn_path.concat_gui('icon.png')))

        # Set window minimum size, set starting sizer and show window
        self.SetMinSize((400, 500))
        self.SetSizer(self.szr_main)
        self.Show()

    # def evt_on_add(self, event):
    #     pass


if __name__ == '__main__':
    """Launch the application."""

    # Set build number to display
    build = "1.0.0"

    # First set build/dev mode
    mode.set_mode(getattr(sys, 'frozen', False))

    # Define appliction and call config
    app = wx.App(False)
    config.load_config(app)

    # Define window size and frame, and start the main application loop
    win = WindowFrame(None, size=(400, 500))
    win.SetTitle("Aria - Build " + build)
    app.MainLoop()
