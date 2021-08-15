# Override the Core hidden file filter to be able to hide non-hidden dotfiles on Windows

from fman import load_json, PLATFORM, DATA_DIRECTORY
import core.commands
from fman.url import as_human_readable as as_path, as_url, join, splitscheme, basename
from fman.fs import exists

config_file       = 'StatusBarExtended ('+PLATFORM+').json'
user_settings_url = join(as_url(DATA_DIRECTORY),'Plugins','User','Settings')
f_url             = join(user_settings_url, config_file)
f_path            = as_path(f_url)
key               = 'HideDotfile'
if exists(f_url):
    cfgCurrent = load_json(f_path) # read the path directly and without any validation as at this moment in module loading load_json doesn't seem to know about 'User/Settings' path and cfg.loadConfig() would instead of loading the existing config create a new file at the wrong location ('Third-party/StatusBarExtended' folder)

    # Replace Core file filter with Core + dotfiles (if 'HideDotfile' is set)
    if PLATFORM == 'Windows' \
        and type(cfgCurrent) is type(dict()) \
        and key in cfgCurrent \
        and cfgCurrent[key] == True:
        _core_hidden_file_filter = core.commands._hidden_file_filter
        def _hidden_file_filter(url):
            core_return = _core_hidden_file_filter(url)
            if core_return and not is_dotfile(url): # regular and not dotfile
                return True
            else:                                   # hidden or is_dotfile
                return False
        core.commands._hidden_file_filter = _hidden_file_filter

def is_dotfile(url):
    return basename(url).startswith('.')
