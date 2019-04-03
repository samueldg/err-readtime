# ReadTime Bot

[![Build Status](https://travis-ci.org/samueldg/err-readtime.svg?branch=master)](https://travis-ci.org/samueldg/readtime)

**ReadTime** is a bot that listens for messages containing links, and will post an estimate the reading time. The estimate is based on [Medium's read time forumula](https://help.medium.com/hc/en-us/articles/214991667-Read-time), via the [readtime](https://pypi.org/project/readtime/) library.

The only commands of that bot are administrative, to control in which room(s) the bot is active.

## Commands

* `!readtime activate` — Activates the plugin in the current room.
* `!readtime deactivate` — Deactivates the plugin in the current room.

## Installation

The **ReadTime** bot depends on the [readtime](https://pypi.org/project/readtime/) library. You can either install it yourself, or set `AUTOINSTALL_DEPS` to `True` and let ErrBot do the rest. More info in the [User Guide](http://errbot.io/en/latest/user_guide/administration.html#dependencies).

## Contribute

Pull requests and issues are welcome!
