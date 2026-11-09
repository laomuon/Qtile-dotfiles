#!/bin/sh
#
# xfsettingsd &
#
# xfce4-power-manager &

# Start notifications. xfce4-notifyd can claim the D-Bus name first, so stop it.
systemctl --user stop xfce4-notifyd.service
dunst &

# Start ibux for unikey
ibus-daemon -dxrR &

# Start i3lock for lockscreen
xss-lock --transfer-sleep-lock -- i3lock --nofork -i /home/dmmuon/.config/qtile/kana_dark_2.png &

# Disable screen blanking
xset dpms 0 0 0 &
xset s off -dpms &


# Start greenclip
pkill greenclip; greenclip clear && greenclip daemon &

# Start bentopdf
docker start bentopdf >/dev/null 2>&1 &

## Starting compositor on startup
picom --daemon --config ~/.config/picom/picom.conf

## Start the password-prompt service
/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &

## Start the network manager and bluetooth applet
nm-applet &
blueman-applet &
