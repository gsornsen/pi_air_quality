#!/bin/bash -e

if $(grep -q "Raspberry Pi" /proc/cpuinfo 2> /dev/null)
then
    echo "Found Raspberry Pi CPU!"
else
    echo "This script is only for bootstrapping pi device!"
    exit 1
fi


sudo apt update
sudo apt install i2c-tools python3 python3-pip python-is-python3 python3-rpi.gpio
python3 -m pip install virtualenv

sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -aG i2c $USER
sudo su $USER
