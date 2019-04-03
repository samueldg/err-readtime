import re
import urllib.request

import readtime
from errbot import BotPlugin
from errbot import botcmd
from errbot import re_botcmd


# Using Django's URL regex (adapted for simplification)
# https://github.com/django/django/blob/master/django/core/validators.py

ul = '\u00a1-\uffff'  # unicode letters range (must not be a raw string)

# Host patterns
hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
tld_re = (
    r'\.'                                # dot
    r'(?!-)'                             # can't start with a dash
    r'(?:[a-z' + ul + '-]{2,63}'         # domain label
    r'|xn--[a-z0-9]{1,59})'              # or punycode label
    r'(?<!-)'                            # can't end with a dash
    r'\.?'                               # may have a trailing dot
)
host_re = '(' + hostname_re + domain_re + tld_re + ')'

URL_REGEX = re.compile(
    r'https?://'  # Only allow HTTP/HTTPS
    r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
    r'(?:' + host_re + ')'
    r'(?::\d{2,5})?'  # port
    r'(?:[/?#][^\s]*)?',  # resource path
    re.IGNORECASE | re.UNICODE,
)


def get_page_html(url):
    """Given a web page URL, return it's HTML content as a string.
    """
    with urllib.request.urlopen(url) as response:
        content = response.read()
        content_encoding = response.headers.get_content_charset()
    html = content.decode(content_encoding)  # Is this legit?
    return html


class ReadTimePlugin(BotPlugin):

    @staticmethod
    def get_room_id(room):
        """Return the room object as a string.
        """
        return str(room)

    def is_active_in_room(self, room):
        """Checks whether or not the bot has been activated in the room.

        This is achieved by looking at the plugin storage.
        """
        room_id = self.get_room_id(room)
        try:
            return self['room:' + room_id]
        except KeyError:
            return False
        return room_id == '#TODO'

    @botcmd
    def readtime_activate(self, msg, args):
        """Activate the plugin in the current room.
        """
        room_id = self.get_room_id(msg.to)
        self['room:' + room_id] = True

        return 'ReadTime activated!'

    @botcmd
    def readtime_deactivate(self, msg, args):
        """Dectivate the plugin in the current room.
        """
        room_id = self.get_room_id(msg.to)
        self['room:' + room_id] = False

        return 'ReadTime deactivated!'

    @re_botcmd(pattern=URL_REGEX, prefixed=False)
    def estimate_link_read_time(self, msg, args):
        """Listen to messages containing a link, and if so, fetch the page
        and estimate the reading time based on the HTML.

        If the bot is not active in the room, it simply does nothing.
        """
        room = msg.to
        if not self.is_active_in_room(room):
            return

        url = re.search(URL_REGEX, msg.body).group(0)
        html = get_page_html(url)
        estimated_time = readtime.of_html(html)
        return 'Estimated time: {} min.'.format(estimated_time.minutes)
