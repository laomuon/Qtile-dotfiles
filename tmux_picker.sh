#!/bin/sh
# Pick a tmux session with rofi and open it in a new terminal.
# Typing a name that doesn't exist creates that session.
session=$(tmux list-sessions -F '#S' 2>/dev/null | rofi -dmenu -i -p tmux) || exit 0
[ -n "$session" ] || exit 0
exec alacritty -e tmux new-session -A -s "$session"
