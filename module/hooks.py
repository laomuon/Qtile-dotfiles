from libqtile import hook, qtile
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
