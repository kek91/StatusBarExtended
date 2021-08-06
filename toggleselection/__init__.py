# Override commands that toggle item selection to automatically compute and instantly display
# combined filesize for selected files and the number of selected folders/files

from fman import DirectoryPaneCommand, DirectoryPaneListener, load_json, save_json, PLATFORM
from core.commands.util import is_hidden
from fman.url import splitscheme
import json
from statusbarextended import StatusBarExtended

class _CorePaneCommand(DirectoryPaneCommand): # copy from core/commands/__init__.py
    def select_all(self):
        self.pane.select_all()
    def deselect(  self):
        self.pane.clear_selection()

    def move_cursor_down(     self,     toggle_selection=False):
        self.pane.move_cursor_down(     toggle_selection)
    def move_cursor_up(       self,     toggle_selection=False):
        self.pane.move_cursor_up(       toggle_selection)
    def move_cursor_page_up(  self,     toggle_selection=False):
        self.pane.move_cursor_page_up(  toggle_selection)
    def move_cursor_page_down(self,     toggle_selection=False):
        self.pane.move_cursor_page_down(toggle_selection)
    def move_cursor_home(     self,     toggle_selection=False):
        self.pane.move_cursor_home(     toggle_selection)
    def move_cursor_end(      self,     toggle_selection=False):
        self.pane.move_cursor_end(      toggle_selection)

    def toggle_hidden_files(self):
        _toggle_hidden_files(self.pane, not _is_showing_hidden_files(self.pane))
def _toggle_hidden_files(pane, value):
    if value:
        pane._remove_filter(_hidden_file_filter)
    else:
        pane._add_filter(_hidden_file_filter)
    _get_pane_info(pane)['show_hidden_files'] = value
    save_json('Panes.json')
def _is_showing_hidden_files(pane):
    return _get_pane_info(pane)['show_hidden_files']
def _get_pane_info(pane):
    settings = load_json('Panes.json', default=[])
    default = {'show_hidden_files': False}
    pane_index = pane.window.get_panes().index(pane)
    for _ in range(pane_index - len(settings) + 1):
        settings.append(default.copy())
    return settings[pane_index]
def _hidden_file_filter(url):
    if PLATFORM == 'Mac' and url == 'file:///Volumes':
        return True
    scheme, path = splitscheme(url)
    return scheme != 'file://' or not is_hidden(path)

def _get_opposite_pane(pane):
    panes = pane.window.get_panes()
    return panes[(panes.index(pane) + 1) % len(panes)]



class CommandEmpty(): # to avoid duplicate command execution (and "return '', args" hangs)
    def __call__(self):
        pass

class SelectionOverride(DirectoryPaneListener):
    def on_command(self, command_name, args):
            self.show_selected_files()
            return 'command_empty', args
        elif command_name in (
            'select_all', 'deselect',
            'toggle_hidden_files'):
            getattr(_CorePaneCommand, command_name)(self)
            self.show_selected_files()
            return 'command_empty', args
        elif command_name in ( # commands that can pass a 'toggle_selection' argument
            'move_cursor_down'     , 'move_cursor_up'     ,
            'move_cursor_page_down', 'move_cursor_page_up',
            'move_cursor_home'     , 'move_cursor_end'):
            getattr(_CorePaneCommand, command_name)(self, args)
            self.show_selected_files()
            return 'command_empty', args

    def show_selected_files(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.show_selected_files(self)
