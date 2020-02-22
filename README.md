# Aria PDF Merger
Simple Application to Merge PDF Files

## Working Executable
A working executable can be downloaded [here](https://github.com/AncientAbysswalker/Aria/raw/master/build/Aria.exe).

## Problem Statement
Most PDF modification and merging tools cost a fair amount or are poorly-implemented web solutions. This creates a 
problem when you need to merge several, or in my case potentially hundreds of PDF files.

## Solution
After spending far too much time dealing with other "free" solutions to this issue, I decided to see if I could 
tackle the problem myself. The result is this simple application that I will continue to use moving forwards. The 
application has only three buttons that trigger functions for the program:

* ADD: Adds any number of PDFs to the list of PDFs to merge
* MERGE: Request save destination and save merged file there
* CLEAR: Reset list of PDFs to merge

The box encompassing the right portion of the screen is where all the PDFs currently slotted for merge are listed. This 
box has functionality so that PDF files dragged onto from the file explorer it will be added to the list the same as if 
using the ADD button.

![Window Preview](https://raw.githubusercontent.com/AncientAbysswalker/Aria/master/md/preview.png)
![Merge Save Confirmation](https://raw.githubusercontent.com/AncientAbysswalker/Aria/master/md/saved.png)

#### Origin of the Project Name
At the time of writing this program I was relatively annoyed with the available "free" solutions to merge PDFs. I 
considered the first successfully merged PDF to be the "siren song of a successfully merged PDF"; thus the name Aria. 
Yes, I realize that merging PDFs does not make any noise, but this is what popped unto my head and thus the name.