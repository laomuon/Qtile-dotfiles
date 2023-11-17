from libqtile import hook
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


@hook.subscribe.screen_change
def on_screen_change(event):
    home = os.path.expanduser("~/.config/qtile/change_screen.sh")
    subprocess.run([home])
