from libqtile import hook, qtile
from libqtile.utils import send_notification
import os
import subprocess


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])


@hook.subscribe.client_focus
def float_to_front(window):
    if window.floating:
        window.bring_to_front()


@hook.subscribe.screens_reconfigured
def on_screen_change():
    home = os.path.expanduser("~/.config/qtile/change_screen.sh")
    subprocess.run([home])


#
#
# @hook.subscribe.suspend
# def lock_on_sleep():
# qtile.spawn("light-locker-command -l")
