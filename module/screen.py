import subprocess

from libqtile import bar
from libqtile.lazy import lazy
from libqtile.config import Screen
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from .kanagawa import colors
from .keys import show_keys

powerline = {"decorations": [PowerLineDecoration(path="arrow_right")]}

# ibus engines (see `ibus list-engine`); Bamboo gives Vietnamese Telex
configured_keyboard = ["xkb:us::eng", "xkb:fr::fra", "Bamboo::Us"]
keyboard_labels = {"xkb:us::eng": "US", "xkb:fr::fra": "FR", "Bamboo::Us": "VI"}

browser = "firefox"


widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=12,
    background=colors["background-color"],
    foreground=colors["foreground-color"],
    padding=10,
)


class _IBusBackend:
    """KeyboardLayout backend that reads and switches ibus engines."""

    def get_keyboard(self):
        return subprocess.run(
            ["ibus", "engine"], capture_output=True, text=True
        ).stdout.strip()

    def set_keyboard(self, layout, options):
        subprocess.run(["ibus", "engine", layout])


class IBusKeyboardLayout(widget.KeyboardLayout):
    """KeyboardLayout driven by ibus instead of setxkbmap."""

    backend = property(lambda self: _IBusBackend(), lambda self, _: None)


keyboard_widget = IBusKeyboardLayout(
    configured_keyboards=configured_keyboard,
    display_map=keyboard_labels,
    background=colors["lighter-foreground"],
    **powerline,
)
extension_defaults = widget_defaults.copy()


class CenteredTextBox(widget.TextBox):
    """A TextBox without the 1px downward offset Qtile adds to bar text."""

    def _configure(self, qtile, parent_bar):
        super()._configure(qtile, parent_bar)
        draw = self.layout.draw
        self.layout.draw = lambda x, y: draw(x, y - 1)


def make_bar(primary=False):
    widgets = [
        widget.CurrentLayoutIcon(scale=0.65),
        widget.Sep(
            linewidth=0,
            padding=5,
            ),
        CenteredTextBox(
            padding=7,
            text="",
            foreground=colors["bold-color"],
            fontsize=17,
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
        CenteredTextBox(
            font="FiraCode Nerd Font",
            text="",
            foreground=colors["bold-color"],
            fontsize=17,
            mouse_callbacks={
                "Button1": lazy.screen.next_group()
                },
            ),
        widget.BrightnessControl(),
        widget.Spacer(**powerline),
    ]

    if primary:
        widgets += [
            CenteredTextBox(
                name="keys_button",
                text="",  # keyboard icon
                foreground=colors["bold-color"],
                fontsize=17,
                mouse_callbacks={"Button1": show_keys()},
            ),
            widget.Systray(icon_size=18),
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
    return bar.Bar(widgets, 24, margin=[0, 0, 5, 0], background=colors["background-color"])


screens = [
    Screen(top=make_bar(primary=True), wallpaper="~/.config/qtile/wallpaper.png", wallpaper_mode="fill"),
    Screen(top=make_bar(), wallpaper="~/.config/qtile/wallpaper.png", wallpaper_mode="fill"),
]
