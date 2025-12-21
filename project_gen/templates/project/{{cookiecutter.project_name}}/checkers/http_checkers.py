import json
from typing import Generator
import httpx
from contextlib import contextmanager

@contextmanager  # type: ignore[arg-type]
def check_status_code_http(
    exception: type[Exception] = Exception,
    expected_status_code: int = httpx.codes.OK,
    expected_message: str = "",
) -> Generator[None, None, None]:
    try:
        yield
        if expected_status_code != httpx.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение {expected_message}, но запрос прошел успешно")
    except exception as e:
        assert e.status == expected_status_code
        # проверка на None для body, так как в ApiException body может быть Optional[str]
        if e.body is None:
            raise AssertionError("Body is None, cannot parse JSON") from e
        assert json.loads(e.body)["title"] == expected_message
