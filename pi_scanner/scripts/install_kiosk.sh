#!/usr/bin/env bash
# One-shot setup: installs deps and wires the app to launch on boot.
# Run this ON THE PI, from inside the pi_scanner folder:
#   chmod +x scripts/install_kiosk.sh && ./scripts/install_kiosk.sh
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Installing from: $APP_DIR"

echo "--- Installing Python dependencies ---"
python3 -m pip install --break-system-packages -r "$APP_DIR/requirements.txt"

echo "--- Detecting desktop session type ---"
SESSION_TYPE="${XDG_SESSION_TYPE:-unknown}"
echo "XDG_SESSION_TYPE=$SESSION_TYPE"

if [ "$SESSION_TYPE" = "wayland" ]; then
  echo "--- Wayland (labwc) detected: installing autostart entry ---"
  mkdir -p "$HOME/.config/labwc"
  AUTOSTART_LINE="python3 $APP_DIR/main.py &"
  touch "$HOME/.config/labwc/autostart"
  if ! grep -qF "$APP_DIR/main.py" "$HOME/.config/labwc/autostart" 2>/dev/null; then
    echo "$AUTOSTART_LINE" >> "$HOME/.config/labwc/autostart"
    echo "Added launch line to ~/.config/labwc/autostart"
  else
    echo "Autostart entry already present, skipping."
  fi
  echo
  echo "Next steps (manual, one-time):"
  echo "  1. sudo raspi-config -> System Options -> Boot / Auto Login -> Desktop Autologin"
  echo "  2. sudo raspi-config -> Display Options -> Screen Blanking -> Disable"
  echo "  3. Reboot: sudo reboot"
else
  echo "--- X11 (or unknown) session: installing systemd service ---"
  sed "s#/home/pi/pi_scanner#$APP_DIR#g; s#User=pi#User=$USER#g; s#Group=pi#Group=$USER#g" \
    "$APP_DIR/systemd/pi-scanner.service" | sudo tee /etc/systemd/system/pi-scanner.service > /dev/null
  sudo systemctl daemon-reload
  sudo systemctl enable pi-scanner.service
  echo
  echo "Service installed. Next steps (manual, one-time):"
  echo "  1. sudo raspi-config -> System Options -> Boot / Auto Login -> Desktop Autologin"
  echo "  2. Reboot: sudo reboot"
  echo "  3. Check status any time with: systemctl status pi-scanner.service"
fi

echo
echo "Done. Set SCANNER_KIOSK=0 as an env var if you ever need to run it windowed for debugging."
