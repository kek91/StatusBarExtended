from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, \
 show_alert
from os import stat, path, getenv, listdir
import json
import glob

def convert_bytes(n):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return "%3.1f %s" % (n, x)
        n /= 1024.0

class ToggleStatusBarExtended(DirectoryPaneCommand):
    def __call__(self):
        appData = getenv('APPDATA')
        if path.isfile(appData + "\\fman\\Plugins\\User\\StatusBarExtended (Windows).json"):
            statusBarExtendedEnabled = load_json('StatusBarExtended.json')
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                statusBarExtendedEnabled = 'true'
            else:
                statusBarExtendedEnabled = 'false'
        else:
            statusBarExtendedEnabled = 'false'

        if statusBarExtendedEnabled == 'true':
            save_json('StatusBarExtended.json', '{"enabled": false}')
            show_status_message("Disabled StatusBarExtended", 3)
        else:
            save_json('StatusBarExtended.json', '{"enabled": true}')
            show_status_message("Enabled StatusBarExtended", 3)

        #show_alert("Toggled StatusBarExtended plugin")

class StatusBarExtended(DirectoryPaneListener):
    def on_path_changed(self):
        appData = getenv('APPDATA')
        if path.isfile(appData + "\\fman\\Plugins\\User\\StatusBarExtended (Windows).json"):
            statusBarExtendedEnabled = load_json('StatusBarExtended.json')
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                panes = self.pane.window.get_panes()
                pane1 = panes[0].id
                pane2 = panes[1].id

                statusbar_pane1 = "" #str(pane1) + "\t"
                statusbar_pane2 = "" #str(pane2) + "\t"

                pane1_show_hidden_files = load_json('Panes.json')[pane1]['show_hidden_files']
                pane1_show_hidden_files = "Show" if pane1_show_hidden_files == True else "Hide"
                statusbar_pane1 += "Hidden files: " + pane1_show_hidden_files + "\t\t"

                pane2_show_hidden_files = load_json('Panes.json')[pane2]['show_hidden_files']
                pane2_show_hidden_files = "Show" if pane2_show_hidden_files == True else "Hide"
                statusbar_pane2 += "Hidden files: " + pane2_show_hidden_files + "\t\t"

                for p in panes:
                    current_dir = p.get_path()
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
                                dir_filesize += stat(f).st_size
                    if(p.id == pane1):
                        statusbar_pane1 += "Subfolders: " + str(dir_folders) + "\t\t"
                        statusbar_pane1 += "Files: " + str(dir_files) + "\t\t"
                        statusbar_pane1 += "Filesize: " + str(convert_bytes(dir_filesize)) + "\t\t"
                    else:
                        statusbar_pane2 += "Subfolders: " + str(dir_folders) + "\t\t"
                        statusbar_pane2 += "Files: " + str(dir_files) + "\t\t"
                        statusbar_pane2 += "Filesize: " + str(convert_bytes(dir_filesize)) + "\t\t"

                show_status_message(statusbar_pane1 + "---\t\t" + statusbar_pane2, 5000)
                clear_status_message()

                #show_status_message('{:>12}  {:>12}  {:>12}'.format(statusbar_pane1, ' - - ', statusbar_pane2))
