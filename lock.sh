#!/bin/sh
# Lock the screen with the image fitted to each monitor.
# i3lock draws one image from the top left of the whole desktop, so build that image for the current layout.
# If building it fails, lock with the original image. This must always end by running i3lock.

image="$HOME/.config/qtile/kana_dark_2.png"
cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/qtile"

outputs=$(xrandr --query)
desktop=$(printf '%s\n' "$outputs" | sed -n 's/.*current \([0-9]*\) x \([0-9]*\),.*/\1x\2/p')
monitors=$(printf '%s\n' "$outputs" | sed -n 's/.* connected.* \([0-9]*x[0-9]*+[0-9]*+[0-9]*\) .*/\1/p')

key=$(printf '%s\n' "$desktop" $monitors | md5sum | cut -c1-12)
fitted="$cache_dir/lock-$key.png"

if [ ! "$fitted" -nt "$image" ]; then
    mkdir -p "$cache_dir"
    set --
    for monitor in $monitors; do
        size=${monitor%%+*}
        offset=+${monitor#*+}
        set -- "$@" "(" "$image" -resize "$size^" -gravity center -extent "$size" ")" \
            -gravity northwest -geometry "$offset" -composite
    done
    convert -size "$desktop" xc:black "$@" "png:$fitted.tmp" && mv "$fitted.tmp" "$fitted"
    rm -f "$fitted.tmp"
fi

[ -s "$fitted" ] || fitted=$image
exec i3lock --nofork -i "$fitted"
