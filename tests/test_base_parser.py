import pytest

from project_atlantis.parsers import BaseParser


def test_base_parser_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseParser()