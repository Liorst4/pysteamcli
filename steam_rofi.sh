#!/usr/bin/env sh
# Launch steam games with rofi.

python3 -m pysteamcli -r "`python3 -m pysteamcli -l | rofi -dmenu -p Steam:`"
