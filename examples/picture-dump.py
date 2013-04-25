#!/usr/bin/env python
"""
Dump out all the pictures from a keynote presentation keeping their
adjusted sizes.
"""
import os
import sys

import Image

from KeynoteAPI import Keynote


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: picture-dump.py <filename.key>")
        sys.exit()
    keynote_file = sys.argv[1]

    keynote = Keynote(keynote_file)
    folder_name, dummy_ext = os.path.splitext(os.path.basename(keynote_file))
    folder_name += "-pictures"
    folder_name = os.path.join(os.path.dirname(keynote_file), folder_name)
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
            picture.save_as(slide_folder)
            # Resize picture to match keynote display size
            img = Image.open(picture_path)
            img = img.resize((int(picture.display_width), int(picture.display_height)), Image.ANTIALIAS)
            img.save(picture_path)