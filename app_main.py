# -*- coding: utf-8 -*-
"""Main Interface Window and Application Launch"""

import sys
import wx

import pane
import mode

import fn_path


class WindowFrame(wx.Frame):
    """Base class defining the application window (frame)"""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        wx.Frame.__init__(self, *args, **kwargs)

        # Define the main pane  and add to the primary sizer
        self.pane_main = pane.PaneMain(self)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)
        self.szr_main.Add(self.pane_main, proportion=1, flag=wx.EXPAND)

        # Define lower status bar
        self.status = self.CreateStatusBar(1)
        self.status.SetStatusText("Written by Ancient Abysswalker")

        # Set icon
        self.SetIcon(wx.Icon(fn_path.concat_gui('icon.png')))

        # Set window minimum size, set starting sizer and show window
        self.SetMinSize((300, 300))
        self.SetSizer(self.szr_main)
        self.Show()


if __name__ == '__main__':
    """Launch the application."""

    # Set build number to display
    build = "1.0.0"

    # First set build/dev mode
    mode.set_mode(getattr(sys, 'frozen', False))

    # Define the application and call config
    app = wx.App(False)

    # Define window size and frame, and start the main application loop
    win = WindowFrame(None, size=(400, 500))
    win.SetTitle("Aria - Build " + build)
    app.MainLoop()
