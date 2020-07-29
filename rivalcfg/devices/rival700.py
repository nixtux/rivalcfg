from .. import usbhid

_RIVAL700_RGBGRADIENT_HEADER = {
    "color_field_length": 139,  # Index of length of colot field (used for padding)                                    # noqa
    "duration_length": 2,       # Length of the "duration" field (in Bytes)                                            # noqa
    "maxgradient":14,           # max numbers of gradients see handler rival700_rgbgradient.py                         # noqa
}

_DEFAULT_RIVAL700_RGBGRADIENT = "[8l0rgbgradient(duration=1000; colors=0%: #ff00e1, 33%: #ffea00, 66%: #00ccff)"  # noqa

_TRIGGER_HEADER = {
    "header_length": 6,        # Length of the header excuding command / LED ID
    "led_id_offsets": 3,       # Offset of the "led_id" fields
    "duration_offset": 8,      # Offset of the "duration" field
    "duration_length": 2,      # Length of the "duration" field (in Bytes)
}

_DEFAULT_TRIGGER = "trigger(duration=1000; #ff0000, #00ff00)"  # noqa

profile = {

    "name": "SteelSeries Rival 700",

    "models": [{
        "name": "SteelSeries Rival 700",
        "vendor_id": 0x1038,
        "product_id": 0x1700,
        "endpoint": 0,
    }, {
        "name": "SteelSeries Rival 710",
        "vendor_id": 0x1038,
        "product_id": 0x1730,
        "endpoint": 0,
    }],

    "settings": {

        "sensitivity1": {
            "label": "Sensibility preset 1",
            "description": "Set sensitivity preset 1 (DPI)",
            "cli": ["-s", "--sensitivity1"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x00, 0x01],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 800,
        },

        "sensitivity2": {
            "label": "Sensibility preset 2",
            "description": "Set sensitivity preset 2 (DPI)",
            "cli": ["-S", "--sensitivity2"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x03, 0x00, 0x02],
            "command_suffix": [0x00, 0x42],
            "value_type": "range",
            "input_range": [100, 12000, 100],
            "output_range": [0x00, 0x77, 1],
            "default": 1600,
        },

        "polling_rate": {
            "label": "Polling rate",
            "description": "Set polling rate (Hz)",
            "cli": ["-p", "--polling-rate"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x04, 0x00],
            "value_type": "choice",
            "choices": {
                125: 0x04,
                250: 0x03,
                500: 0x02,
                1000: 0x01,
            },
            "default": 1000,
        },

        "wheel_color": {
            "label": "Wheel LED colors and effects",
            "description": "Set the colors and the effects of the wheel LED",
            "cli": ["-C", "--wheel-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x00],
            "command_suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x00, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "logo_color": {
            "label": "Logo LED colors and effects",
            "description": "Set the colors and the effects of the logo LED",
            "cli": ["-c", "--logo-color"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00, 0x01],
            "command_suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x01, 0x01],
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_logo_trigger": {
            "description": "Set the wheel backlight color",
            "cli": ["-t", "--logo-trigger"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00],
            "command_suffix": [0x00, 0x08, 0x00, 0x00],
            "value_type": "trigger",
            "led_id": 0x0,
            "default": [["#FF3C00", "#FF32C8"], 200]
        },

        "set_wheel_trigger": {
            "description": "Set the wheel backlight color",
            "cli": ["-T", "--wheel-trigger"],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "command": [0x05, 0x00],
            "command_suffix": [0x00, 0x08, 0x00, 0x00],
            "value_type": "trigger",
            "led_id": 0x1,
            "default": [["#FF1800", "#FF1800"], 200]
        },

        "set_logo_rgbgradient": {
            "description": "Set the logo colors and effects",
            "cli": ["-O", "--logo-colorshift"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rival700_rgbgradient",
            "rival700_rgbgradient_header": _RIVAL700_RGBGRADIENT_HEADER,
            "led_id": 0x0,
            "default": _DEFAULT_RIVAL700_RGBGRADIENT,
        },

        "set_wheel_rgbgradient": {
            "description": "Set the wheel colors and effects",
            "cli": ["-o", "--wheel-colorshift"],
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,
            "value_type": "rival700_rgbgradient",
            "rival700_rgbgradient_header": _RIVAL700_RGBGRADIENT_HEADER,
            "led_id": 0x1,
            "default": _DEFAULT_RIVAL700_RGBGRADIENT,
        },

        "set_tactile_settings": {
            "description": "Set tactile feedback on click",
            "cli": ["--ts", "--tactile-settings"],
            "command": [0x92, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "value_type": "tactile_button_map",
        },

        "buttons_mapping": {
            "label": "Buttons mapping",
            "description": "Set the mapping of the buttons",
            "cli": ["-b", "--buttons"],
            "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
            "command": [0x31, 0x00],
            "value_type": "buttons",
            "rival700": True,

            "buttons": {
                "Button1": {"id": 0x01, "offset": 0x00, "default": "button1"},
                "Button2": {"id": 0x02, "offset": 0x05, "default": "button2"},
                "Button3": {"id": 0x03, "offset": 0x0a, "default": "button3"},
                "Button4": {"id": 0x04, "offset": 0x0f, "default": "button4"},
                "Button5": {"id": 0x05, "offset": 0x14, "default": "button5"},
                "Button6": {"id": 0x06, "offset": 0x19, "default": "disable"},
                "Button7": {"id": 0x07, "offset": 0x1e, "default": "dpi"},

            },

            "button_field_length": 5,

            "button_disable":     0x00,
            "button_keyboard":    0x51,
            "button_multimedia":  0x61,
            "button_dpi_switch":  0x30, #0x15
            "button_scroll_up":   0x31, #0xcd
            "button_scroll_down": 0x32, #0xcd

            "default": "buttons(button1=button1; button2=button2; button3=button3; button4=button4; button5=button5; button6=disable; button7=dpi; layout=qwerty)",  # noqa
        },

    },

    "save_command": {
        "report_type": usbhid.HID_REPORT_TYPE_OUTPUT,
        "command": [0x09, 0x00],
    },

}
