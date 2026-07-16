# Pi 3D Scanner - Touch UI

Touchscreen control app for a Raspberry Pi 5 based laser-triangulation 3D
scanner, built for a 320x480 portrait panel.

## Layout

```
main.py                      entry point only
scanner/
  core/
    config.py                screen size, kiosk flag, pins, paths
    settings.py               load/save settings.json
    worker.py                 generic QThread hardware worker
  hardware/
    shell.py                  safe subprocess wrapper for terminal commands
    gpio_io.py                LED/GPIO wrapper (+ mock fallback off-Pi)
    camera.py                 camera init/capture (rpicam-* CLI by default)
    motion.py                 jog / home / calibrate / triangulation logic
  ui/
    theme.py                  colours + stylesheets
    widgets.py                IconTile, top_bar, status_pill
    main_window.py            QStackedWidget shell, kiosk sizing
    screens/
      home.py, calibration.py, settings_screen.py, control.py, info.py
systemd/pi-scanner.service    optional systemd unit (X11 path)
scripts/install_kiosk.sh      one-shot setup script, run on the Pi
```

Rule of thumb for where new code goes: if it talks to hardware or a
terminal command, it goes under `scanner/hardware/`. If it's UI, it goes
under `scanner/ui/`. `main.py` never grows past a few lines.

## Running

```bash
python3 -m pip install --break-system-packages -r requirements.txt
python3 main.py                 # boots straight into kiosk mode
SCANNER_KIOSK=0 python3 main.py # windowed, for desktop development
```

The app runs fine off a Pi too - `gpiozero` and `rpicam-*` calls fall back
to logged/simulated results automatically (see `hardware/gpio_io.py` and
`hardware/camera.py`), so you can build out the UI on a laptop.

## Wiring in real hardware

- **GPIO/motors/sensors**: add calls in `scanner/hardware/*.py` using
  `gpiozero`, `RPi.GPIO`, or `smbus2` for I2C. Never call hardware
  libraries from the `ui/` package directly - screens only call functions
  in `hardware/`, via a `HardwareWorker` so the UI thread never blocks.
- **Terminal commands**: use `scanner/hardware/shell.py`'s `run_command()`,
  which always takes a list of args (no `shell=True`), captures
  stdout/stderr, and enforces a timeout.

## Boot straight into kiosk mode

Two supported paths, pick based on your desktop session
(`echo $XDG_SESSION_TYPE` tells you which you're on):

### Wayland / labwc (default on current Raspberry Pi OS)
1. `sudo raspi-config` -> System Options -> Boot / Auto Login -> **Desktop Autologin**
2. `sudo raspi-config` -> Display Options -> Screen Blanking -> **Disable**
3. Add to `~/.config/labwc/autostart`:
   ```
   python3 /home/pi/pi_scanner/main.py &
   ```
4. Reboot. `KIOSK_MODE` defaults to `True`, so it launches frameless + fullscreen immediately.

### X11 (systemd-managed, auto-restarts on crash)
1. `sudo raspi-config` -> System Options -> Boot / Auto Login -> **Desktop Autologin**
2. Copy `systemd/pi-scanner.service` to `/etc/systemd/system/`, fixing the
   paths/user if your app isn't at `/home/pi/pi_scanner`.
3. `sudo systemctl daemon-reload && sudo systemctl enable pi-scanner.service`
4. Reboot.

`scripts/install_kiosk.sh` does the dependency install and picks the right
path automatically based on your session type - run it once from the Pi.

## Config

Everything tunable lives in `scanner/core/config.py`: screen size, the
kiosk flag (env override: `SCANNER_KIOSK=0`), and GPIO pin numbers.
User-adjustable values (laser power, LED brightness, etc.) are separate -
those live in `settings.json`, created next to `main.py` the first time
you hit Save on the Settings screen.
