#!/usr/bin/env python3
"""
Serial interface for the pan/tilt stepper firmware.

Protocol (matches the Arduino sketch, CRC removed):
    TX: [command_byte]                        -> 1 byte
    RX: RESP_OK (0x02) or RESP_ERR (0x03)      -> 1 byte
    (TELL_DEG_H / TELL_DEG_V reply with 4 raw little-endian float bytes instead)
"""

import struct
import time

import serial


class StepperSerial:
    """Wraps a serial connection to the pan/tilt stepper firmware and sends protocol commands."""

    STEP_COMMAND = 0x01
    RESP_OK      = 0x02
    RESP_ERR     = 0x03
    SET_DEG_45   = 0x04
    SET_DEG_90   = 0x05
    SET_DEG_0    = 0x06
    TELL_DEG_H   = 0x07
    TELL_DEG_V   = 0x08

    CMD_NAMES = {
        STEP_COMMAND: "STEP_COMMAND",
        SET_DEG_0:    "SET_DEG_0",
        SET_DEG_45:   "SET_DEG_45",
        SET_DEG_90:   "SET_DEG_90",
        TELL_DEG_H:   "TELL_DEG_H",
        TELL_DEG_V:   "TELL_DEG_V",
    }

    def __init__(self, port: str, baud: int = 115200, settle_s: float = 2.0, timeout: float = 1.0):
        """Open the serial port and give the MCU time to reset before use."""
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = serial.Serial(port, baud, timeout=timeout)
        time.sleep(settle_s)  # many boards reset on serial open
        self.ser.reset_input_buffer()

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _name(self, command: int) -> str:
        return self.CMD_NAMES.get(command, hex(command))

    def send_command(self, command: int, timeout_s: float = None) -> bool:
        """Send a single command byte and wait for a 1-byte response. Returns True on RESP_OK."""
        timeout_s = self.timeout if timeout_s is None else timeout_s
        self.ser.reset_input_buffer()
        self.ser.write(bytes([command]))

        deadline = time.time() + timeout_s
        while time.time() < deadline:
            if self.ser.in_waiting:
                resp = self.ser.read(1)
                if not resp:
                    continue
                code = resp[0]
                if code == self.RESP_OK:
                    return True
                elif code == self.RESP_ERR:
                    return False
                else:
                    raise ValueError(f"{self._name(command)} -> unexpected byte 0x{code:02X}")
            time.sleep(0.005)

        raise TimeoutError(f"{self._name(command)} -> no response")

    def query_angle(self, command: int, timeout_s: float = None) -> float:
        """
        Send TELL_DEG_H or TELL_DEG_V and return the float angle reported back.
        The firmware sends this as 4 raw IEEE-754 bytes via
        Serial.write((uint8_t*)&angle, sizeof(angle)) -- little-endian on
        AVR/ESP32 -- so we read exactly 4 bytes and struct.unpack them.
        """
        timeout_s = self.timeout if timeout_s is None else timeout_s
        self.ser.reset_input_buffer()
        self.ser.write(bytes([command]))

        deadline = time.time() + timeout_s
        buf = b""
        while time.time() < deadline and len(buf) < 4:
            if self.ser.in_waiting:
                buf += self.ser.read(4 - len(buf))
            else:
                time.sleep(0.005)

        if len(buf) < 4:
            raise TimeoutError(f"{self._name(command)} -> got {len(buf)}/4 bytes: {buf.hex(' ')}")

        return struct.unpack("<f", buf)[0]

    # --- Convenience wrappers -------------------------------------------------

    def step(self) -> bool:
        return self.send_command(self.STEP_COMMAND)

    def set_deg_0(self) -> bool:
        return self.send_command(self.SET_DEG_0)

    def set_deg_45(self) -> bool:
        return self.send_command(self.SET_DEG_45)

    def set_deg_90(self) -> bool:
        return self.send_command(self.SET_DEG_90)

    def tell_deg_h(self) -> float:
        return self.query_angle(self.TELL_DEG_H)

    def tell_deg_v(self) -> float:
        return self.query_angle(self.TELL_DEG_V)


if __name__ == "__main__":
    # Minimal usage example.
    with StepperSerial("/dev/ttyESP") as stepper:
        stepper.step()
        print(f"H: {stepper.tell_deg_h():.3f} deg  V: {stepper.tell_deg_v():.3f} deg")