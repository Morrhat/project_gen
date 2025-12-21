import platform
from pathlib import Path

class ClientCollector:
    base_path: Path = Path(".") / "clients" / "http"

    def collect_clients(self):
        clients = []
        for file_path in self.base_path.rglob("*.py"):
            if str(file_path.parent).endswith("api") and file_path.name.endswith("__init__.py"):
                with file_path.open("r", encoding="utf-8") as f:
                    lines = f.readlines()

                for line in lines:
                    if line.startswith("from"):
                        system = platform.system()

                        if system == "Windows":
                            parts = str(file_path.parent.parent).split("\\")
                        else:  # Linux, MacOS, etc.
                            parts = str(file_path.parent.parent).split("/")

                        client = {
                            "client": line.split()[-1],
                            "package": parts[-1]
                        }
                        clients.append(client)
        return clients
