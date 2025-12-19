from project_gen.utils.download import download
from project_gen.utils.generate import generate_api

download()
generate_api(
    package_name="game-service",
    swagger_url="http://185.185.143.231:5051/swagger/Game/swagger.json",
    )
