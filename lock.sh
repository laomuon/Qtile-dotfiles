#!/bin/sh
# Lock the screen with i3lock-color, styled by the options in lock.conf.
# i3lock-color is built from source and linked at ~/.local/bin/i3lock-color; without it, fall back to plain i3lock.
# This must always end by running a locker.

image="$HOME/.config/qtile/kana_dark_2.png"
config="$HOME/.config/qtile/lock.conf"
locker="$HOME/.local/bin/i3lock-color"

if [ ! -x "$locker" ] || [ ! -r "$config" ]; then
    exec i3lock --nofork -i "$image"
fi

# xargs splits lock.conf into arguments and honours its quotes.
grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$config" |
    exec xargs "$locker" --nofork -i "$image"
