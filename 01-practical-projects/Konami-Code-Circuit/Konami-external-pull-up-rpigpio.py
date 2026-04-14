#!/usr/bin/env python3
"""
Same behavior as Konami-internal-pull-up-rpigpio.py, but for breadboard wiring with *external* ~10 kΩ
pull-ups to 3.3 V (pin 1) and buttons tying each GPIO to GND when pressed.

Do NOT enable internal pull-ups here - the resistors on the board define the idle HIGH.

Requires: RPi.GPIO, and for fullscreen message: python3-tk (usually preinstalled on Desktop Pi OS).
See 03-Wiring-Hardware.md (Wiring option 2) for hardware.
"""

import os
import sys
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# INPUT PINS: external pull-up on breadboard; active LOW when pressed
pins = {
    "UP": 17,
    "DOWN": 27,
    "LEFT": 22,
    "RIGHT": 23,
    "B": 24,
    "A": 25,
    "RESET": 5,
}

GREEN_LED = 18
RED_LED = 16

for pin in pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

for led in (GREEN_LED, RED_LED):
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)


def leds_off():
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.output(RED_LED, GPIO.LOW)


KONAMI = ["UP", "UP", "DOWN", "DOWN", "LEFT", "RIGHT", "LEFT", "RIGHT", "B", "A"]

DEBOUNCE_S = 0.05


def read_pressed_button():
    for name, pin in pins.items():
        if GPIO.input(pin) == GPIO.LOW:
            return name
    return None


def wait_for_release():
    time.sleep(DEBOUNCE_S)
    while read_pressed_button() is not None:
        time.sleep(0.01)


def wait_for_press():
    while True:
        pressed = read_pressed_button()
        if pressed is not None:
            time.sleep(DEBOUNCE_S)
            if read_pressed_button() == pressed:
                return pressed
        time.sleep(0.01)


def blink_reset_ack() -> None:
    leds_off()
    for _ in range(2):
        GPIO.output(GREEN_LED, GPIO.HIGH)
        time.sleep(0.06)
        leds_off()
        time.sleep(0.05)


def blink_feedback(correct: bool, duration: float = 0.1):
    leds_off()
    if correct:
        GPIO.output(GREEN_LED, GPIO.HIGH)
    else:
        GPIO.output(RED_LED, GPIO.HIGH)
    time.sleep(duration)
    leds_off()


def show_hire_me_fullscreen():
    try:
        import tkinter as tk
    except ImportError:
        print("HIRE ME! (install python3-tk for on-screen text)")
        return

    has_display = "DISPLAY" in os.environ or "WAYLAND_DISPLAY" in os.environ
    if not (sys.platform == "linux" and has_display):
        print("HIRE ME! (no GUI display; connect a monitor or set DISPLAY)")
        return

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-1>", lambda e: root.destroy())

    label = tk.Label(
        root,
        text="Hire Me!",
        fg="#00ff66",
        bg="black",
        font=("Sans", 72, "bold"),
    )
    label.pack(expand=True)

    root.after(30_000, root.destroy)
    root.mainloop()


def main():
    input_sequence = []

    print(
        "Konami: ↑↑↓↓←→←→BA - external pull-ups on breadboard; "
        "RESET clears. One logical press per tap (debounced)."
    )
    try:
        while True:
            wait_for_release()
            press = wait_for_press()

            print("Pressed:", press)

            if press == "RESET":
                input_sequence = []
                print("Reset - sequence cleared.")
                blink_reset_ack()
                wait_for_release()
                continue

            input_sequence.append(press)
            input_sequence = input_sequence[-len(KONAMI) :]

            n = len(input_sequence)
            correct_prefix = input_sequence == KONAMI[:n]
            blink_feedback(correct_prefix, duration=0.1)

            if input_sequence == KONAMI:
                print("KONAMI - HIRE ME!")
                leds_off()
                GPIO.output(GREEN_LED, GPIO.HIGH)
                show_hire_me_fullscreen()
                break

            wait_for_release()

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
