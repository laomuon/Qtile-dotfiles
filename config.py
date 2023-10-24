# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.core.manager import Qtile
from libqtile.utils import send_notification
from libqtile.log_utils import logger
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from colors.nord import colors
from colors.winter_rainbow import colors as decor_colors
# from colors.catpuccin import colors

mod = "mod4"
terminal = "alacritty"
browser = "firefox"
configured_keyboard = ["us", "fr"]


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


@hook.subscribe.startup
def dbus_register():
    id = os.environ.get('DESKTOP_AUTOSTART_ID')
    if not id:
        return
    subprocess.Popen(['dbus-send',
                      '--session',
                      '--print-reply',
                      '--dest=org.gnome.SessionManager',
                      '/org/gnome/SessionManager',
                      'org.gnome.SessionManager.RegisterClient',
                      'string:qtile',
                      'string:' + id])


@hook.subscribe.client_focus
def float_to_front(window):
    if window.floating:
        window.bring_to_front()

@lazy.function
def z_next_keyboard(qtile):
    keyboard_widget.next_keyboard()


powerline = {
    "decorations": [
        PowerLineDecoration(path="arrow_right")
    ]
}


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.window.toggle_maximize(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
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
    Key([mod], "z", lazy.spawn("zulip"), desc="Launch zulip"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch apps using rofi"),
    Key([mod], "f", lazy.spawn("rofi -show filebrowser"), desc="Browse file using rofi"),
    Key([mod, "shift"], "space", z_next_keyboard, desc="Change keyboard layout"),
    Key([mod, 'control'], 'x',
        lazy.spawn("rofi -show p -modi p:rofi-power-menu -font 'Fira Code Nerd Font Mono 10' -lines 6"),
        desc="Open the power menu"),
    Key([mod], 'm', lazy.spawn('gnome-screensaver-command -l'), desc="Lock the screen"),
    Key([], "XF86AudioRaiseVolume", lazy.widget["pulsevolume"].increase_vol()),
    Key([], "XF86AudioLowerVolume", lazy.widget["pulsevolume"].decrease_vol()),
    Key([], "XF86AudioMute", lazy.widget["pulsevolume"].mute()),
]

groups = [Group(i, label="") for i in "123456"]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
        # "border_width": 2,
        "border_focus": colors["blue"],
        "border_normal": colors["darkbg"],
        "margin": [5, 9, 5, 9]
        }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    layout.Stack(num_stacks=2, **layout_theme),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]
widget_defaults = dict(
    font="Font Awesome",
    fontsize=12,
    background=colors["bg"][0],
    foreground=colors["fg"][0],
    padding=10,
)
keyboard_widget = widget.KeyboardLayout(configured_keyboards=configured_keyboard, background=decor_colors[2], **powerline)
extension_defaults = widget_defaults.copy()
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(fontsize=7),
                widget.Sep(
                        linewidth=0,
                        padding=5,
                    ),
                widget.TextBox(
                        text="",
                        foreground=colors["super blue"],
                        fontsize=20,
                    ),
                widget.GroupBox(
                    fontsize=15,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=3,
                    borderwidth=3,
                    active=colors["super cyan"],
                    rounded=True,
                    highlight_method="text",
                    this_current_screen_border=colors["green"],
                    ),
                widget.TextBox(
                        font="Font Awesome",
                        text="",
                        foreground=colors["super blue"],
                        fontsize=20,
                    ),
                widget.Sep(
                        linewidth=0,
                        padding=5,
                    ),
                widget.Prompt(),
                widget.Spacer(**powerline),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.PulseVolume(background=decor_colors[1], **powerline),
                keyboard_widget,
                # widget.Bluetooth(),
                widget.GithubNotifications(
                    icon_size=15,
                    token_file="~/tokens/github.token",
                    mouse_callbacks={
                        "Button1": lazy.spawn([browser, "-new-tab", "https://github.com/notifications"])
                    },
                    update_interval=10,
                    background=decor_colors[3],
                    **powerline,
                ),
                # widget.WiFiIcon(
                #         interface="wlp9s0",
                #         padding=6,
                #         mouse_callbacks={"Button1": lazy.spawn("alacritty -e 'nmtui'")},
                #         background=decor_colors[7],
                #         **powerline,
                # ),
                widget.Clock(format="%H:%M  %d/%m/%y", background=decor_colors[8], **powerline),
                widget.UPowerWidget(background=decor_colors[9], **powerline),
                widget.QuickExit(
                    default_text="",
                    countdown_format='[{}]',
                    background=decor_colors[10],
                ),
            ],
            25,
            margin=[5, 9, 0, 9],
            background=colors["lightbg"],
            opacity=1
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper='~/.config/qtile/wallpaper.png',
        wallpaper_mode='fill',
    ),
    Screen(
        wallpaper='~/.config/qtile/kana_dark.jpg',
        wallpaper_mode='fill'
    ),
]
logger.warning(lazy.widget)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
layouts.append(floating_layout)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
