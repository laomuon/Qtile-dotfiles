from libqtile import hook, qtile
from libqtile.config import Output, ScreenRect
from libqtile.utils import send_notification
import os
import subprocess


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])


@hook.subscribe.client_focus
def float_to_front(window):
    if window.floating:
        window.bring_to_front()


@hook.subscribe.screens_reconfigured
def forget_unplugged_screens():
    # Qtile 0.37 matches screens by monitor, and an unplugged screen object still
    # names the monitor that took its place. Qtile then treats it as live: focus
    # stays on it and workspaces sent there vanish. So compare objects, not ==.
    live = {id(s) for s in qtile.screens}
    dead = [s for s in qtile.config.screens if id(s) not in live]
    for screen in dead:
        screen.output = Output(None, None, None, None, ScreenRect(0, 0, 0, 0))
    for group in qtile.groups:
        if group.screen is not None and id(group.screen) not in live:
            group.hide()
    if id(qtile.current_screen) not in live:
        qtile.focus_screen(0)
    for screen in dead:
        # Otherwise replugging hides whichever workspace this screen last showed.
        if hasattr(screen, "group"):
            del screen.group


@hook.subscribe.screens_reconfigured
def on_screen_change():
    subprocess.Popen(["autorandr", "--change"])


@hook.subscribe.startup_complete
def on_startup_complete():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/change_screen.sh")])
#
#
# @hook.subscribe.suspend
# def lock_on_sleep():
# qtile.spawn("light-locker-command -l")
