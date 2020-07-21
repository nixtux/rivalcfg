"""
The "command_data" type handles data for lua api command only


Device Profile
--------------

Example of a frame value type in a device profile:

::

    profile = {

        # ...

        "settings": {

            "screen": {
                "label": "OLED frame",
                "description": "Oled frame",
                "command": [0x50],
                "stream_len": 576
                "value_type": "command_data",
            },

        },

        # ...

    }


CLI
---

frame is a none cli command

LUA API
-------

Todo

Functions
---------
"""


def process_value(setting_info, data):
    """Called by the :class:`rivalcfg.mouse.Mouse` class when processing a
    "frame" type setting.

    :param dict setting_info: The information dict of the setting from the
                              device profile.
    """
    # frame
    if len(data) != setting_info["command_data"]:
        raise ValueError("Please provide %i bytes data." %
                         (setting_info["command_data"]))
    return data


def add_cli_option(cli_parser, setting_name, setting_info):
    # pass here as none cli command
    pass
