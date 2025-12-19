import os
import platform
import shutil
import requests


OPENAPI_GENERATOR = "openapi-generator-cli-7.17.0.jar"

def download() -> None:
    url = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.17.0/openapi-generator-cli-7.17.0.jar"
    with requests.get(url, stream=True, timeout=100, verify=False) as response:
        response.raise_for_status()
        file_name = OPENAPI_GENERATOR
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        if platform.system() != "Windows":
            os.chmod(file_name, mode=0o755)

    shutil.move(file_name, f".venv/Scripts/{file_name}")



def init() -> None:
    if not os.path.exists(f".venv/Scripts/{OPENAPI_GENERATOR}"):
        download()

    print(f"Downloaded {OPENAPI_GENERATOR}")


