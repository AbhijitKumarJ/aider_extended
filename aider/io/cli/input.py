# aider/ionew/cli/input.py

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document
from ..base import BaseInputHandler
import os

class AutoCompleter(Completer):
    def __init__(self, root, rel_fnames, addable_rel_fnames, commands, encoding, abs_read_only_fnames=None):
        self.root = root if isinstance(root, str) else root[0] if root else ''
        self.rel_fnames = rel_fnames
        self.addable_rel_fnames = addable_rel_fnames
        self.commands = commands if commands else []
        self.encoding = encoding
        self.abs_read_only_fnames = abs_read_only_fnames or []

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith('/'):
            return self.get_command_completions(text[1:])
        return self.get_file_completions(text)

    def get_command_completions(self, text):
        for command in self.commands:
            if command.startswith(text):
                yield Completion(command, start_position=-len(text))

    def get_file_completions(self, text):
        path_completer = PathCompleter(get_paths=lambda: [self.root])
        for completion in path_completer.get_completions(Document(text), None):
            yield completion

class CLIInputHandler(BaseInputHandler):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding
        self.prompt_session = PromptSession()

    def get_input(self, prompt, root="", files=None, addable_files=None, commands=None, abs_read_only_fnames=None, edit_format=None):
        completer = AutoCompleter(root, files or [], addable_files or [], commands or [], self.encoding, abs_read_only_fnames)

        # Format the prompt to just show ">"
        formatted_prompt = "> "

        return self.prompt_session.prompt(formatted_prompt, completer=completer)

    def confirm_ask(self, question, default="y", subject=None, explicit_yes_required=False, group=None, allow_never=False):
        if subject:
            print(subject)

        if group and not group.show_group:
            group = None

        options = " (Y)es/(N)o"
        if group:
            options += "/(A)ll/(S)kip all"
        if allow_never:
            options += "/(D)on't ask again"

        while True:
            response = self.prompt_ask(f"{question}{options} [{default}]: ", default=default).lower()
            if response in ['y', 'yes'] or (not explicit_yes_required and response == ''):
                return True
            elif response in ['n', 'no']:
                return False
            elif group and response == 'a':
                group.preference = 'all'
                return True
            elif group and response == 's':
                group.preference = 'skip'
                return False
            elif allow_never and response == 'd':
                return None
            else:
                print("Please provide a valid response.")

    def prompt_ask(self, question, default="", subject=None):
        if subject:
            print(subject)
        return self.prompt_session.prompt(question, default=default)
