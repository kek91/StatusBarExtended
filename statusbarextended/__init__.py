# Main class for StatusBarExtended

from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, show_alert
from os import stat, path, getenv
import json
import glob
from byteconverter import ByteConverter
#from PyQt5.QtWidgets import QApplication

def convert_bytes(n):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return "%3.1f %s" % (n, x)
        n /= 1024.0

class StatusBarExtended(DirectoryPaneListener):

    def refresh(self):

        pane = self.pane.id
        statusbar_pane = ""

        pane_show_hidden_files = load_json('Panes.json')[pane]['show_hidden_files']
        pane_show_hidden_files = "✓" if pane_show_hidden_files == True else "X"

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
        if(pane == self.pane.window.get_panes()[0].id):
            statusbar_pane += "Pane: Left     "
        else:
            statusbar_pane += "Pane: Right     "
        statusbar_pane += "" + pane_show_hidden_files + "     "
        statusbar_pane += "Dirs: " + str(dir_folders) + "     "
        if dir_files > 0:
            statusbar_pane += "Files: " + str(dir_files) + "     "
            statusbar_pane += "Size: " + str(bc.calc()) + "     "

        show_status_message(statusbar_pane, 5000)


    def show_selected_files(self):
        selected = self.pane.get_selected_files()
        dir_folders = 0
        dir_files = 0
        dir_filesize = 0

        if selected:
            for f in selected:
                if path.isdir(f):
                    dir_folders += 1
                else:
                    dir_files += 1
                    dir_filesize += stat(f).st_size

            bc = ByteConverter(dir_filesize)
            statusbar = str(dir_folders) + " directories, "
            statusbar += str(dir_files) + " files "
            statusbar += "selected - "
            statusbar += "total filesize: " + str(bc.calc())
            show_status_message(statusbar)

        else:
            StatusBarExtended.refresh(self)


    def on_path_changed(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.refresh(self)
