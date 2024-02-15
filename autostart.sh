#!/bin/sh
# Start the docker
docker start eureka-dev-env_base_1
docker start eureka-model-server

## Starting compositor on startup for transparency
picom --daemon --config ~/.config/picom/picom.conf -b &

# Start ibux for unikey
ibus-daemon &
# Start power manager
# xfce4-power-manager &

# Start xscreensaver
# xscreensaver -nosplash &

# Start gnome-screensaver
light-locker &

# Start greenclip
pkill greenclip && greenclip clear && greenclip daemon &
