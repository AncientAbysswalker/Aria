# -*- coding: utf-8 -*-
"""This module defines panes - master panels that act as direct children of the progenitor frame"""

import wx
import os
import PyPDF2

import fn_path


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

        # Checkbox Widget Objects
        # self.wgt_print_to_desktop = wx.CheckBox(self, label="Save to Desktop")
        # self.wgt_print_to_desktop.SetValue(True)
        self.wgt_flatten_pdf = wx.CheckBox(self, label="Flatten PDF")
        self.wgt_flatten_pdf.SetValue(False)

        # Button Sizer
        self.szr_buttons = wx.BoxSizer(wx.VERTICAL)
        self.szr_buttons.Add(btn_add, flag=wx.CENTER)
        self.szr_buttons.Add(btn_merge, flag=wx.CENTER)
        self.szr_buttons.AddSpacer(5)
        self.szr_buttons.Add(self.wgt_print_to_desktop, flag=wx.CENTER | wx.ALL, border=5)
        self.szr_buttons.Add(self.wgt_flatten_pdf, flag=wx.CENTER | wx.ALL, border=5)
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

        # Assemble PDF
        pdf_merger = PyPDF2.PdfFileMerger(strict=False)
        for document in self.ls_paths:
            pdf_merger.append(document)

        # for page in merger.getPage(0)
        # for j in range(0, len(page['/Annots'])):
        #     writer_annot = page['/Annots'][j].getObject()
        #     for field in data_dict:
        #         if writer_annot.get('/T') == field:
        #             writer_annot.update({
        #                 NameObject("/Ff"): NumberObject(1)  # make ReadOnly
        #             })

        # # Determine save-to location
        # if self.wgt_print_to_desktop.GetValue():
        #     # Write to desktop
        #     pdf_merger.write(os.path.join(os.path.expandvars('%UserProfile%'), 'Desktop', "merged.pdf"))
        # else:
        #     # Write to custom location

        with wx.FileDialog(None, "Save",
                           wildcard="pdf files (*.pdf)|*.pdf",
                           style=wx.FD_SAVE) as file_dialog:

            # Check if the user changed their mind about importing
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            # Save merged file to selected location
            pdf_merger.write(file_dialog.GetPath())
            # print(file_dialog.GetPath())
            # selected_files = [os.path.basename(your_path) for your_path in file_dialog.GetPaths()]

        #
        # dialog = wx.RichMessageDialog(self,
        #                               caption="PDF Printed",
        #                               message="The pdf has been printed to " + self.file_dest.GetValue(),
        #                               style=wx.OK | wx.ICON_INFORMATION)
        # dialog.ShowModal()
        # dialog.Destroy()

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


class PaneMain2(wx.Panel):
    """Master pane that contains the normal operational widgets for the application

        Class Variables:
            bar_size (int): Size (height) of the top ribbon with the searchbar

        Args:
            parent (ptr): Reference to the wx.object this panel belongs to

        Attributes:
            parent (ptr): Reference to the wx.object this panel belongs to
    """

    bar_size = 25

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetDoubleBuffered(True)  # Remove odd effects at main switch to this pane after login

        self.parent = parent

        # Search bar and bind
        self.wgt_searchbar = wx.TextCtrl(self,
                                         size=(PaneMain.bar_size*10, PaneMain.bar_size),
                                         style=wx.TE_PROCESS_ENTER)
        self.wgt_searchbar.Bind(wx.EVT_TEXT_ENTER, self.evt_search)

        # Search bar button and bind
        btn_search = wx.BitmapButton(self,
                                     bitmap=wx.Bitmap(fn_path.concat_gui('search.png')),
                                     size=(PaneMain.bar_size, ) * 2)
        btn_search.Bind(wx.EVT_BUTTON, self.evt_search)
        btn_search.Bind(wx.EVT_SET_FOCUS, self.evt_button_no_focus)

        # Notebook widget
        self.wgt_notebook = tab.Notebook(self)

        # Top bar sizer
        szr_bar = wx.BoxSizer(wx.HORIZONTAL)
        szr_bar.AddSpacer(3)
        szr_bar.Add(self.wgt_searchbar)
        szr_bar.AddSpacer(2)
        szr_bar.Add(btn_search)

        # Main Sizer
        self.szr_main = wx.BoxSizer(wx.VERTICAL)
        self.szr_main.Add(szr_bar, flag=wx.EXPAND)
        self.szr_main.AddSpacer(1)
        self.szr_main.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), flag=wx.EXPAND)
        self.szr_main.Add(self.wgt_notebook, proportion=1, flag=wx.EXPAND)

        self.SetSizer(self.szr_main)

    def evt_button_no_focus(self, event):
        """Prevents focus from being called on the buttons

            Args:
                event: A focus event
        """
        pass

    def evt_search(self, *args):
        """Search for a part number and call open_parts_tab before emptying the searchbar

            Args:
                args[0]: Either None or a button click event
        """

        # Ensure there is something in the search bar before searching
        if self.wgt_searchbar.GetValue().strip():
            self.wgt_notebook.open_parts_tab(self.wgt_searchbar.GetValue())

        # Empty the searchbar
        self.wgt_searchbar.SetValue("")


class PaneLogin(wx.Panel):
    """Master pane that deals with login behaviour for the application.

        Args:
            parent (ptr): Reference to the wx.object this panel belongs to
            sizer_landing (ptr): Reference to the sizer (of the parent) the landing pane belongs to
            pane_landing (ptr): Reference to the landing pane

        Attributes:
            parent (ptr): Reference to the wx.object this panel belongs to
    """

    def __init__(self, parent, sizer_landing, pane_landing):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetDoubleBuffered(True)  # Remove slight strobing on failed login

        self.parent = parent

        # Widget that controls user login auth - currently set to debug (no auth) for testing and dev
        login_panel = login.LoginDebug(self, sizer_landing, pane_landing)

        # Main Sizer
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.AddStretchSpacer()
        sizer_main.Add(login_panel, flag=wx.CENTER)
        sizer_main.AddStretchSpacer()

        # Set main sizer
        self.SetSizer(sizer_main)
