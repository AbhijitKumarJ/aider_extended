import os
from pathlib import Path
import base64
import mimetypes

class FileIO:
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def read_text(self, filename):
        try:
            with open(filename, "r", encoding=self.encoding) as f:
                return f.read()
        except Exception as e:
            return f"Error reading {filename}: {str(e)}"

    def write_text(self, filename, content):
        try:
            with open(filename, "w", encoding=self.encoding) as f:
                f.write(content)
        except Exception as e:
            return f"Error writing to {filename}: {str(e)}"

    def read_image(self, filename):
        try:
            with open(str(filename), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                mime_type, _ = mimetypes.guess_type(filename)
                if mime_type and mime_type.startswith("image/"):
                    return f"data:{mime_type};base64,{encoded_string}"
                else:
                    return None
        except Exception as e:
            return f"Error reading image {filename}: {str(e)}"

    def is_file_safe(self, fname):
        try:
            return Path(fname).is_file()
        except OSError:
            return False
