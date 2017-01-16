from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, show_alert
from os import stat, path, getenv, listdir
import json
import glob

def convert_bytes(n):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return "%3.1f %s" % (n, x)
        n /= 1024.0


class ShowStatusBarExtended(DirectoryPaneListener):
    def refresh(self):
        panes = self.pane.window.get_panes()
        pane1 = panes[0].id
        pane2 = panes[1].id
        statusbar_pane1 = ""
        statusbar_pane2 = ""

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



class ToggleStatusBarExtended(DirectoryPaneCommand):
    def __call__(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                save_json('StatusBarExtended.json', '{"enabled": false}')
                show_status_message("Disabled StatusBarExtended", 1)
            else:
                save_json('StatusBarExtended.json', '{"enabled": true}')
                ShowStatusBarExtended.refresh(self)
        else:
            save_json('StatusBarExtended.json', '{"enabled": true}')
            ShowStatusBarExtended.refresh(self)



class StatusBarExtended(DirectoryPaneListener):
    def on_path_changed(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                ShowStatusBarExtended.refresh(self)
