# -*- coding: utf-8 -*-
"""This module defines panes - master panels that act as direct children of the progenitor frame"""

import wx
import os
import PyPDF2


class DummyFileDrop(wx.FileDropTarget):
    """Dummy class to catch files dropped onto the add documents button

        Args:
            parent (ref): Reference to the parent wx.object
            target_function (ref): Reference to the intended function to trigger and pass filepaths to

        Attributes:
            parent (ref): Reference to the parent wx.object
            target_function (ref): Reference to the intended function to trigger and pass filepaths to
    """

    def __init__(self, parent, target_function):
        """Constructor"""
        wx.FileDropTarget.__init__(self)

        self.window = parent
        self.target_function = target_function

    def OnDropFiles(self, x, y, file_paths):
        """Trigger target_function when files are dropped onto this widget

            Args:
                x (int): Integer x position that the file(s) were dropped on
                y (int): Integer y position that the file(s) were dropped on
                file_paths (list: str): A list of string paths for the file(s) dropped onto this widget
        """

        self.target_function(file_paths)

        return True


class PaneMain(wx.Panel):
    """Main panel class. Controls the behaviour of the application

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
                ls_paths (list: str): List of string representation of full filepaths to PDF files to merge
                ls_files (list: str): List of string representation of filenames of PDF files to merge
        """

    def __init__(self, parent, *args, **kwargs):
        """Constructor"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Empty Lists
        self.ls_paths = []
        self.ls_files = []

        # Button widget objects and their binds
        btn_add = wx.Button(self, size=(75, 25), label="ADD")
        self.Bind(wx.EVT_BUTTON, self.evt_add, btn_add)
        btn_merge = wx.Button(self, size=(75, 25), label="MERGE")
        self.Bind(wx.EVT_BUTTON, self.evt_submit, btn_merge)
        btn_clear = wx.Button(self, size=(75, 25), label="CLEAR")
        self.Bind(wx.EVT_BUTTON, self.evt_clear, btn_clear)

        # Buttons Sizer
        self.szr_buttons = wx.BoxSizer(wx.VERTICAL)
        self.szr_buttons.Add(btn_add, flag=wx.CENTER)
        self.szr_buttons.Add(btn_merge, flag=wx.CENTER)
        self.szr_buttons.AddSpacer(5)
        self.szr_buttons.Add(wx.StaticText(self), proportion=1)
        self.szr_buttons.Add(btn_clear, flag=wx.CENTER | wx.BOTTOM)

        # Added PDF list display pane
        self.wgt_added_docs = wx.TextCtrl(self, size=(750, 1500), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.EXPAND)

        # Hook in drag-drop functionality to PDF list display pane
        self.wgt_added_docs.SetDropTarget(DummyFileDrop(self, self.evt_dragged_files))

        # Overall Sizer
        szr_main = wx.BoxSizer(wx.HORIZONTAL)
        szr_main.Add(self.szr_buttons, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        szr_main.Add(self.wgt_added_docs, proportion=3, flag=wx.EXPAND)

        self.SetSizer(szr_main)

    def update_files(self, new_paths):
        """Add file(s) to list of files to merge

            Args:
                new_paths (list: str): List of string representation of full filepaths new PDF files to add to the list
        """

        # Extend the internal lists of the files
        self.ls_paths.extend(new_paths)
        self.ls_files.extend([os.path.basename(file_path) for file_path in new_paths])

        # Update the widget to display new files list
        self.wgt_added_docs.SetValue("\n".join(self.ls_files))

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

            # Add selected files to the list of PDFs
            self.update_files(file_dialog.GetPaths())

    def evt_submit(self, event):
        """Merges the intended PDF file

            Args:
                event: A button event
        """

        # Check if the list is populated
        if self.ls_paths:
            # Determine save-to location
            with wx.FileDialog(None, "Save",
                               wildcard="pdf files (*.pdf)|*.pdf",
                               style=wx.FD_SAVE) as file_dialog:

                # Check if the user changed their mind about importing
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return

                # Assemble PDF
                try:
                    pdf_merger = PyPDF2.PdfFileMerger(strict=False)
                    for document in self.ls_paths:
                        pdf_merger.append(document)

                    # Save merged file to selected location
                    pdf_merger.write(file_dialog.GetPath())

                    # Close merging gracefully
                    pdf_merger.close()
                except Exception as e:
                    dialog = wx.RichMessageDialog(self,
                                                  caption="An exception occurred",
                                                  message=str(e),
                                                  style=wx.OK | wx.ICON_ERROR)
                    dialog.ShowModal()
                    dialog.Destroy()
                    return

                # Merge Success Confirmation
                dialog = wx.RichMessageDialog(self,
                                              caption="PDF Merged",
                                              message="The PDF has been successfully saved to:\n\n" +
                                                      file_dialog.GetPath(),
                                              style=wx.OK | wx.ICON_INFORMATION)
                dialog.ShowModal()
                dialog.Destroy()

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

    def evt_dragged_files(self, file_paths):
        """Trigger dialog to add new documents

            Args:
                file_paths (list: str): A list of string paths for the file(s) dropped onto this widget
        """

        # Add dragged files to the list of PDFs
        self.update_files(self.only_pdf(file_paths))

    @staticmethod
    def only_pdf(path_list):
        """Convert a list of filepaths to a list of filepaths containing only PDFs

            Args:
                path_list (list: str): List of string representations of full filepaths
        """

        return [pdf for pdf in path_list if os.path.splitext(pdf)[1] == ".pdf"]
