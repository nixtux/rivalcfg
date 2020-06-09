
from .. import usbhid

rival700 = {
    "name": "SteelSeries Rival 700 (Experimental)",

    "vendor_id": 0x1038,
    "product_id": 0x1700,
    "interface_number": 0,

    "rival700_colorshift_format": {
        "header_len": 139,  # Number of bytes in header excluding command bytes
        "led_id": [0],      # Index(es) of LED ID (unsure why rival600 have 2)
        "speed": 160,       # Index of the colorshift speed field
        "speed_len": 2,     # How many bytes the speed field takes up
        "data_pos": 12,    # Index of the color count field
    },

    "commands": {

        "set_sensitivity1": {
            "description": "Set sensitivity preset 1",
            "cli": ["-s", "--sensitivity1"],
            "command": [0x03, 0x00, 0x01],
            "suffix": [0x00, 0x42],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int((x / 100) - 1),
            "default": 800,
        },

        "set_sensitivity2": {
            "description": "Set sensitivity preset 2",
            "cli": ["-S", "--sensitivity2"],
            "command": [0x03, 0x00, 0x02],
            "suffix": [0x00, 0x42],
            "value_type": "range",
            "range_min": 100,
            "range_max": 12000,
            "range_increment": 100,
            "value_transform": lambda x: int((x / 100) - 1),
            "default": 1600,
        },

        "set_polling_rate": {
            "description": "Set polling rate in Hz",
            "cli": ["-p", "--polling-rate"],
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

        "set_logo_color": {
            "description": "Set the logo backlight color",
            "cli": ["-c", "--logo-color"],
            "command": [0x05, 0x00, 0x00],
            "suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x00, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_wheel_color": {
            "description": "Set the wheel backlight color",
            "cli": ["-C", "--wheel-color"],
            "command": [0x05, 0x00, 0x01],
            "suffix": [0xFF, 0x32, 0xC8, 0xC8, 0x00, 0x01, 0x01],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rgbcolor",
            "default": "#FF1800"
        },

        "set_wheel_colorshift": {
            "description": "test",
            "cli": ["-o", "--wheel-o"] ,
            "command": [0x05, 0x00],
            "report_type": usbhid.HID_REPORT_TYPE_FEATURE,  # wValue = 0x0300
            "value_type": "rival700_colorshift",
            "led_id": 0x0,
        },

        "save": {
            "description": "Save the configuration to the mouse memory",
            "cli": None,
            "command": [0x09, 0x00],
            "value_type": None,
        },

    },

}
