# Install Raspberry Pi OS
onto the Raspberry Pi 4 Model B - since the Pi is not pre-configured like a laptop. It is:
- Just hardware
- **No OS**, **no storage**, **no terminal**
-> I must set it up using a **MicroSD card** as hard drive that the Pi boots from
- microSD card (16GB+ recommended)
- The "Model B" suffix indicates variants with an Ethernet port
## Steps
- By default, Raspberry Pi devices check for an operating system on any SD card inserted in the SD card slot.
- install an operating system using [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager) (tool to flash the OS onto the micro SD card).
- use Imager to preconfigure credentials and remote access settings for your Raspberry Pi.
- Imager supports images packaged in the `.img` format as well as container formats like `.zip` or `.xz`.

On my Ubuntu PC, install the tool `rpi-imager` 
```bash
sudo apt install rpi-imager
```

run it:
```bash
rpi-imager
```

Then:
1. **Choose my Pi**
2. **Choose OS**  
    → Raspberry Pi OS (64-bit) - Imager shows the recommended version of Raspberry Pi OS for the device at the top of the list.
3. Plug in MicroSD card into my computer via adapter
4. **Choose Storage**  
    → microSD card
5. Click advanced settings:
    - Enable SSH (optional)
    - Set username/password
    - Set WiFi (optional)
6. Click **Write**

Then:
- Remove microSD and insert into Pi (slot underneath)

more on how to connect:
https://randomnerdtutorials.com/installing-raspbian-lite-enabling-and-connecting-with-ssh/
# First boot of Pi:
Now connect:
- microSD inserted ✔️
- HDMI → monitor ✔️
- USB keyboard ✔️
- USB mouse ✔️
- Power (USB-C) ✔️

-> The Pi will now boot into a **desktop environment**
-> I can open a terminal by clicking on the icon or:
-> Press `CTRL + ALT + T`
## Install GPIO libraries

The Konami scripts use Python to talk to the GPIO header. On current Raspberry Pi OS there are the following options of libraries to use:

| Library   | Debian package      | Role |
| --------- | ------------------- | ---- |
| **RPi.GPIO** | `python3-rpi.gpio` | Classic API; still common on Pi 4; **legacy** on newer OS/kernels. |
| **lgpio** | `python3-lgpio`    | Lower-level access; matches **Bookworm** / newer kernel expectations (see note 06). |
| **gpiozero** | `python3-gpiozero` | Higher-level API; depends on a pin factory (often `lgpio` on new OS). |

On the Raspberry Pi:

```bash
sudo apt update
sudo apt install python3-rpi.gpio python3-lgpio python3-gpiozero
```

Avoid mixing two GPIO libraries in the same program on the same pins.

