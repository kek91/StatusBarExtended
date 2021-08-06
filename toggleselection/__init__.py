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

class CommandEmpty(): # to avoid duplicate command execution (and "return '', args" hangs)
    def __call__(self):
        pass

class SelectionOverride(DirectoryPaneListener):
    def on_command(self, command_name, args):
            self.show_selected_files()
            return 'command_empty', args
        elif command_name in (
            'select_all', 'deselect'):
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
