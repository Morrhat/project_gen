from project_gen.utils.download import download
from project_gen.utils.generate import generate_api, move_files, replace_import_in_files

download()
generate_api(
    package_name="game_service",
    swagger_url="http://185.185.143.231:5051/swagger/Game/swagger.json",
    )

move_files(package_name="game_service")
replace_import_in_files(
    directory="clients/http",
    package_name="game_service",
)