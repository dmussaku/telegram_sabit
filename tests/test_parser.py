from utils.parser import TelegramParser
import pytest


@pytest.mark.parametrize('input_data,expected', (
    ({'text': '  sample_text  '}, 'sample_text'),
    ({'text': ['Sample_Text', 'wrong_text']}, 'sample_text'),
    ({'text': 911}, ''),
    ({'text': ('wrong_text', 911)}, ''),
    ({'text': {'wrong_text': 911}}, ''),
))
def test_get_message_text_parametrized(input_data, expected):
    result = TelegramParser.get_message_text(input_data)
    assert result == expected


def test_get_message_text_error():
    with pytest.raises(Exception):
        TelegramParser.get_message_text({'text': [{'wrong_text': 911}]})
