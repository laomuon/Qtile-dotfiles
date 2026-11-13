#!/bin/bash
# Lock the screen with i3lock-color, styled by the options in lock.conf.
# i3lock-color is built from source and linked at ~/.local/bin/i3lock-color; without it, fall back to plain i3lock.
# This must always end by running a locker.
# dunst draws above the locker, so notifications are paused while locked. They queue up and show after unlocking.

image="$HOME/.config/qtile/kana_dark_2.png"
config="$HOME/.config/qtile/lock.conf"
locker="$HOME/.local/bin/i3lock-color"

# Leave do-not-disturb on after unlocking if it was already on
was_paused=$(dunstctl is-paused)
dunstctl set-paused true

if [ -x "$locker" ] && [ -r "$config" ]; then
    # xargs splits lock.conf into arguments and honours its quotes.
    mapfile -d '' options < <(grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$config" | xargs printf '%s\0')
    "$locker" --nofork -i "$image" "${options[@]}" &
else
    i3lock --nofork -i "$image" &
fi
pid=$!

# The locker releases xss-lock's sleep delay once the screen is locked. Drop this shell's copy so it can.
[ -n "$XSS_SLEEP_LOCK_FD" ] && exec {XSS_SLEEP_LOCK_FD}<&-

# xss-lock stops the locker with TERM when the session is unlocked through logind
trap 'kill "$pid"' TERM INT
wait "$pid"

[ "$was_paused" = true ] || dunstctl set-paused false
