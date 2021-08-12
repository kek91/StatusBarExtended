# Class for configuring StatusBarExtended

from fman import ApplicationCommand, \
 show_prompt, show_alert, show_status_message, load_json, save_json, \
 PLATFORM, DATA_DIRECTORY, run_application_command
from fman.fs import exists, delete, move_to_trash
from fman.url import as_human_readable as as_path, as_url, join, splitscheme, basename, dirname
from collections import OrderedDict as odict

class SingletonConfig(object):
    def __new__(cls):
        """Create the global config singleton object or return the existing one."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonConfig, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self): # set the defaults only once
        if(self.__initialized): return
        self.__initialized = True
        self.setDefault()

    @classmethod
    def setDefault(cls): # set the defaults in a dictionary
        cls.Default                 = odict()
        cls.Default['Enabled']      = True      # enable plugin
        cls.Default['SizeDivisor']  = 1024.0    # binary file sizes
        cls.Default['MaxGlob']      = 5000      # skip large folders with as many items; 0=∞
        cls.Default['SymbolPane']   = ['◧','◨'] # Left/Right
        cls.Default['SymbolHiddenF']= ['◻','◼'] # Show/Hide hidden files
        cls.Default['HideDotfile']  = False     # hide non-hidden dotfiles on Windows
        cls.Default['Justify']      = odict({   # right-justification parameter
                    'folder'        : 5 ,
                    'file'          : 5 ,
                    'size'          : 7 })
        cls.msgTimeout = 5 # timeout in seconds for show_status_message

    @classmethod
    def loadConfig(cls):
        """Check StatusBarExtended.json for consistency/completeness, restore defaults on fail"""
        msg_t = cls.msgTimeout
        if hasattr(cls, 'locked_update'):
            show_status_message("StatusBarExtended: waiting for the config files to be updated, try again later...")
            return None, 'UpdateInProgress'
        cls.locked_update = True # ensure globally unique 'loadConfig' run so that e.g. we don't ask a user multiple times to delete corrupted configs

        cfgCurrent = load_json('StatusBarExtended.json') # within one fman session, it is guaranteed that multiple calls to load_json(...) with the same JSON name always return the same object, so save {} when deleting the files to force reload
        if type(cfgCurrent) not in (type(dict()), type(None)):
            # delete config files, fman's save_json can't replace types
            config_files       = ['StatusBarExtended.json']
            config_files.append(  'StatusBarExtended ('+PLATFORM+').json')
            user_settings_url  = join(as_url(DATA_DIRECTORY),'Plugins','User','Settings')
            user_input_allow   = ''
            prompt_msg_full    = ''
            corrupt_config     = []
            for f in config_files:
                f_url  = join(user_settings_url,f)
                f_path = as_path(f_url)

                if not exists(f_url):
                    continue

                excerpt    = str(load_json(f_path))[:100]
                prompt_msg = f_path \
                    + "\n  that begins with:"\
                    + "\n  " + excerpt
                corrupt_config.append({})
                corrupt_config[-1]['url' ] = f_url
                corrupt_config[-1]['path'] = f_path
                corrupt_config[-1]['prompt_msg'] = prompt_msg

            corrupt_count = len(corrupt_config)
            if corrupt_count: # delete corrupt config files with the user's permission
                prompt_msg_full += "Please enter 'y' or 'yes' or '1' (without the quotes) to delete " + str(corrupt_count) + " corrupt plugin config file" \
                    + ("\n" if corrupt_count==1 else "s\n") \
                    + "with incompatible data type " + str(type(cfgCurrent)) + '\n'\
                    + "(all settings will be reset to their defaults)\n"
                for corrupt_file_dict in corrupt_config:
                    prompt_msg_full += '\n' + corrupt_file_dict['prompt_msg'] + '\n'
                user_input_allow, ok = show_prompt(prompt_msg_full, default=user_input_allow)
                if ok and user_input_allow in ('y', 'yes', '1'):
                    _reset = False
                    for corrupt_file_dict in corrupt_config:
                        f_url  = corrupt_file_dict['url' ]
                        f_path = corrupt_file_dict['path']
                        try:
                            move_to_trash(f_url)
                        except Exception as e:
                            show_status_message("StatusBarExtended: failed to move to trash — " + f_path + " — with exception " + repr(e), msg_t)
                            pass

                        if not exists(f_url):
                            show_status_message("StatusBarExtended: moved to trash — " + f_path, msg_t)
                            _reset = True
                        else:
                            show_status_message("StatusBarExtended: failed to move to trash, deleting — " + f_path, msg_t)
                            try:
                                delete(f_url)
                            except Exception as e:
                                show_status_message("StatusBarExtended: failed to delete — " + f_path + " — with exception " + repr(e), msg_t)
                                pass

                            if not exists(f_url):
                                show_status_message("StatusBarExtended: deleted — " + f_path, msg_t)
                                _reset = True
                            else:
                                show_alert("StatusBarExtended: failed to move to trash or delete — " + f_path + "\nPlease, delete it manually")
                                del cls.locked_update
                                return None, 'ConfigDeleteFail'
                    if _reset == True: # can save_json only when both files are deleted, otherwise there is a format mismatch ValueError
                        cls.saveConfig({})
                        cfgCurrent = load_json('StatusBarExtended.json')
                else: # user canceled or didn't enter y/1
                    show_status_message("StatusBarExtended: you canceled the deletion of the corrupted config files", msg_t)
                    del cls.locked_update
                    return None, 'Canceled'
            else: # can't find the config files
                show_alert("StatusBarExtended: can't find the corrupt config files:\n" \
                    + str(config_files) + "\n @ " + as_path(user_settings_url) \
                    + "\nMaybe their default location changed, please, delete them manually")
                del cls.locked_update
                return None, 'CorruptConfigNotFound'

        reload = False
        if (cfgCurrent is None) or (cfgCurrent == {}): # empty file or empty dictionary (corrupt configs deleted and replaced with {}), save defaults to the config file
            cfgCurrent = dict()
            for key in cls.Default:
                cfgCurrent[key] = cls.Default[key]
            reload = True

        if type(cfgCurrent) is dict:
            for key in cls.Default: # Fill in missing default values (e.g. in older installs)
                if key not in cfgCurrent:
                    cfgCurrent[key] = cls.Default[key]
                    reload = True
        if reload:
            cls.saveConfig(cfgCurrent)
            cfgCurrent = load_json('StatusBarExtended.json')

        if type(cfgCurrent) is dict: # check for still missing keys
            missing_keys=[]
            for key in cls.Default:
                if key in cfgCurrent:
                    continue
                missing_keys.append(key)
            if len(missing_keys):
                show_status_message("StatusBarExtended: config files are missing some required keys:" + str(missing_keys) + " Maybe try to reload?", msg_t)
                del cls.locked_update
                return None, 'MissingKeys'
            else:
                del cls.locked_update
                return cfgCurrent, 'Success'
        else:
            show_status_message("StatusBarExtended: couldn't fix config files, maybe try to reload?", msg_t)
            del cls.locked_update
            return None, 'UnknownError'

    @classmethod
    def saveConfig(cls, save_data):
        save_json('StatusBarExtended.json', save_data)

class ConfigureStatusBarExtended(ApplicationCommand):
    aliases = ('StatusBarExtended: configure',)

    def __call__(self):
        cfg = SingletonConfig()
        self.cfgCurrent, exit_status = cfg.loadConfig()
        if self.cfgCurrent is None:
            return
        self.setEnabled(      cfg.Default['Enabled'])
        self.setSizeDivisor(  cfg.Default['SizeDivisor'])
        self.setMaxGlob(      cfg.Default['MaxGlob'])
        self.setSymbolPane(   cfg.Default['SymbolPane'])
        self.setSymbolHiddenF(cfg.Default['SymbolHiddenF'])
        self.setHideDotfile(  cfg.Default['HideDotfile'])
        self.setJustify(      cfg.Default['Justify'])
        cfg.saveConfig(self.cfgCurrent)
        run_application_command('view_configuration_status_bar_extended')

    def setEnabled(self, value_default):
        _t      = ('1', 't', 'true')
        _f      = ('0', 'f', 'false')
        _tsep   = "'" + "' or '".join(_t) + "'"
        _fsep   = "'" + "' or '".join(_f) + "'"
        _accept = (_t + _f)
        value_cfg       = str(self.cfgCurrent['Enabled'])
        prompt_msg      = "Please enter " +_tsep+ " to enable this plugin" +'\n'\
            + "or " +_fsep+ " to disable it" +'\n'\
            + "or leave the field empty to restore the default ("+str(value_default) +'):'
        selection_start = 0
        value_new       = ''
        value_new_fmt   = value_new.casefold()
        while value_new_fmt not in _accept:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['Enabled'] = value_default
                return
            value_new_fmt = value_new.casefold()
            if value_new_fmt not in _accept:
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + value_new_fmt +'\n'\
                    + "but the only acceptable values are:\n" +_tsep+ "\n" +_fsep)
        self.cfgCurrent['Enabled'] = True if value_new_fmt in _t else False

    def setSizeDivisor(self, value_default):
        _accept         = ('1000', '1024')
        value_cfg       = str(int(self.cfgCurrent['SizeDivisor']))
        prompt_msg      = "Please enter the file size divisor ('1000' or '1024') to display file size\nin a decimal (1k=1000=10³) or binary (1k=1024=2¹⁰) format" + '\n'\
            + "or leave the field empty to restore the default ("+str(value_default) +'):'
        selection_start = 2
        value_new       = ''
        while value_new not in _accept:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if   value_new.strip(' ') == '':
                self.cfgCurrent['SizeDivisor'] = value_default
                return
            elif value_new not in _accept:
                show_alert("You entered\n" + value_new +'\n'\
                    + "but the only acceptable values are:\n1000\n1024")
        self.cfgCurrent['SizeDivisor'] = float(value_new)

    def setMaxGlob(self, value_default):
        value_cfg       = str(self.cfgCurrent['MaxGlob'])
        prompt_msg      = "Please enter a natural number to set the threshold of the number of folders+files in a pane," +'\n'\
            + "above which the status bar for such a pane will not be updated to improve performance" +'\n'\
            + "or enter '0' to disable" +'\n'\
            + "or leave the field empty to restore the default ("+str(value_default)+"):"
        selection_start = 0
        value_new       = ''
        while not isNat0(value_new):
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['MaxGlob'] = value_default
                return
            if value_new.strip(' ') == '0':
                self.cfgCurrent['MaxGlob'] = 0
                return
            if   not isInt(value_new):
                show_alert("You entered\n" + value_new +'\n'\
                    + "but I couldn't parse it as an integer")
            elif not isNat0(value_new):
                show_alert("You entered\n" + value_new +'\n'\
                    + "but I was expecting a non-negative integer 0,1,2,3–∞")
        self.cfgCurrent['MaxGlob'] = int(value_new)

    def setSymbolPane(self, value_default):
        value_cfg       = " ".join(self.cfgCurrent['SymbolPane'])
        prompt_msg      = "Please enter two symbols, separated by space, to indicate Left/Right pane" +'\n'\
            + "or leave the field empty to restore the default ("+str(value_default)+"):"
        selection_start = 0
        selection_end   = 0
        value_new       = ''
        value_new_list  = []
        _len            = len(value_new_list)
        len_def         = len(value_default)
        while _len != len_def:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start, selection_end)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['SymbolPane'] = value_default
                return
            value_new_nosp = ' '.join(value_new.split()) # replace multiple spaces with 1
            value_new_list = value_new_nosp.split(' ')   # split by space
            _len = len(value_new_list)
            if _len != len_def:
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but was expecting " + str(len_def) + " elements")
        self.cfgCurrent['SymbolPane'] = value_new_list

    def setSymbolHiddenF(self, value_default):
        value_cfg       = " ".join(self.cfgCurrent['SymbolHiddenF'])
        prompt_msg      = "Please enter two symbols, separated by space, to indicate whether hidden files are Shown/Hidden" +'\n'\
            + "or leave the field empty to restore the default ("+str(value_default)+"):"
        selection_start = 0
        selection_end   = 0
        value_new       = ''
        value_new_list  = []
        _len            = len(value_new_list)
        len_def         = len(value_default)
        while _len != len_def:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start, selection_end)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['SymbolHiddenF'] = value_default
                return
            value_new_nosp = ' '.join(value_new.split()) # replace multiple spaces with 1
            value_new_list = value_new_nosp.split(' ')   # split by space
            _len = len(value_new_list)
            if _len != 2:
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but was expecting " + str(len_def) + " elements")
        self.cfgCurrent['SymbolHiddenF'] = value_new_list

    def setHideDotfile(self, value_default):
        _t      = ('1', 't', 'true')
        _f      = ('0', 'f', 'false')
        _tsep   = "'" + "' or '".join(_t) + "'"
        _fsep   = "'" + "' or '".join(_f) + "'"
        _accept = (_t + _f)
        value_cfg       = str(self.cfgCurrent['HideDotfile'])
        prompt_msg      = "Please enter " +_tsep+ " to treat all .dotfiles on Windows as hidden files\n    even if they don't have a 'hidden' attribute" +'\n'\
            + "or " +_fsep+ " to treat them as regular files" +'\n'\
            + "or leave the field empty to restore the default ("+str(value_default) +'):'
        selection_start = 0
        value_new       = ''
        value_new_fmt   = value_new.casefold()
        while value_new_fmt not in _accept:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['HideDotfile'] = value_default
                return
            value_new_fmt = value_new.casefold()
            if value_new_fmt not in _accept:
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + value_new_fmt +'\n'\
                    + "but the only acceptable values are:\n" +_tsep+ "\n" +_fsep)
        self.cfgCurrent['HideDotfile'] = True if value_new_fmt in _t else False

    def setJustify(self, value_default):
        value_cfg_in    = self.cfgCurrent['Justify']
        value_cfg       = " ".join(str(val) for val in  value_cfg_in.values())
        val_def_fmt     = " ".join(str(val) for val in value_default.values())
        max_val         = 11
        prompt_msg      = "Please enter three natural numbers, each <= "+str(max_val)+", separated by space, to set the minimum width of" +'\n'\
            + "the folder, file, and size indicators respectively." +'\n'\
            + "e.g. with a min width=2, 1 in 1 and 21 will align, but not in 321:" +'\n'\
            + " 1" +'\n'\
            + "21" +'\n'\
            + "321" +'\n'\
            + "or enter '0' to restore an individual default" +'\n'\
            + "or leave the field empty to restore all the defaults ("+val_def_fmt+"):"
        selection_start = 0
        selection_end   = 1
        value_new       = ''
        value_new_list  = []
        _len            = len(value_new_list)
        len_def         = len(value_default)
        above_max       = False
        while (not all([isNat0(v) for v in value_new_list])) \
            or above_max \
            or _len != len_def:
            value_new, ok = show_prompt(prompt_msg, value_cfg, selection_start, selection_end)
            value_cfg = value_new # preserve user input on multiple edits
            if not ok:
                show_status_message("StatusBarExtended: setup canceled")
                return
            if value_new.strip(' ') == '':
                self.cfgCurrent['Justify'] = value_default
                return
            value_new_nosp = ' '.join(value_new.split()) # replace multiple spaces with 1
            value_new_list = value_new_nosp.split(' ')   # split by space
            _len = len(value_new_list)
            if   not all([isInt(v) for v in value_new_list]):
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but I couldn't parse all elements as integers")
            elif not all([isNat0(v) for v in value_new_list]):
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but couldn't parse all elements as non-negative integers 0,1,2,3–∞")
            elif True in [int(v) > max_val for v in value_new_list]:
                above_max = True
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but the maximum value of each number is " + str(max_val))
                continue
            elif all([int(v) <= max_val for v in value_new_list]):
                above_max = False
            if _len != len_def:
                show_alert("You entered\n" + value_new +'\n'\
                    + "I parsed it as " + str(value_new_list) + " with " + str(_len) + " element" + ("" if _len==1 else "s") +'\n'\
                    + "but was expecting " + str(len_def) + " elements")
        for i, key in enumerate(value_default):
            if value_new_list[i] == '0':
                self.cfgCurrent['Justify'][key] = value_default[key]
            else:
                self.cfgCurrent['Justify'][key] = int(value_new_list[i])



class ViewConfigurationStatusBarExtended(ApplicationCommand):
    aliases = ('StatusBarExtended: view current configuration settings',)

    def __call__(self):
        cfg = SingletonConfig()
        cfgCurrent, exit_status = cfg.loadConfig()
        if cfgCurrent is None:
            return
        cfg_fmt = "StatusBarExtended's configuration:" +'\n\n'\
            + "Option" + '\t      ' + 'Current' + '\t' + 'Default' +'\n'
        for key in cfg.Default: # Default is odict, preserving the key order
            if   key in ('SizeDivisor'):
                cfg_fmt += key +'\t  =  '+ str(int(cfgCurrent[key])) + "\t"+str(int(cfg.Default[key])) +'\n'
            elif key in ('SymbolPane'):
                cfg_fmt += key +'\t  =  '+ " ".join(cfgCurrent[key]) + "\t"+" ".join(cfg.Default[key]) +'\n'
            elif key in ('SymbolHiddenF'):
                cfg_fmt += key +    '='  + " ".join(cfgCurrent[key]) + "\t"+" ".join(cfg.Default[key]) +'\n'
            elif key in ('Justify'):
                cfg_fmt += key +'\t  =  '+ " ".join(str(v) for v in cfgCurrent['Justify'].values()) + "\t"+" ".join(str(v) for v in cfg.Default['Justify'].values()) +'\n'
            else:
                cfg_fmt += key +'\t  =  '+ str(cfgCurrent[key]) + "\t"+str(cfg.Default[key]) +'\n'
        show_alert(cfg_fmt)

def isInt(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
def isNat0(s: str) -> bool:
    try:
        int(s)
        return int(s) >= 0
    except ValueError:
        return False
def isNat1(s: str) -> bool:
    try:
        int(s)
        return int(s) > 0
    except ValueError:
        return False
