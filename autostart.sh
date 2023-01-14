#!/bin/sh
## Define screen ouputs and their positon
xrandr --output DP-2 --primary --left-of eDP-1 --auto
# Start the docker
docker start eureka-dev-env_base_1

## Starting compositor on startup for transparency
picom --config ~/.config/picom/picom.conf --experimental-backends -b &

# Start power manager
xfce4-power-manager &

# Start xscreensaver
xscreensaver -nosplash &

# Run spotifyd
~/spotifyd/target/release/spotifyd &
