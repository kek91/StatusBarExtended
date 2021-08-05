# Override commands that toggle item selection to automatically compute and instantly display
# combined filesize for selected files and the number of selected folders/files

from fman import DirectoryPaneListener, load_json
import json
from statusbarextended import StatusBarExtended

class CommandEmpty(): # to avoid duplicate command execution (and "return '', args" hangs)
    def __call__(self):
        pass

class SelectionOverride(DirectoryPaneListener):
    def on_command(self, command_name, args):
        if command_name in ('select_all'): # def ^A
            self.pane.select_all()
            self.show_selected_files()
            return 'command_empty', args
        elif command_name in ('deselect'): # def ^D
            self.pane.clear_selection()
            self.show_selected_files()
            return 'command_empty', args
        elif command_name in ( # commands that can pass a 'toggle_selection' argument
            'move_cursor_down'     , 'move_cursor_up'     ,
            'move_cursor_page_down', 'move_cursor_page_up',
            'move_cursor_home'     , 'move_cursor_end'):
            if args.get('toggle_selection'): # select item → update statusbar → pass False arg
                file_under_cursor = self.pane.get_file_under_cursor()
                if file_under_cursor:
                    self.pane.toggle_selection(file_under_cursor)
                    self.show_selected_files()
                    new_args = dict(args)
                    new_args['toggle_selection'] = False
                    return command_name, new_args

    def show_selected_files(self):
        statusBarExtendedEnabled = load_json('StatusBarExtended.json')
        if statusBarExtendedEnabled:
            statusBarExtendedEnabledJson = json.loads(statusBarExtendedEnabled)
            if statusBarExtendedEnabledJson['enabled'] == True:
                StatusBarExtended.show_selected_files(self)
