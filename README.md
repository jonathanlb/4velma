# 4velma
View images on a Raspberry Pi using your TV.

When my family started using digital cameras, we nearly stopped printing pictures. We, outside of a holiday card, only shared pictures using the display on the phone or the camera producing the image. My grandma Velma ended up with fewer pictures to look at.  Worse, yet, the displays we use to share are tiny!

4velma is a python script to display images, targeted at Raspberry Pi connected to a TV.  The idea is to take a Raspberry Pi and HDMI cable to my grandma's house, plug it in, and let her see pictures.  Grandma seems to be able to browse channels, but I thought that navigating through the USB file viewer on her Smart TV might be too much....

4velma comes with a script which udev can execute when new files appear in the SD-card reader, copying new files for viewing.

## Dependencies
- Python 3.5:  Your mileage may vary with other versions.
- Pillow:  Read, display, and scale images.
- tkinter: Window management.
- *optional:* Anaconda, virtualenv, etc....

## Installation
```sh
git clone https://github.com/jonathanlb/4velma
cd 4velma
conda create -n 4velma python=3.5
source activate 4velma
conda install Pillow
# edit xsessionrc to suit
cat xsessionrc >> ${HOME}/.xsessionrc
```

The following command, for example, will cycle through the pictures every 10 seconds.
```sh
python 4velma.py -i /path/to/your/pictures -d 10
```

The will watch a mount point and copy new jpeg pictures to your picture directory.
```sh
python import.py -i /mnt/card -o /path/to/your/pictures
```

## Controls

- 'd' replay previous photo.
- 'f' advance to next photos.
- 'q' or closing the window to quit.
- backspace/delete show dialog to delete photos.
- '>' rotate image clockwise, overwriting original file.
- '<' rotate image counter clockwise, overwriting original file.

## Troubleshooting
### Python Environments
- Use the latest version of conda.

```
conda update conda
```
### Mounting SD cards
 - In ```/etc/fstab``` put
```
/dev/sdb1  /mnt/card  exfat-fuse ro,defaults,nofail,user,auto  0  0
```  Your card reader may show up as /dev/sda1.  Edit the device and mount directory to suit.
  - Install exfat-fuse to read Windows-formatted cards.
  
```
sudo apt-get install extfat-fuse
```
