#!/usr/bin/sh
echo -n "4" > /sys/class/gpio/export
echo -n "40" > /sys/class/gpio/export
echo -n "41" > /sys/class/gpio/export
echo -n "out" > /sys/class/gpio/gpio4/direction
echo -n "out" > /sys/class/gpio/gpio40/direction
echo -n "out" > /sys/class/gpio/gpio41/direction
echo -n "strong" > /sys/class/gpio/gpio40/drive
echo -n "strong" > /sys/class/gpio/gpio41/drive
echo -n "1" > /sys/class/gpio/gpio4/value
echo -n "0" > /sys/class/gpio/gpio40/value
echo -n "0" > /sys/class/gpio/gpio41/value
