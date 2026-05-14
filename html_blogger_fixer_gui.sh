#!/bin/bash
# Launcher for html_blogger_fixer_gui.py
# Sets QT_QPA_PLATFORMTHEME=gtk3 so the native OS file dialog is used,
# enabling Ctrl+F to search files. Requires qt6-gtk-platformtheme installed:
#   sudo apt install qt6-gtk-platformtheme
export QT_QPA_PLATFORMTHEME=gtk3
exec python3 "$(dirname "$0")/html_blogger_fixer_gui.py" "$@"
