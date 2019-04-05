import re
from contextlib import contextmanager
from queue import Empty

import pytest

import readtime_bot


# pytest/errbot config
extra_plugin_dir = '.'
pytest_plugins = [
    'errbot.backends.test',
]


EXAMPLE_URL = 'https://example.com'
MESSAGE_WITH_URL = 'Check out this link: {0} OMG!'.format(EXAMPLE_URL)
MESSAGE_WITHOUT_URL = 'I love https: such a great protocol!'

ACTIVATE_COMMAND = '!readtime activate'
DEACTIVATE_COMMAND = '!readtime deactivate'

TIMEOUT = 0.5  # How long to wait for the response, in seconds.


@contextmanager
def assert_no_message():
    with pytest.raises(Empty) as exc_info:
        yield exc_info


@pytest.mark.regression(issue=3)
def test_get_url():
    url = 'https://towardsdatascience.com/from-scikit-learn-to-tensorflow-part-1-9ee0b96d4c85'
    html = readtime_bot.get_page_html(url)
    assert html is not None

@pytest.mark.parametrize('command', [
    ACTIVATE_COMMAND,
    DEACTIVATE_COMMAND,
])
def test_admin_commands_exist(testbot, command):
    testbot.assertCommandFound(command, timeout=TIMEOUT)


def test_url_in_room_default(testbot):
    testbot.push_message(MESSAGE_WITH_URL)
    with assert_no_message():
        testbot.pop_message(timeout=TIMEOUT)


def test_url_in_activated_room(testbot):
    testbot.push_message(ACTIVATE_COMMAND)
    testbot.pop_message()  # Activation response
    testbot.push_message(MESSAGE_WITH_URL)
    response = testbot.pop_message()
    assert re.match(r'Estimated time: \d+ min.', response)


def test_no_url_in_activated_room(testbot):
    testbot.push_message(ACTIVATE_COMMAND)
    testbot.pop_message()  # Activation response
    testbot.push_message(MESSAGE_WITHOUT_URL)
    with assert_no_message():
        testbot.pop_message()


def test_url_in_deactivated_room(testbot):
    # Activate then deactivate
    testbot.push_message(ACTIVATE_COMMAND)
    testbot.pop_message()  # Activation response
    testbot.push_message(DEACTIVATE_COMMAND)
    testbot.pop_message()  # Deactivation response

    # Send message with URL
    testbot.push_message(MESSAGE_WITHOUT_URL)
    with assert_no_message():
        testbot.pop_message()


# TODO: Use testbot.inject_mocks to mock urllib
