# Class for enabling/disabling StatusBarExtended

from fman import DirectoryPaneCommand, show_status_message
import statusbarextended        as SBE
import statusbarextended_config as SBEcfg

class ToggleStatusBarExtended(DirectoryPaneCommand):
    def __call__(self):
        cfg = SBEcfg.SingletonConfig()
        cfgCurrent, exit_status = cfg.loadConfig()
        if  cfgCurrent is None:
            return
        if  cfgCurrent["Enabled"] == True:
            cfgCurrent["Enabled"]  = False
            cfg.saveConfig(cfgCurrent)
            show_status_message("Disabled StatusBarExtended", 1)
        else:
            cfgCurrent["Enabled"]  = True
            cfg.saveConfig(cfgCurrent)
            SBE.StatusBarExtended.refresh(self)
