from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from rich.syntax import Syntax
import time

class MarkdownStream:
    def __init__(self, mdargs=None):
        self.mdargs = mdargs or {}
        self.live = Live(Text(""), refresh_per_second=4)
        self.live.start()
        self.content = ""
        self.last_update = 0

    def __del__(self):
        if self.live:
            self.live.stop()

    def update(self, text, final=False):
        now = time.time()
        if not final and now - self.last_update < 0.25:
            return
        self.last_update = now

        self.content += text
        markdown = Markdown(self.content, **self.mdargs)
        self.live.update(markdown)

        if final:
            self.live.stop()
            self.live = None

class Formatter:
    def __init__(self):
        self.console = Console()

    def create_style(self, color=None, bold=False):
        return f"{'bold ' if bold else ''}{color or ''}"

    def format_user_input(self, text, color):
        return Text(text, style=color)

    def format_tool_output(self, text, color):
        return Text(text, style=color)

    def format_code(self, code, language, theme):
        return Syntax(code, language, theme=theme)

    def rule(self, title=None, color=None):
        self.console.rule(title, style=color)

    def print(self, *objects, sep=" ", end="\n", style=None):
        self.console.print(*objects, sep=sep, end=end, style=style)
