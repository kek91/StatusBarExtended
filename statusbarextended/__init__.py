# Main class for StatusBarExtended

from fman import DirectoryPaneCommand, DirectoryPaneListener, \
 show_status_message, load_json, PLATFORM
from fman.url import as_url, as_human_readable as as_path
from fman.fs import is_dir, query
from core.commands.util import is_hidden # works on file_paths, not urls
import glob
import re
from byteconverter import ByteConverter
#from PyQt5.QtWidgets import QApplication
import statusbarextended_config as SBEcfg


class StatusBarExtended(DirectoryPaneListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_first_path_change = True

    def refresh(self, cfg):

        panes            = self.pane.window.get_panes()
        pane_id          = panes.index(self.pane)
        statusbar_pane   = ""

        cfg_show_hidden_files  = load_json('Panes.json')[pane_id]['show_hidden_files']
        pane_show_hidden_files = cfg['SymbolHiddenF'][0] if cfg_show_hidden_files else\
                                 cfg['SymbolHiddenF'][1]
        cur_dir_url      = self.pane.get_path()
        current_dir      = as_path(cur_dir_url)
        current_dir_gnorm= re.sub(r'(?P<bracket>\[|\]|\?|\*)',r'[\g<bracket>]',current_dir) # bracket the brackets, asterisks and question marks in paths to match them literaly instead of treating them as special globl characters
        dir_folders      = 0
        dir_files        = 0
        dir_filesize     = 0
        dir_files_in_dir      = glob.glob(current_dir_gnorm + "/*")
        if PLATFORM == 'Windows' and not cfg['HideDotfile']:
            # .dotfiles=regular (always shown unless have a 'hidden' attr)
            dir_files_in_dir += glob.glob(current_dir_gnorm + "/.*")
        elif cfg_show_hidden_files: # .dotfile=hidden (internal option shows)
            dir_files_in_dir += glob.glob(current_dir_gnorm + "/.*")
        f_url            = ""
        aboveMax         = False

        if not dir_files_in_dir:
            pass
        elif len(dir_files_in_dir) > cfg['MaxGlob']:
            aboveMax       = True
        else:
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

        bc   = ByteConverter(dir_filesize)
        bcc  = str(bc.calc())
        maxG = str("{0:,}".format(cfg['MaxGlob']))
        jFd  = cfg['Justify']['folder']
        jFl  = cfg['Justify']['file']
        jSz  = cfg['Justify']['size']
        lFd  = cfg['Label'  ]['folder']+' '
        lFl  = cfg['Label'  ]['file']  +' '
        lSz  = cfg['Label'  ]['size']  +' '
        if cfg['Hide0Label'] == True:
            lFd_sp = ''.rjust(len(lFd),' ')
            lFl_sp = ''.rjust(len(lFl),' ')
        else:
            lFd_sp = lFd
            lFl_sp = lFl
        dir_foldK = str("{0:,}".format(dir_folders)) # to ','→' ' add .replace(',', ' ')
        dir_fileK = str("{0:,}".format(dir_files))
        if(self.pane == panes[0]):
            statusbar_pane      += cfg['SymbolPane'][0]
        else:
            statusbar_pane      += cfg['SymbolPane'][1]
        statusbar_pane          += "   "    + pane_show_hidden_files    + "     "
        if     dir_folders > 0:
            statusbar_pane      += lFd      + dir_foldK.rjust(jFd, ' ') + "  "
            if dir_folders <= 9999:
                statusbar_pane  +=                                           " "
        elif aboveMax:
            statusbar_pane      += lFd      +     ' + '.rjust(jFd, ' ') + "   "
        else:
            statusbar_pane      += lFd_sp   +        ''.rjust(jFd, ' ') + "   "
        if     dir_files > 0:
            statusbar_pane      += lFl      + dir_fileK.rjust(jFl, ' ') + "   "
            if dir_files <= 9999:
                statusbar_pane  +=                                            " "
        elif aboveMax:
            statusbar_pane      += lFl+">"  +      maxG.rjust(jFl, ' ') + "    "
        else:
            statusbar_pane      += lFl_sp   +        ''.rjust(jFl, ' ') + "    "
        if not aboveMax:
            statusbar_pane      += "  "+lSz +       bcc.rjust(jSz, ' ') + "   "
            #        to align with "∑ "

        show_status_message(statusbar_pane, 5000)

    def show_selected_files(self, cfg):
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
                    if not is_hidden(as_path(f)):
                        if is_dir(f):
                            dir_folders     += 1
                        else:
                            dir_files       += 1
                            dir_filesize    += query(f, 'size_bytes')

            bc  = ByteConverter(dir_filesize)
            bcc = str(bc.calc())
            jFd = cfg['Justify']['folder']
            jFl = cfg['Justify']['file']
            jSz = cfg['Justify']['size']
            lFd = cfg['Label'  ]['folder']+' '
            lFl = cfg['Label'  ]['file']  +' '
            lSz = cfg['Label'  ]['size']  +' '
            if cfg['Hide0Label'] == True:
                lFd_sp = ''.rjust(len(lFd),' ')
                lFl_sp = ''.rjust(len(lFl),' ')
            else:
                lFd_sp = lFd
                lFl_sp = lFl
            dir_foldK  = "{0:,}".format(dir_folders)
            dir_fileK  = "{0:,}".format(dir_files)
            statusbar  = "Selected* "
            if     dir_folders > 0:
                statusbar      += lFd      + dir_foldK.rjust(jFd, ' ') + "  "
                if dir_folders <= 9999:
                    statusbar  +=                                           " "
            else:
                statusbar      += lFd_sp   +        ''.rjust(jFd, ' ') + "   "
            if     dir_files > 0:
                statusbar      += lFl      + dir_fileK.rjust(jFl, ' ') + "   "
                if dir_files <= 9999:
                    statusbar  += " "
            else:
                statusbar      += lFl_sp   +        ''.rjust(jFl, ' ') + "    "
            statusbar          += "∑ "+lSz +       bcc.rjust(jSz, ' ') + "   "
            show_status_message(statusbar)

        else:
            StatusBarExtended.refresh(self, cfg)


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
           StatusBarExtended.refresh(self, cfgCurrent)
