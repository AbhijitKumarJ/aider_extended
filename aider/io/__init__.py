from .base import BaseIO, ConfirmGroup
from .cli.input import CLIInputHandler
from .cli.output import CLIOutputHandler
from .file_io import FileIO
from .history import HistoryManager
from .formatting import Formatter, MarkdownStream

class CLIIO(BaseIO):
    def __init__(self, pretty=True, yes=None, input_history_file=None, chat_history_file=None,
                 encoding="utf-8", user_input_color="blue", tool_output_color=None,
                 tool_error_color="red", tool_warning_color="#FFA500",
                 assistant_output_color="blue", code_theme="default", llm_history_file=None, *args, **kwargs):
        self.encoding = encoding
        self.input_handler = CLIInputHandler(encoding=encoding)
        self.output_handler = CLIOutputHandler(
            pretty=pretty,
            user_input_color=user_input_color,
            tool_output_color=tool_output_color,
            tool_error_color=tool_error_color,
            tool_warning_color=tool_warning_color,
            assistant_output_color=assistant_output_color,
            code_theme=code_theme
        )
        super().__init__(self.input_handler, self.output_handler)

        self.file_io = FileIO(encoding=encoding)
        self.history_manager = HistoryManager(input_history_file, chat_history_file, llm_history_file)
        self.formatter = Formatter()
        self.yes = yes
        self.pretty = pretty
        self.commands = []  # Initialize an empty list for commands

    def get_input(self, prompt, root="", files=None, addable_files=None, commands=None, abs_read_only_fnames=None, edit_format=None):
        if commands is None:
            commands = self.commands
        return self.input_handler.get_input(prompt, root, files, addable_files, commands, abs_read_only_fnames, edit_format)

    def set_commands(self, commands):
        self.commands = commands

    def read_text(self, *args, **kwargs):
        return self.file_io.read_text(*args, **kwargs)

    def write_text(self, *args, **kwargs):
        return self.file_io.write_text(*args, **kwargs)

    def read_image(self, *args, **kwargs):
        return self.file_io.read_image(*args, **kwargs)

    def is_file_safe(self, *args, **kwargs):
        return self.file_io.is_file_safe(*args, **kwargs)

    def add_to_input_history(self, *args, **kwargs):
        return self.history_manager.add_to_input_history(*args, **kwargs)

    def get_input_history(self, *args, **kwargs):
        return self.history_manager.get_input_history(*args, **kwargs)

    def append_chat_history(self, *args, **kwargs):
        return self.history_manager.append_chat_history(*args, **kwargs)

    def get_assistant_mdstream(self):
        return self.output_handler.get_assistant_mdstream()

    def rule(self, *args, **kwargs):
        return self.formatter.rule(*args, **kwargs)

    def print(self, *args, **kwargs):
        return self.formatter.print(*args, **kwargs)

    def get_rel_fname(self, fname):
        from pathlib import Path
        try:
            return str(Path(fname).relative_to(self.file_io.root))
        except ValueError:
            return fname

    def log_llm_history(self, role, content):
            self.history_manager.log_llm_history(role, content)

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

    def create_file(self, filepath):
        try:
            Path(filepath).touch()
            return True
        except Exception as e:
            self.tool_error(f"Error creating file {filepath}: {str(e)}")
            return False

    def add_file(self, filepath):
        if not Path(filepath).exists():
            create = self.confirm_ask(f"File {filepath} does not exist. Create it?")
            if create:
                if self.create_file(filepath):
                    self.tool_output(f"Created file: {filepath}")
                    return True
            return False
        return True

__all__ = ['CLIIO', 'BaseIO', 'FileIO', 'HistoryManager', 'Formatter', 'ConfirmGroup']
