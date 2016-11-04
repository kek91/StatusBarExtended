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
        else:
            save_json('StatusBarExtended.json', '{"enabled": true}')

        show_alert("StatusBarExtended plugin enabled: " + str(statusBarExtendedEnabled))

class StatusBarExtended(DirectoryPaneListener):
    def on_path_changed(self):
        status_bar_message = ""

        str_showHiddenFiles = str(load_json('Panes.json')[self.pane.id]['show_hidden_files'])
        str_showHiddenFiles = "Show" if str_showHiddenFiles else "Hide"
        status_bar_message += "Hidden files: " + str_showHiddenFiles + "\t\t"

        '''
        float_selectedFilesSize = 0
        arr_selectedFiles = self.pane.get_selected_files()

        if arr_selectedFiles:
            int_selectedFilesAmount = len(arr_selectedFiles)
            status_bar_message += "Selection: " + int_selectedFilesAmount + " files\t\t"
            if int_selectedFilesAmount >= 1:
                for file in arr_selectedFiles:
                    float_selectedFilesSize = float_selectedFilesSize + stat(file).st_size

            status_bar_message += "Total size: " + convert_bytes(float_selectedFilesSize) + "\t\t"

        else:
            status_bar_message += "No files selected \t - \t"
        '''

        currentDir = self.pane.get_path()
        filesInDirAmount = 0
        filesInDirSize = 0
        filesInCurrentDir = glob.glob(currentDir+"/*.*")

        if filesInCurrentDir:
            for f in filesInCurrentDir:
                filesInDirAmount = filesInDirAmount + 1
                filesInDirSize = filesInDirSize + stat(f).st_size

        status_bar_message += "Files in directory: " + str(filesInDirAmount) + "\t\t"
        status_bar_message += "Total filesize: " + str(convert_bytes(filesInDirSize)) + "\t\t"

        show_status_message(status_bar_message)
