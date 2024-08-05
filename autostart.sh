#!/bin/sh

## Starting compositor on startup for transparency
picom --daemon --config ~/.config/picom/picom.conf -b &

# Start ibux for unikey
ibus-daemon &
# Start power manager
# xfce4-power-manager &

# Start xscreensaver
# xscreensaver -nosplash &

# Start gnome-screensaver
# light-locker &
xss-lock --transfer-sleep-lock -- i3lock --nofork -i /home/muon/.config/qtile/kana_dark_2.png &

# Start greenclip
pkill greenclip && greenclip clear && greenclip daemon &
