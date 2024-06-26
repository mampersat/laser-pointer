# laser-pointer
laser mounted on simple servo turret to point to interesting locations on a map

## Communications
```mermaid
sequenceDiagram
    participant Browser as Web Browser
    participant Hub as MQTT Hub
    participant Turret as Laser Turret Device

    Browser->>+Hub: Publish "target coordinates"

    Hub->>+Turret: Forward "target coordinates"

    Turret->>+Turret: Point laser to coordinates
```    

## Wiring
```mermaid
graph LR
    servo1 -- black(-) --> pico38[pico pin 38]
    servo1 -- red(+) --> pico36[pico pin 36]
    servo1 -- white --> pico22[pico pin 22]

    servo2 -- black(-) --> pico38[pico pin 38]
    servo2 -- red(+) --> pico36[pico pin 36]
    servo2 -- white --> pico24[pico pin 24]

    laser -- black(-) --> pico38[pico pin 38]
    laser -- white --> pico16[pico pin 16]
```

![turret on block](images/turret_on_block.jpg)

I have a large map (9ft x 6ft) in my home office. It's a triumph of cartography really. [You can get it here for $100](https://www.natgeomaps.com/re-world-executive-mural). Installation is the same as wall paper.

I had some servos (from R/C airplane hobby) and an extra raspberry pi and was inspired by an online tutorial (can't find link) in which the creator used hot glue to stick the servos and laser together... so now I have a thing which points a laser at my map.

Future goal is to have it read news stories from an API, figure out their location and point the laser at them. Like this weeks story about the ship stuck in the Suez canal.

![Suez Canal](images/suez_canal.jpg)

## Parts
* Raspberry pi 4 (SD card required 16gb works for me, micro HDMI cable recommended)
* 2 Servo's (futaba S3107 for now... might update for more accuracy)
* Laser (I got [these laser diodes](https://www.amazon.com/gp/product/B00VCR036Q/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) a few years ago to upgrade a nerf gun)
* Hot glue
* A base (block of wood for me)
* Wiring (I have tons of wiring stuff from other projects)
* A map ([NatGeo 9'x6' : $100](https://www.natgeomaps.com/re-world-executive-mural).)

I tried to get this working with an ESP8266, but getting 5V to the servos was proving to be a PITA and the project was sitting next to a raspberry pi so I switched.

Warning: requirements.txt and some raspberry pi gpio pin libraries not 100% automated
```
export GPIOZERO_PIN_FACTORY=pigpio
sudo pigpiod
```

## Callibration
Point to a well known point and allow user to adjust with keyboard

Detecting keyboard input is IMPOSSIBLE I think.
pygame + pynput require a display to be connected

Honalulu
Brisbane

## Projection
Not 100% perfect, but here's the plan
1. Manually locate a bunch of points using calibration setup
1. To project a new point, find the 2 closest and extrapolate along a line between them

## Raspberry PI pico
installint umqtt library
```
import mip
mip.install("umqtt.simple")
```
# 2024-06-16
x and y rand is 0 to 1000

servo x
left = 970000
right = 470000

servo y
top = 1370000
bottom = 1670000


