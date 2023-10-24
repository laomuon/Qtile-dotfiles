#!/bin/sh
## Define screen ouputs and their positon
if ! (xrandr | grep "^HDMI-1" | grep "disconnected")
then
    xrandr --output HDMI-1 --primary --left-of eDP-1 --auto
else
    xrandr --output DP-2 --primary --left-of eDP-1 --auto
fi
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
gnome-screensaver &
