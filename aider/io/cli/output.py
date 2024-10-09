# aider/ionew/cli/output.py

from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from ..base import BaseOutputHandler
from ..formatting import MarkdownStream

class CLIOutputHandler(BaseOutputHandler):
    def __init__(self, pretty=True, user_input_color="blue", tool_output_color=None,
                 tool_error_color="red", tool_warning_color="#FFA500",
                 assistant_output_color="blue", code_theme="default"):
        self.pretty = pretty
        self.user_input_color = user_input_color if pretty else None
        self.tool_output_color = tool_output_color if pretty else None
        self.tool_error_color = tool_error_color if pretty else None
        self.tool_warning_color = tool_warning_color if pretty else None
        self.assistant_output_color = assistant_output_color
        self.code_theme = code_theme
        self.console = Console(force_terminal=pretty, no_color=not pretty)

    def tool_output(self, message="", log_only=False, bold=False):
        if not log_only:
            style = None
            if bold:
                style = "bold"
                if self.tool_output_color:
                    style += f" {self.tool_output_color}"
            elif self.tool_output_color:
                style = self.tool_output_color

            self.console.print(message, style=style)

    def tool_error(self, message="", strip=True):
        if strip:
            message = message.strip()
        self.console.print(f"Error: {message}", style=f"bold {self.tool_error_color}")

    def tool_warning(self, message="", strip=True):
        if strip:
            message = message.strip()
        self.console.print(f"Warning: {message}", style=self.tool_warning_color)

    def assistant_output(self, message, pretty=None):
        if pretty is None:
            pretty = self.pretty

        if pretty:
            md = Markdown(message, style=self.assistant_output_color)
            self.console.print(md)
        else:
            self.console.print(message)

    def user_input(self, message, log_only=False):
        if not log_only:
            self.console.print(message, style=self.user_input_color)

    def show_rate_limit_warning(self):
        self.tool_warning("Rate limit reached. Waiting before retrying...")

    def get_assistant_mdstream(self):
        mdargs = dict(style=self.assistant_output_color, code_theme=self.code_theme)
        return MarkdownStream(mdargs=mdargs)
