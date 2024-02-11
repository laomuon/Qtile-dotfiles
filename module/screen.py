from libqtile import bar
from libqtile.lazy import lazy
from libqtile.config import Screen
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from .kanagawa import colors

powerline = {"decorations": [PowerLineDecoration(path="arrow_right")]}

configured_keyboard = ["us", "fr"]

browser = 'firefox'


@lazy.function
def z_next_keyboard(qtile):
    keyboard_widget.next_keyboard()


widget_defaults = dict(
    font="Font Awesome",
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
                    foreground=colors["bold-color"],
                    fontsize=20,
                ),
                widget.GroupBox(
                    fontsize=15,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=3,
                    borderwidth=3,
                    active=colors["highlight-foreground-color"],
                    rounded=True,
                    highlight_method="text",
                    this_current_screen_border=colors["highlight-background-color"],
                ),
                widget.TextBox(
                    font="Font Awesome",
                    text="",
                    foreground=colors["bold-color"],
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
                    update_interval=10,
                    background=colors["black"],
                    **powerline,
                ),
                widget.Clock(
                    format="%H:%M  %d/%m/%y",
                    background=colors["lighter-foreground"],
                    timezone="Asia/Ho_Chi_Minh",
                    **powerline,
                ),
                widget.UPowerWidget(
                    background=colors["darker-foreground"], **powerline
                ),
            ],
            25,
            margin=[0, 0, 5, 0],
            background=colors["background-color"],
            opacity=1,
        ),
        wallpaper="~/.config/qtile/wallpaper.png",
        wallpaper_mode="fill",
    ),
    Screen(wallpaper="~/.config/qtile/kana_dark.jpg", wallpaper_mode="fill"),
]
