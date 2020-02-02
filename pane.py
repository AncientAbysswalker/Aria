# -*- coding: utf-8 -*-
"""This module defines panes - master panels that act as direct children of the progenitor frame"""

import wx
import os
import PyPDF2


class PaneMain(wx.Panel):
    """Debug login panel class. Automatically passes login check to following (landing) page

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to
                sizer_landing (ptr): Reference to the sizer (of the parent) the landing pane belongs to
                pane_landing (ptr): Reference to the landing pane
                bound_text (str, optional): String to display in the login panel bounding box
                user_last (str, optional): String to initially display within the "user" textbox
                pass_last (str, optional): String to initially display within the "passkey" textbox
                user_text (str, optional): String to display preceding the "user" textbox
                pass_text (str, optional): String to display preceding the "passkey" textbox

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
                sizer_landing (ptr): Reference to the sizer (of the parent) the landing pane belongs to
                pane_landing (ptr): Reference to the landing pane
                login_user (ptr): Reference to the "user" textbox
                login_pass (ptr): Reference to the "passkey" textbox
        """

    def __init__(self, parent, *args, **kwargs):
        """Constructor"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Empty Lists
        self.ls_paths = []
        self.ls_files = []

        # Button Widget Objects
        btn_add = wx.Button(self, size=(75, 25), label="ADD")
        self.Bind(wx.EVT_BUTTON, self.evt_add, btn_add)
        btn_merge = wx.Button(self, size=(75, 25), label="MERGE")
        self.Bind(wx.EVT_BUTTON, self.evt_submit, btn_merge)
        btn_clear = wx.Button(self, size=(75, 25), label="CLEAR")
        self.Bind(wx.EVT_BUTTON, self.evt_clear, btn_clear)

        # Button Sizer
        self.szr_buttons = wx.BoxSizer(wx.VERTICAL)
        self.szr_buttons.Add(btn_add, flag=wx.CENTER)
        self.szr_buttons.Add(btn_merge, flag=wx.CENTER)
        self.szr_buttons.AddSpacer(5)
        self.szr_buttons.Add(wx.StaticText(self), proportion=1)
        self.szr_buttons.Add(btn_clear, flag=wx.CENTER | wx.BOTTOM)

        # Added PDFs
        self.wgt_added_docs = wx.TextCtrl(self, size=(750, 1500), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.EXPAND)

        # Overall Sizer
        szr_main = wx.BoxSizer(wx.HORIZONTAL)
        szr_main.Add(self.szr_buttons, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        szr_main.Add(self.wgt_added_docs, proportion=3, flag=wx.EXPAND)

        self.SetSizer(szr_main)

    def evt_add(self, event):
        """Add file(s) to list of files to merge

            Args:
                event: A button event
        """

        # Open an explorer dialog to select images to import
        with wx.FileDialog(None, "Open",
                           wildcard="pdf files (*.pdf)|*.pdf",
                           style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST) as file_dialog:

            # Check if the user changed their mind about importing
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            # Make a list of chosen images to add to the database
            selected_paths = file_dialog.GetPaths()
            selected_files = [os.path.basename(your_path) for your_path in file_dialog.GetPaths()]

        # Proceed loading the file(s) chosen by the user to the "add image" dialog
        self.ls_paths.extend(selected_paths)
        self.ls_files.extend(selected_files)

        # Update the widget to display new files list
        self.wgt_added_docs.SetValue("\n".join(self.ls_files))

    def evt_submit(self, event):
        """Merges the intended PDF file

            Args:
                event: A button event
        """

        # Check if the list is populated
        if self.ls_paths:
            print(356)
            # Assemble PDF
            pdf_merger = PyPDF2.PdfFileMerger(strict=False)
            for document in self.ls_paths:
                pdf_merger.append(document)

            with wx.FileDialog(None, "Save",
                               wildcard="pdf files (*.pdf)|*.pdf",
                               style=wx.FD_SAVE) as file_dialog:

                # Check if the user changed their mind about importing
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return

                # Save merged file to selected location
                pdf_merger.write(file_dialog.GetPath())

            # Close merging gracefully
            pdf_merger.close()

    def evt_clear(self, event):
        """Clears the widget listing files to merge

            Args:
                event: A button event
        """

        # Empty Lists
        self.ls_paths = []
        self.ls_files = []

        # Reset widget
        self.wgt_added_docs.SetValue("")
