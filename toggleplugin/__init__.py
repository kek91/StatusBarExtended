# Class for enabling/disabling StatusBarExtended

from fman import DirectoryPaneCommand, \
 show_status_message, load_json, save_json
import json
from statusbarextended import StatusBarExtended

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
                StatusBarExtended.refresh(self)
        else:
            save_json('StatusBarExtended.json', '{"enabled": true}')
            StatusBarExtended.refresh(self)
