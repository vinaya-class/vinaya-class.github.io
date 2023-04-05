#!/usr/bin/env bash

while true; do
    inotifywait -qr -e modify pali-lessons.org

    if make pali-lessons; then
        notify-send -t 5000 "OK: pali-lessons"
    else
        notify-send --urgency=critical "FAILURE: pali-lessons"
    fi
done
