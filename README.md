# 4velma
View images on a Raspberry Pi using your TV.

When my family started using digital cameras, we nearly stopped printing pictures. We outside of a holiday card, we sharing pictures using the display on the phone or the camera producing the image. My grandma Velma ended up with fewer pictures to look at.  Worse, yet, the displays we use to share are tiny!

4velma is a python script to display images, targeted at Raspberry Pi connected to a TV.  The idea is to take a Raspberry Pi and HDMI cable to my grandma's house, plug it in, and let her see pictures.  Grandma seems to be able to browse channels, but I thought that navigating through the USB file viewer on her Smart TV might be too much....

4velma comes with a script to monitor your SD-card reader for new files, copying new files for viewing.

## Dependencies
- Python 3.5:  Your mileage may vary with other versions.
- Pillow:  Read, display, and scale images.
- tkinter: Window (mis)management.
- *optional:* Anaconda, virtualenv, etc....
- [at](https://en.wikipedia.org/wiki/At_(Unix)): Useful in scheduling SD-card copy commands from udev.
- [udev](https://en.wikipedia.org/wiki/Udev): Watch for SD-card mount to copy new files.

## Installation
If you just want to kick the tires...

```sh
python 4velma.py -i /path/to/your/pictures -d 10
```

Closing the window or typing 'q' will terminate the script.  Replay or advance photos with 'd' and 'f' keys.

For more permanent installation, after downloading 4velma, create a virtual environment and edit your xsessionrc file to start up 4velma.


```sh
git clone https://github.com/jonathanlb/4velma
cd 4velma
conda create -n 4velma python=3.5
source activate 4velma
conda install Pillow
# edit xsessionrc to suit
cat xsessionrc >> ${HOME}/.xsessionrc
```

In order to watch for new pictures on an SD card

```
# install at to defer execution of SD read and copy commands.
sudo apt-get install at
# edit path variables in 99-local.rules so udev can read and copy camera images.
cat 99-local.rules >> /etc/udev/rules.d/99-local.rules
```
