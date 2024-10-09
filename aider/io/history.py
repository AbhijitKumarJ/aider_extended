from prompt_toolkit.history import FileHistory
from pathlib import Path

class HistoryManager:
    def __init__(self, input_history_file=None, chat_history_file=None, llm_history_file=None):
        self.input_history_file = input_history_file
        self.chat_history_file = Path(chat_history_file) if chat_history_file else None
        self.input_history = FileHistory(input_history_file) if input_history_file else None
        self.llm_history_file = Path(llm_history_file) if llm_history_file else None

    def add_to_input_history(self, input_text):
        if self.input_history:
            self.input_history.append_string(input_text)

    def get_input_history(self):
        if self.input_history:
            return self.input_history.load_history_strings()
        return []

    def append_chat_history(self, text, linebreak=False, blockquote=False, strip=True):
        if self.chat_history_file:
            with self.chat_history_file.open("a", encoding="utf-8") as f:
                if blockquote:
                    text = "> " + text
                if strip:
                    text = text.strip()
                if linebreak:
                    text = text + "  \n"
                if not text.endswith("\n"):
                    text += "\n"
                f.write(text)

    def log_llm_history(self, role, content):
        if self.llm_history_file:
            timestamp = datetime.now().isoformat(timespec="seconds")
            with self.llm_history_file.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{role.upper()} {timestamp}\n")
                log_file.write(content + "\n")
