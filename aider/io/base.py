from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ConfirmGroup:
    preference: str = None
    show_group: bool = True

    def __init__(self, items=None):
        if items is not None:
            self.show_group = len(items) > 1

class BaseInputHandler(ABC):
    @abstractmethod
    def get_input(self, prompt, **kwargs):
        pass

    @abstractmethod
    def confirm_ask(self, question, default="y", subject=None, explicit_yes_required=False, group=None, allow_never=False):
        pass

    @abstractmethod
    def prompt_ask(self, question, default="", subject=None):
        pass

class BaseOutputHandler(ABC):
    @abstractmethod
    def tool_output(self, message, **kwargs):
        pass

    @abstractmethod
    def tool_error(self, message, **kwargs):
        pass

    @abstractmethod
    def tool_warning(self, message, **kwargs):
        pass

    @abstractmethod
    def assistant_output(self, message, **kwargs):
        pass

    @abstractmethod
    def user_input(self, message, **kwargs):
        pass

    @abstractmethod
    def show_rate_limit_warning(self):
        pass

    @abstractmethod
    def get_assistant_mdstream(self):
        pass

class BaseIO(ABC):
    def __init__(self, input_handler: BaseInputHandler, output_handler: BaseOutputHandler):
        self.input_handler = input_handler
        self.output_handler = output_handler
        self._encoding = "utf-8"  # Default encoding

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

    def get_input(self, *args, **kwargs):
        return self.input_handler.get_input(*args, **kwargs)

    def confirm_ask(self, *args, **kwargs):
        return self.input_handler.confirm_ask(*args, **kwargs)

    def prompt_ask(self, *args, **kwargs):
        return self.input_handler.prompt_ask(*args, **kwargs)

    def tool_output(self, *args, **kwargs):
        return self.output_handler.tool_output(*args, **kwargs)

    def tool_error(self, *args, **kwargs):
        return self.output_handler.tool_error(*args, **kwargs)

    def tool_warning(self, *args, **kwargs):
        return self.output_handler.tool_warning(*args, **kwargs)

    def assistant_output(self, *args, **kwargs):
        return self.output_handler.assistant_output(*args, **kwargs)

    def user_input(self, *args, **kwargs):
        return self.output_handler.user_input(*args, **kwargs)

    def show_rate_limit_warning(self):
        return self.output_handler.show_rate_limit_warning()

    @abstractmethod
    def read_text(self, filename):
        pass

    @abstractmethod
    def write_text(self, filename, content):
        pass

    @abstractmethod
    def read_image(self, filename):
        pass

    @abstractmethod
    def is_file_safe(self, fname):
        pass

    @abstractmethod
    def add_to_input_history(self, input_text):
        pass

    @abstractmethod
    def get_input_history(self):
        pass

    @abstractmethod
    def append_chat_history(self, text, linebreak=False, blockquote=False):
        pass

    @abstractmethod
    def get_assistant_mdstream(self):
        pass

    @abstractmethod
    def log_llm_history(self, role, content):
        pass
