from . import helpers


def _transform(command, *args):
    """Apply command's transformation function (if any) to given arguments.

    Arguments:
    command -- the command description dict
    *args -- command arguments
    """
    if "value_transform" in command:
        return command["value_transform"](*args)
    return args if len(args) > 1 else args[0]


def choice_handler(command, choice):
    """Returns command bytes from choices commands.

    Arguments:
    command -- the command description dict
    choice -- the choosen value
    """
    if choice not in command["choices"]:
        raise ValueError(
                "value must be one of [%s]" %
                helpers.choices_to_string(command["choices"]))
    value = command["choices"][choice]
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], value)


def rgbcolor_handler(command, *args):
    """Returns command bytes from RGB color commands.

    Arguments:
    command -- the command description dict
    *args -- the color as a string (color name or hexadecimal RGB), or as R, G
             and B int (e.g. fn(cmd, "red"), fn(cmd, "#ff0000"),
             fn(cmd, 255, 0, 0))
    """
    color = (0x00, 0x00, 0x00)
    if len(args) == 3:
        for value in args:
            if type(value) != int or value < 0 or value > 255:
                raise ValueError("Not a valid color %s" % str(args))
        color = args
    elif len(args) == 1 and type(args[0]) == str and helpers.is_color(args[0]):
        color = helpers.color_string_to_rgb(args[0])
    else:
        raise ValueError("Not a valid color %s" % str(args))
    color = _transform(command, *color)
    return helpers.merge_bytes(command["command"], color)


def rgbcolorshift_handler(command, colors, speed=200):
    """Returns command bytes from RGB color commands.

    Arguments:
    command -- the command description dict
    colors -- the colors as an array of string (color name or hexadecimal RGB),
              or as an array of array of R, G and B int (e.g. fn(cmd, ["red"]),
              fn(cmd, ["#ff0000"]), fn(cmd, [[255, 0, 0]]))

    Keyword arguments:
    speed -- the color shift speed (default 200ms)
    """
    parsed_colors = []
    for color in colors:
        if type(color) in (list, tuple) and len(color) == 3:
            parsed_colors.extend(color)
        elif type(color) == str and helpers.is_color(color):
            parsed_colors.extend(helpers.color_string_to_rgb(color))
        else:
            raise ValueError("Not a valid color %s" % str(color))
    parsed_colors, speed = _transform(command, parsed_colors, speed)
    speed = helpers.uint_to_little_endian_bytearray(speed, 2)
    return helpers.merge_bytes(command["command"], parsed_colors, speed)


def rgbuniversal_handler(command, colors, positions, speed, triggers):
    """ Returns command bytes from RGB color commands.
    It crafts packets on a per mouse basis, by reading the format given
    in "rgbuniversal_format" in the command dict. If a single color is given,
    it creates a steady color command. If multiple colors are given, it creates
    a colorshift command. If triggermask is nonzero, a reactive command is
    created.

    Arguments:
    command -- the command description dict
    colors -- the colors as an array of string (color name or hexadecimal RGB)
    positions -- cumulative color positions as an array of hex strings
    speed -- the colorshift cycle time as a string (milliseconds)
    triggers -- trigger button mask as a hex string
    """
    colors = list(map(helpers.color_string_to_rgb, colors))
    positions = list(map(lambda x: int(x, 16), positions))
    speed = 5000 if speed.lower() == "x" else int(speed, 10)
    triggers = 0 if triggers.lower() == "x" else int(triggers, 16)

    rgb_format = command["rgbuniversal_format"]
    header = [0] * rgb_format["header_len"]

    for led_id in rgb_format["led_id"]:
        header[led_id] = command["led_id"]

    speed_pos, speed_len = rgb_format["speed"], rgb_format["speed_len"]
    speed = helpers.uint_to_little_endian_bytearray(speed, speed_len)

    header[speed_pos:speed_pos + speed_len] = speed
    header[rgb_format["repeat"]] = 1 if len(colors) == 1 or triggers > 0 else 0
    header[rgb_format["triggers"]] = triggers
    header[rgb_format["point_count"]] = len(colors) + 1

    # data segment format:
    # color1:color1:pos1:...:colorn:posn:color1:pos1
    data = colors[0]

    for color, pos in zip(colors, positions):
        data = helpers.merge_bytes(data, color, pos)

    remaining = 0xff - sum(positions)
    if remaining < 0:
        raise ValueError("The cumulative position offsets must be < 255 (is %d)" % sum(positions)) # noqa

    # inserts first color at the end for smooth colorshifting
    data = helpers.merge_bytes(data, colors[0], remaining)

    return helpers.merge_bytes(command["command"], header, data)


