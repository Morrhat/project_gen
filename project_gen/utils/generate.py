import os
import pathlib
import shutil

from project_gen.utils.utils import run_command


def generate_api(package_name: str, swagger_url: str, templates: str | None=None) -> None:
    templates = templates or str(pathlib.Path(__file__).parent.parent / "templates" / "python")
    command = [
        "java", "-jar", "openapi-generator-cli-7.17.0.jar",
        "generate", "-i", swagger_url,
         "-g", "python",
         "-o", package_name,
         "-t", templates,
         "--library", "asyncio",
         "--package-name", package_name,
         "--skip-validate-spec",
         ]
    if templates:
        command.extend(["-t", templates])

    run_command(command)


def move_files(package_name: str) -> None:
    if os.path.exists(f"clients/http/{package_name}"):
        shutil.rmtree(f"clients/http/{package_name}")

    shutil.move(f"{package_name}/{package_name}", f"clients/http/{package_name}")
    shutil.rmtree(package_name)

# "http://5.63.153.31:8085/register/openapi.json"
# http://185.185.143.231:5051/swagger/Game/swagger.json
