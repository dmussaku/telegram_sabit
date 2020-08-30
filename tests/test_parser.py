import pytest
from utils.parser import TelegramParser


@pytest.fixture
def chat_message():
    """
    Simple chat message fixture
    """
    return {
        "action": "migrate_from_group",
        "actor": "John Doe",
        "actor_id": 845274635,
        "date": "2020-04-28T22:22:56",
        "edited": "1970-01-01T01:00:00",
        "id": 1,
        "text": "FooBar",
        "title": "Тест 5",
        "type": "service"
    }


def test_get_message_text_happypath(chat_message):
    print(chat_message)


@pytest.mark.parametrize('input,expected_result', (
    ({'text': '  FoOBar  '}, 'foobar'),
    ({'text': ['FooBar']}, 'foobar'),
    ({'text': {'foo': 'bar'}}, ''),
))
def test_get_message_text_parametrized(input, expected_result):
    result = TelegramParser.get_message_text(input)
    assert result == expected_result