def rival700_colorshift_handler(command, colors, positions, speed):
    """ Returns command bytes from RGB color commands.
    It crafts packets on a per mouse basis, by reading the format given
    in "rival700_colorshift_format" in the command dict. If a single color is
    given,it creates a steady color command. If multiple colors are given,
    it creates a colorshift command.

    Arguments:
    command -- the command description dict
    colors -- the colors as an array of string (color name or hexadecimal RGB)
    positions -- what percentage of color position
    speed -- the colorshift cycle time as a string (milliseconds)
    """
    colors = list(map(helpers.color_string_to_rgb, colors))
    # print(colors, len(colors))
    positions = list(positions)
    speed = 5000 if speed.lower() == "x" else int(speed, 10)

    rgb_format = command["rival700_colorshift_format"]
    start_header = [0x1d, 0x01, 0x02, 0x31, 0x51, 0xff, 0xc8, 0x00]
    #              [0xff, 0x3c, 0x00, 0xff, 0x32, 0xc8, 0xc8, 0x00]
    header = helpers.merge_bytes(command["led_id"], start_header)

    # 7 bytes in a stage
    stage = []
    r = colors[0][0]
    g = colors[0][1]
    b = colors[0][2]
    last_pos = 0
    oldcolor = [0,0,0]

    for i in range(1, len(colors)):
        stage.append(i-1)
        stage.append(00)

        pos = int(positions[i]) - last_pos
        time = int(speed / 100 * int(pos))
        last_pos = pos

        index = 0
        for rgb in colors[i]:
            diff = rgb - oldcolor[index]
            ramp = round(diff / time * 8)
            oldcolor[index] = rgb
            stage = helpers.merge_bytes(stage, ramp & 255)
            index = index + 1
            # print("rgb", rgb, diff, ramp, ramp & 255, hex(ramp & 255))
        stage.append(00)
       
        # print("pos percentage ", positions[i], " at ", time, "of", speed)
        time = helpers.uint_to_little_endian_bytearray(time, 2)
        stage = helpers.merge_bytes(stage, time)

    # for i in range(len(stage)):
        # print(hex(stage[i]))

    header = helpers.merge_bytes(header, stage)
    padding = [0] * (rgb_format["header_len"] - len(header))
    header = helpers.merge_bytes(header, padding)

    speed_len = rgb_format["speed_len"]
    speed = helpers.uint_to_little_endian_bytearray(speed, speed_len)

    data = colors[0]

    for color, pos in zip(colors, positions):
        data = helpers.merge_bytes(data, color, pos)

    start_color = colors[0]
    split_color = []
    for i in range(len(start_color)):
        high, low = helpers.bytes_to_high_low_nibbles(start_color[i])
        left_byte = helpers.nibbles_to_byte(low, 00)
        right_byte = high & 0x0F
        split_color.append(left_byte)
        split_color.append(right_byte)

    end_suffix = [0xff, 0x00, 0xdc, 0x05, 0x8a, 0x02, 0x00, 0x00, 0x00, 0x00,
                  0x01, 0x00, 0x03, 0x00]
    suffix = helpers.merge_bytes(split_color, end_suffix, speed)

    return helpers.merge_bytes(command["command"], header, suffix)


def range_handler(command, value):
    """Returns command bytes from range commands.

    Arguments:
    command -- the command description dict
    value -- the choosen value
    """
    if not command["range_min"] <= value <= command["range_max"]:
        raise ValueError("Value %i not in range [%i, %i]" % (
            value,
            command["range_min"],
            command["range_max"]
            ))
    if ("range_increment" in command
            and value % command["range_increment"] != 0):
        raise ValueError("Value %i is not a multiple of %i" % (
            value,
            command["range_increment"]
            ))
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], value)


def none_handler(command):
    """Returns command bytes for command with not arguments.

    Arguments:
    command -- the command description dict
    """
    return command["command"]


def hotsbtnmap_handler(command, value):
    """Returns command bytes for HotS button map.

    Arguments:
    command -- the command description dict
    value -- the choosen value
    """
    olist = helpers.hotsbtnmap_to_list(value)
    if len(olist) != 8:
        raise ValueError("Please provide 8 keys to be mapped.")
    value = _transform(command, value)
    return helpers.merge_bytes(command["command"], *olist)
