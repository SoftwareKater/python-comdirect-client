import pathlib
import json


class FileHandler():
    def __init__(self):
        pass


    def ensure_dir(self, path: str):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)


    def save_json(self, filename: str, content) -> None:
        serialized = json.dumps(content)
        with open(filename, "w") as f:
            f.write(serialized)


    def load_json(self, filename: str):
        with open(filename, "r") as f:
            content = f.read()
        res = json.loads(content)
        return res


    def _create_if_not_exist(self, filename: str, default_content):
        try:
            with open(filename, "r") as f:
                pass
        except FileNotFoundError:
            self.save_json(filename, default_content)
