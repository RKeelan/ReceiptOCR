import importlib.util


def test_paddleocr_dependency_is_available():
    assert importlib.util.find_spec("paddleocr") is not None
