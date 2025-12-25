import os
import platform
import requests


OPENAPI_GENERATOR = "openapi-generator-cli-7.17.0.jar"

def download() -> None:
    url = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.17.0/openapi-generator-cli-7.17.0.jar"

    if platform.system() == "Windows":
        scripts_dir = ".venv/Scripts"
    else:
        scripts_dir = ".venv/bin"  # На Mac/Linux

    os.makedirs(scripts_dir, exist_ok=True)

    with requests.get(url, stream=True, timeout=100, verify=False) as response:
        response.raise_for_status()
        file_name = OPENAPI_GENERATOR

        file_path = os.path.join(scripts_dir, file_name)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        if platform.system() != "Windows":
            os.chmod(file_path, mode=0o755)


def init() -> None:
    if platform.system() == "Windows":
        scripts_dir = ".venv/Scripts"
    else:
        scripts_dir = ".venv/bin"   # На Mac/Linux

    file_path = os.path.join(scripts_dir, OPENAPI_GENERATOR)

    if not os.path.exists(file_path):
        download()

    print(f"Downloaded {OPENAPI_GENERATOR}")
    
