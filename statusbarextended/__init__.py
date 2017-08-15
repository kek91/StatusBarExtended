# Main class for StatusBarExtended

from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, show_alert
from os import stat, path, getenv
import json
import glob
from byteconverter import ByteConverter
#from PyQt5.QtWidgets import QApplication

class StatusBarExtended(DirectoryPaneListener):

    def refresh(self):

        justFd = 5 # Justify Folder format: up to 9,999
        justFl = 5 # Justify Folder format: up to 9,999
        justSz = 7 # Justify Size format:   up to 999.0 b

        pane = self.pane.window.get_panes().index(self.pane)
        statusbar_pane = ""

        pane_show_hidden_files = load_json('Panes.json')[pane]['show_hidden_files']
        pane_show_hidden_files = "◻" if pane_show_hidden_files == True else "◼"
        #alternative icons: 👁◎◉✓✗
        current_dir = self.pane.get_path()
        dir_folders = 0
        dir_files = 0
        dir_filesize = 0
        dir_files_in_dir = glob.glob(current_dir + "/*")
        if dir_files_in_dir:
            for f in dir_files_in_dir:
                if path.isdir(f):
                    dir_folders += 1
                else:
                    dir_files += 1
                    try:
                        dir_filesize += stat(f).st_size
                    except Exception as e:
                        continue

        bc = ByteConverter(dir_filesize)
        dir_foldersK	= str("{0:,}".format(dir_folders))	# old use str(dir_folders)
        dir_filesK  	= str("{0:,}".format(dir_files))  	# ' ' instead of ',' .replace(',', ' ')
        if(self.pane == self.pane.window.get_panes()[0]):
            statusbar_pane += "Pane: Left  "
        else:
            statusbar_pane += "Pane: Right "
        statusbar_pane += ""	+ pane_show_hidden_files	+ "    "
        if dir_folders == 0:
            statusbar_pane += "      "  + ''.rjust(justFd, ' ')    + "    "
        elif dir_folders > 9999:
            statusbar_pane += "Dirs: "  + dir_foldersK.rjust(justFl, ' ')    + "   "
        else:
            statusbar_pane += "Dirs: "  + dir_foldersK.rjust(justFl, ' ')    + "    "
        if dir_files > 0:
            if dir_files > 9999:
                statusbar_pane += "Files: "	+ dir_filesK.rjust(justFd, ' ')	+ "   "
            else:
                statusbar_pane += "Files: " + dir_filesK.rjust(justFd, ' ')      + "    "
        else:
            statusbar_pane += "       " + ''.rjust(justFl, ' ')      + "    "
        statusbar_pane += "Size: "  + str(bc.calc()).rjust(justSz, ' ')  + "    "

        show_status_message(statusbar_pane, 5000)


    def show_selected_files(self):
        selected    	= self.pane.get_selected_files()
        dir_folders 	= 0
        dir_files   	= 0
        dir_filesize	= 0

        if selected:
            for f in selected:
                if path.isdir(f):
                    dir_folders += 1
                else:
                    dir_files   	+= 1
                    dir_filesize	+= stat(f).st_size

            bc = ByteConverter(dir_filesize)
            dir_foldersK    = str("{0:,}".format(dir_folders))  # old use str(dir_folders)
            dir_filesK      = str("{0:,}".format(dir_files))    # ' ' instead of ',' .replace(',', ' ')
            statusbar = "Selected*   "
            statusbar += "Dirs: "  + dir_foldersK.rjust(justFd, ' ')    + "   "
            statusbar += "Files: " + dir_filesK.rjust(justFl, ' ')      + "  "
            statusbar += "∑ Size: " + str(bc.calc()).rjust(justSz, ' ')
            show_status_message(statusbar)

        else:
            StatusBarExtended.refresh(self)


    def on_path_changed(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.refresh(self)
