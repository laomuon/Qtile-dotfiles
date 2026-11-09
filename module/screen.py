from libqtile import bar
from libqtile.lazy import lazy
from libqtile.config import Screen
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from .kanagawa import colors

powerline = {"decorations": [PowerLineDecoration(path="arrow_right")]}

configured_keyboard = ["us", "fr"]

browser = "firefox"


@lazy.function
def z_next_keyboard(qtile):
    keyboard_widget.next_keyboard()

widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=12,
    background=colors["background-color"],
    foreground=colors["foreground-color"],
    padding=10,
)
keyboard_widget = widget.KeyboardLayout(
    configured_keyboards=configured_keyboard,
    background=colors["lighter-foreground"],
    **powerline,
)
extension_defaults = widget_defaults.copy()

def make_bar(primary=False):
    widgets = [
        widget.CurrentLayoutIcon(fontsize=7),
        widget.Sep(
            linewidth=0,
            padding=5,
            ),
        widget.TextBox(
            text="",
            foreground=colors["bold-color"],
            fontsize=20,
            mouse_callbacks={
                "Button1": lazy.screen.prev_group()
                },
            ),
        widget.GroupBox(
            fontsize=15,
            margin_y=4,
            padding=0,
            active=colors["highlight-foreground-color"],
            rounded=True,
            highlight_method="text",
            this_current_screen_border=colors["blue"],
            ),
        widget.TextBox(
            font="FiraCode Nerd Font",
            text="",
            foreground=colors["bold-color"],
            fontsize=20,
            mouse_callbacks={
                "Button1": lazy.screen.next_group()
                },
            ),
        widget.BrightnessControl(),
        widget.Spacer(**powerline),
    ]

    if primary:
        widgets += [
            widget.Systray(),
            widget.Spacer(**powerline),
            widget.PulseVolume(background=colors["darker-foreground"], **powerline),
            keyboard_widget,
            widget.GithubNotifications(
                icon_size=15,
                token_file="~/tokens/github.token",
                mouse_callbacks={
                    "Button1": lazy.spawn(
                        [browser, "-new-tab", "https://github.com/notifications"]
                    )
                },
                update_interval=60,
                background=colors["black"],
                **powerline,
            ),
            widget.Clock(
                format="%H:%M  %d/%m/%y",
                background=colors["lighter-foreground"],
                # timezone="Europe/Paris",
                # # timezone="Asia/Ho_Chi_Minh",
                # # timezone="Asia/Singapore",
                **powerline,
            ),
            widget.UPowerWidget(
                background=colors["darker-foreground"], **powerline
            ),
        ]
    return bar.Bar(widgets, 25, margin=[0, 0, 5, 0], background=colors["background-color"])


screens = [
    Screen(top=make_bar(primary=True), wallpaper="~/.config/qtile/wallpaper.png", wallpaper_mode="fill"),
    Screen(top=make_bar(), wallpaper="~/.config/qtile/wallpaper.png", wallpaper_mode="fill"),
]
