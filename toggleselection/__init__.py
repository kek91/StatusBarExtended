# Override commands that toggle item selection to automatically compute and instantly display
# combined filesize for selected files and the number of selected folders/files

from fman import DirectoryPaneCommand, DirectoryPaneListener, load_json, save_json, PLATFORM
import core.commands
from fman.url import splitscheme
import statusbarextended        as SBE
import statusbarextended_config as SBEcfg

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
        core.commands._toggle_hidden_files(self.pane, not core.commands._is_showing_hidden_files(self.pane))

def _get_opposite_pane(pane):
    panes = pane.window.get_panes()
    return panes[(panes.index(pane) + 1) % len(panes)]



class CommandEmpty(DirectoryPaneCommand): # to avoid duplicate command execution (and "return '', args" hangs)
    def __call__(self):
        pass

class SelectionOverride(DirectoryPaneListener):
    def on_command(self, command_name, args):
        if   command_name in ('switch_panes'):
            pane_cur = self.pane
            pane_opp = _get_opposite_pane(self.pane)
            pane_opp.focus()    # doesn't change self.pane, so...
            self.pane=pane_opp  # ...need to do it manually...
            self.show_selected_files()
            self.pane=pane_cur  # ...and restore after the statusbar update
            return 'command_empty', {}
        elif command_name in (
            'select_all', 'deselect',
            'toggle_hidden_files'):
            getattr(_CorePaneCommand, command_name)(self)
            self.show_selected_files()
            return 'command_empty', {}
        elif command_name in ( # commands that can pass a 'toggle_selection' argument
            'move_cursor_down'     , 'move_cursor_up'     ,
            'move_cursor_page_down', 'move_cursor_page_up',
            'move_cursor_home'     , 'move_cursor_end'):
            getattr(_CorePaneCommand, command_name)(self, args)
            if 'toggle_selection' in args:
                if args['toggle_selection'] == True:
                    self.show_selected_files()
            return 'command_empty', {}

    def show_selected_files(self):
        cfg = SBEcfg.SingletonConfig()
        cfgCurrent, exit_status = cfg.loadConfig()
        if  cfgCurrent is None:
            return
        if  cfgCurrent["Enabled"] == True:
            SBE.StatusBarExtended.show_selected_files(self, cfgCurrent)
