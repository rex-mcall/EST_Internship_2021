Neo-6M needs config on Pi to override default use of UART pins


```
sudo nano /boot/config.txt
```

At the end of the file add the following lines:

```
dtparam=spi=on
dtoverlay=pi3-disable-bt
core_freq=250
enable_uart=1
force_turbo=1
```

Raspbian uses the UART as a serial console, which needs to be turned off by changing
the /boot/cmdline.txt file.

```
sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt
sudo nano /boot/cmdline.txt
```

Replace the content with the follwing line (delete everything and replace it with the next line):

```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

```
sudo reboot
```

Now use:

```
ls -l /dev
```

Look for a line that says either:

```
serial0 -> ttyAMA0
```

or

```
serial0 -> ttyS0
```

If it says ttyAMA0 do this:

```
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
```

If it says ttyS0:

```
sudo systemctl stop serial-getty@ttyS0.service
sudo systemctl disable serial-getty@ttyS0.service
```

Now connect the pins:

```
Neo 6M VCC -----> Raspberry pi 5v
Neo 6M GND -----> Raspberry pi GND
Neo 6M  RX -----> Raspberry pi TX (gpio 14) //Not required in our case
Neo 6M  TX -----> Raspberry pi RX (gpio 15)
```

You should now be able to test the module with the test code in:

```
/experimental_code/rpiTests/neo6mTest
```