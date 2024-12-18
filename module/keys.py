from libqtile.lazy import lazy
from libqtile.config import Click, Drag, Group, Key
from libqtile.widget import backlight

mod = "mod4"
terminal = "alacritty"
browser = "firefox"

def _change_brightness(increased):
    if increased:
        lazy.spawn("brightnessctl -d intel_backlight +10%")
    else:
        lazy.spawn("brightnessctl -d intel_backlight 10%-")

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        [mod],
        "space",
        lazy.window.toggle_maximize(),
        desc="Move window focus to other window",
    ),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Backspace", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "s", lazy.spawn("spotify"), desc="Launch spotify"),
    Key([mod], "d", lazy.spawn("discord"), desc="Launch discord"),
    Key([mod], "z", lazy.spawn("zotero"), desc="Launch zotero"),
    Key([mod], "a", lazy.spawn("zathura"), desc="Launch zathura"),
    Key([mod], "t", lazy.spawn("thunderbird"), desc="Launch thunderbird"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch apps using rofi"),
    Key(
        [mod], "f", lazy.spawn("rofi -show filebrowser"), desc="Browse file using rofi"
    ),
    Key(
        [mod, "control"],
        "x",
        lazy.spawn(
            "rofi -show p -modi p:rofi-power-menu -font 'Fira Code Nerd Font Mono 10' -lines 6"
        ),
        desc="Open the power menu",
    ),
    Key(
        [mod],
        "c",
        lazy.spawn(
            "rofi -theme-str 'window {width: 50%;}' -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}' -font 'Fira Code Nerd Font Mono 10' -lines 6"
        ),
        desc="Open the clipboard menu",
    ),
    Key([mod], "m", lazy.spawn("i3lock --nofork -t -i /home/muon/.config/qtile/kana_dark_2.png"), desc="Lock the screen"),
    Key([], "XF86AudioRaiseVolume", lazy.widget["pulsevolume"].increase_vol()),
    Key([], "XF86AudioLowerVolume", lazy.widget["pulsevolume"].decrease_vol()),
    Key([], "XF86AudioMute", lazy.widget["pulsevolume"].mute()),
    Key([], "XF86MonBrightnessUp", lazy.widget['brightnesscontrol'].brightness_up()),
    Key([], "XF86MonBrightnessDown", lazy.widget['brightnesscontrol'].brightness_down()),
]

groups = [Group(i, label="") for i in "123456"]


for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
