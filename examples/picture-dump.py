#!/usr/bin/env python
"""
Dump out all the pictures from a keynote presentation keeping their
adjusted sizes.  It assumes the slides are for arranging pictures
on a full or half size presentation board.

This example relies on having PIL installed.
"""
import os
import sys

try:
    import Image
    PIL_exists = True
except ImportError:
    PIL_exists = False

from keynote_api import Keynote


DPI = 72  # printing dots per inch

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: picture-dump.py <filename.key> [--resize]")
        sys.exit()
    keynote_file = sys.argv[1]
    resize = False
    if len(sys.argv) > 2 and sys.argv[2] == "--resize":
        if PIL_exists:
            resize = True
        else:
            print("PIL isn't installed.  I can't resize images")

    keynote = Keynote(keynote_file)
    if resize:
        aspect_ratio = keynote.width / float(keynote.height)
        if aspect_ratio > 1.7:
            board_width = 90  # inches
            print("Working with a full board.")
        else:
            board_width = 45  # inches
            print("Working with a half board.")
        sizing_factor = (board_width * DPI) / float(keynote.width)
    folder_name, dummy_ext = os.path.splitext(os.path.basename(keynote_file))
    folder_name += "-pictures"
    folder_name = os.path.join(os.path.dirname(keynote_file), folder_name)
    if os.path.exists(folder_name):
        print("Looks like %s already exists.  Please delete or move it aside."
              % folder_name)
        sys.exit()
    print("Putting pictures in folder: %s" % folder_name)
    try:
        os.mkdir(folder_name)
    except OSError:
        print('Unable to make folder: %s' % folder_name)
        sys.exit()
    for i, slide in enumerate(keynote.slides):
        slide_num = i + 1
        slide_folder = os.path.join(folder_name, "Slide %s" % slide_num)
        for j, picture in enumerate(slide.pictures):
            if not os.path.exists(slide_folder):
                print("Creating folder for Slide %s : %s" % (slide_num, slide_folder))
                try:
                    os.mkdir(slide_folder)
                except OSError:
                    pass
            picture_path = os.path.join(slide_folder, picture.relative_path)
            print("Saving Picture: %s" % picture_path)
            picture.export(slide_folder)
            if resize:
                # Resize picture to match keynote display size
                img = Image.open(picture_path)
                img = img.resize((int(picture.display_width * sizing_factor),
                                 int(picture.display_height * sizing_factor)),
                                 Image.ANTIALIAS)
                img.save(picture_path)