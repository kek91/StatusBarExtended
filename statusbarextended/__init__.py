# Main class for StatusBarExtended

from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, save_json, show_alert
from fman.url import as_url, as_human_readable
from fman.fs import is_dir, query
import json
import glob
from byteconverter import ByteConverter
#from PyQt5.QtWidgets import QApplication

class Just: # Justify elements in the status bar
    Fd = 5  # Justify Folder format: 5 symbols — up to 9,999
    Fl = 5  # Justify File   format: 5 symbols — up to 9,999
    Sz = 7  # Justify Size   format: 7 symbols — up to 999.0 b

class StatusBarExtended(DirectoryPaneListener):

    def refresh(self):

        pane = self.pane.window.get_panes().index(self.pane)
        statusbar_pane = ""

        pane_show_hidden_files = load_json('Panes.json')[pane]['show_hidden_files']
        pane_show_hidden_files = "◻" if pane_show_hidden_files == True else "◼"
        #alternative icons: 👁◎◉✓✗
        cur_dir_url      = self.pane.get_path()
        current_dir      = as_human_readable(cur_dir_url)
        dir_folders      = 0
        dir_files        = 0
        dir_filesize     = 0
        dir_files_in_dir = glob.glob(current_dir + "/*")
        f_url            = ""

        if dir_files_in_dir:
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

        bc = ByteConverter(dir_filesize)
        dir_foldK = str("{0:,}".format(dir_folders)) # to ','→' ' add .replace(',', ' ')
        dir_fileK = str("{0:,}".format(dir_files))
        if(self.pane == self.pane.window.get_panes()[0]):
            statusbar_pane      += "◧"
        else:
            statusbar_pane      += "◨"
        statusbar_pane          += "   "     + pane_show_hidden_files             + "     "
        if     dir_folders > 0:
            statusbar_pane      += "Dirs:"   +      dir_foldK.rjust(Just.Fd, ' ') + "  "
            if dir_folders <= 9999:
                statusbar_pane  += " "
        else:
            statusbar_pane      += "     "   +             ''.rjust(Just.Fd, ' ') + "   "
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
        selected        = self.pane.get_selected_files()
        dir_folders     = 0
        dir_files       = 0
        dir_filesize    = 0

        if selected:
            for f in selected:
                if is_dir(f):
                    dir_folders     += 1
                else:
                    dir_files       += 1
                    dir_filesize    += query(f, 'size_bytes')

            bc = ByteConverter(dir_filesize)
            dir_foldK  = str("{0:,}".format(dir_folders))
            dir_fileK  = str("{0:,}".format(dir_files))
            statusbar  = "Selected* "
            if     dir_folders > 0:
                statusbar      += "Dirs:"    +      dir_foldK.rjust(Just.Fd, ' ') + "  "
                if dir_folders <= 9999:
                    statusbar  += " "
            else:
                statusbar      += "     "    +             ''.rjust(Just.Fd, ' ') + "   "
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
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.refresh(self)
