# Override toggle_selection() core method to automatically
# compute and instantly display combined filesize for selected files

from fman import DirectoryPaneCommand, load_json
import json
from statusbarextended import StatusBarExtended

class _CorePaneCommand(DirectoryPaneCommand):
    def toggle_selection(self):
        file_under_cursor = self.pane.get_file_under_cursor()
        if file_under_cursor:
            self.pane.toggle_selection(file_under_cursor)

class ToggleSelection(_CorePaneCommand):
    def __call__(self):
        self.toggle_selection()
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.show_selected_files(self)
