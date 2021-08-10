# Main class for StatusBarExtended

from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, PLATFORM
from fman.url import as_url, as_human_readable
from fman.fs import is_dir, query
from core.commands.util import is_hidden # works on file_paths, not urls
import glob
from byteconverter import ByteConverter
#from PyQt5.QtWidgets import QApplication
import statusbarextended_config as SBEcfg

class Just: # Justify elements in the status bar
    Fd = 5  # Justify Folder format: 5 symbols — up to 9,999
    Fl = 5  # Justify File   format: 5 symbols — up to 9,999
    Sz = 7  # Justify Size   format: 7 symbols — up to 999.0 b

class StatusBarExtended(DirectoryPaneListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_first_path_change = True

    def refresh(self):

        panes            = self.pane.window.get_panes()
        pane_id          = panes.index(self.pane)
        statusbar_pane   = ""

        cfg_show_hidden_files  = load_json('Panes.json')[pane_id]['show_hidden_files']
        pane_show_hidden_files = "◻" if cfg_show_hidden_files else "◼" # alt: 👁🐵🙈◎◉✓✗
        cur_dir_url      = self.pane.get_path()
        current_dir      = as_human_readable(cur_dir_url)
        dir_folders      = 0
        dir_files        = 0
        dir_filesize     = 0
        dir_files_in_dir      = glob.glob(current_dir + "/*")
        if PLATFORM == 'Windows':   # .dotfile=regular (use 'hidden' attr to hide)
            dir_files_in_dir += glob.glob(current_dir + "/.*")
        elif cfg_show_hidden_files: # .dotfile=hidden
            dir_files_in_dir += glob.glob(current_dir + "/.*")
        f_url            = ""

        if dir_files_in_dir:
            if cfg_show_hidden_files:
                for f in dir_files_in_dir:
                    f_url = as_url(f)
                    if is_dir(f_url):
                        dir_folders      += 1
                    else:
                        dir_files        += 1
                        try:
                            dir_filesize += query(f_url, 'size_bytes')
                        except Exception as e:
                            continue
            else:
                for f in dir_files_in_dir:
                    f_url = as_url(f)
                    if not is_hidden(f):
                        if is_dir(f_url):
                            dir_folders      += 1
                        else:
                            dir_files        += 1
                            try:
                                dir_filesize += query(f_url, 'size_bytes')
                            except Exception as e:
                                continue

        bc = ByteConverter(dir_filesize)
        dir_foldK = str("{0:,}".format(dir_folders)) # to ','→' ' add .replace(',', ' ')
        dir_fileK = str("{0:,}".format(dir_files))
        if(self.pane == self.pane.window.get_panes()[0]):
            statusbar_pane      += "◧"
        else:
            statusbar_pane      += "◨"
        statusbar_pane          += "   "     + pane_show_hidden_files             + "     "
        if     dir_folders > 0:
            statusbar_pane      += "Dirs: "  +      dir_foldK.rjust(Just.Fd, ' ') + "  "
            if dir_folders <= 9999:
                statusbar_pane  += " "
        else:
            statusbar_pane      += "      "  +             ''.rjust(Just.Fd, ' ') + "   "
        if     dir_files > 0:
            statusbar_pane      += "Files: " +      dir_fileK.rjust(Just.Fl, ' ') + "   "
            if dir_files <= 9999:
                statusbar_pane  += " "
        else:
            statusbar_pane      += "       " +             ''.rjust(Just.Fl, ' ') + "    "
        statusbar_pane          += "  Size: "+ str(bc.calc()).rjust(Just.Sz, ' ') + "   "
        #            to align with "∑ Size: "

        show_status_message(statusbar_pane, 5000)

    def show_selected_files(self):
        panes           = self.pane.window.get_panes()
        pane_id         = panes.index(self.pane)
        cfg_show_hidden_files  = load_json('Panes.json')[pane_id]['show_hidden_files']
        selected        = self.pane.get_selected_files()
        dir_folders     = 0
        dir_files       = 0
        dir_filesize    = 0

        if selected:
            if cfg_show_hidden_files:
                for f in selected:
                    if is_dir(f):
                        dir_folders     += 1
                    else:
                        dir_files       += 1
                        dir_filesize    += query(f, 'size_bytes')
            else:
                for f in selected:
                    if not is_hidden(as_human_readable(f)):
                        if is_dir(f):
                            dir_folders     += 1
                        else:
                            dir_files       += 1
                            dir_filesize    += query(f, 'size_bytes')

            bc = ByteConverter(dir_filesize)
            dir_foldK  = "{0:,}".format(dir_folders)
            dir_fileK  = "{0:,}".format(dir_files)
            statusbar  = "Selected* "
            if     dir_folders > 0:
                statusbar      += "Dirs: "   +      dir_foldK.rjust(Just.Fd, ' ') + "  "
                if dir_folders <= 9999:
                    statusbar  += " "
            else:
                statusbar      += "      "   +             ''.rjust(Just.Fd, ' ') + "   "
            if     dir_files > 0:
                statusbar      += "Files: "  +      dir_fileK.rjust(Just.Fl, ' ') + "   "
                if dir_files <= 9999:
                    statusbar  += " "
            else:
                statusbar      += "       "  +             ''.rjust(Just.Fl, ' ') + "    "
            statusbar          += "∑ Size: " + str(bc.calc()).rjust(Just.Sz, ' ') + "   "
            show_status_message(statusbar)

        else:
            StatusBarExtended.refresh(self)


    def on_path_changed(self):
        if self.pane.get_path()=='null://': # ignore strange paths on launch
            return
        panes = self.pane.window.get_panes()
        if self.is_first_path_change: # ignore the right pane on start
            self.is_first_path_change = False
            if panes.index(self.pane) == 1:
                return
        cfg = SBEcfg.SingletonConfig()
        cfgCurrent, exit_status = cfg.loadConfig()

        if  cfgCurrent is None:
            return
        if  cfgCurrent["Enabled"] == True:
           StatusBarExtended.refresh(self)
