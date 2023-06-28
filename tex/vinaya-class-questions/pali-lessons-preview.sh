#!/usr/bin/env bash

if [[ "$ANSWERKEY" != "TRUE" ]]; then
    target="pali-lessons"
else
    target="pali-lessons-answerkey"
fi

while true; do
    inotifywait -qr -e modify pali-lessons.org

    if make $target; then
        notify-send -t 5000 "OK: $target"
    else
        notify-send --urgency=critical "FAILURE: $target"
    fi
done
