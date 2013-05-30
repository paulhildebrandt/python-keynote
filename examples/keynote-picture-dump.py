#!/usr/bin/env python
"""
Dump out all the pictures from a keynote presentation keeping their
adjusted sizes.  It assumes the slides are for arranging pictures
on a full or half size presentation board.

This example relies on having PIL installed.
"""
import os
import sys
import argparse


try:
    import Image
    PIL_exists = True
except ImportError:
    PIL_exists = False

from keynote_api import Keynote


DPI = 72  # printing dots per inch


def parse_args():
    parser = argparse.ArgumentParser(description='Keynote Picture Extractor')
    parser.add_argument('--resize', action="store_true", default=False,
                        help='resize the pictures to match board dimensions.')
    parser.add_argument('--gui', action="store_true", default=False,
                        help='Sends output to a GUI window.')
    parser.add_argument('keynote_filename', action="store",
                        help='Name of Apple Keynote 09 file.')
    args = parser.parse_args()

    return args


def main(args):

    if args.resize:
        if not PIL_exists:
            args.resize = False
            output("PIL isn't installed.  I can't resize images")

    keynote = Keynote(args.keynote_filename)
    if args.resize:
        aspect_ratio = keynote.width / float(keynote.height)
        if aspect_ratio > 1.7:
            board_width = 90  # inches
            output("Working with a full board.")
        else:
            board_width = 45  # inches
            output("Working with a half board.")
        sizing_factor = (board_width * DPI) / float(keynote.width)
    folder_name, dummy_ext = os.path.splitext(os.path.basename(args.keynote_filename))
    folder_name += "-pictures"
    folder_name = os.path.join(os.path.dirname(args.keynote_filename), folder_name)
    if os.path.exists(folder_name):
        output("Looks like %s already exists.  Please delete or move it aside."
              % folder_name)
        return 1
    output("Putting pictures in folder: %s" % folder_name)
    try:
        os.mkdir(folder_name)
    except OSError:
        output('Unable to make folder: %s' % folder_name)
        return 1
    for i, slide in enumerate(keynote.slides):
        slide_num = i + 1
        slide_folder = os.path.join(folder_name, "Slide %s" % slide_num)
        for j, picture in enumerate(slide.pictures):
            if not os.path.exists(slide_folder):
                output("Creating folder for Slide %s : %s" % (slide_num, slide_folder))
                try:
                    os.mkdir(slide_folder)
                except OSError:
                    pass
            picture_path = os.path.join(slide_folder, picture.relative_path)
            output("Saving Picture: %s" % picture_path)
            picture.export(slide_folder)
            if args.resize:
                # Resize picture to match keynote display size
                try:
                    img = Image.open(picture_path)
                    img = img.resize((int(picture.display_width * sizing_factor),
                        int(picture.display_height * sizing_factor)),
                        Image.ANTIALIAS)
                    img.save(picture_path)
                except IOError, errObj:
                    output('ERROR: Unable to resize %s. %s' % (picture_path, errObj))

    return 0


GUI = None
def output(outstr):
    if GUI:
        tags = ("ERROR",) if outstr.startswith('ERROR') else None
        GUI.insert(END, outstr+"\n", tags)
        print('GUI: %s' % outstr)
    else:
        print(outstr)

if __name__ == "__main__":
    args = parse_args()
    if args.gui:
        from Tkinter import *
        root = Tk()
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)
        text = Text(root, width=140, wrap=WORD, yscrollcommand=scrollbar.set)
        text.tag_config("ERROR", background="yellow", foreground="red")
        text.pack()
        GUI = text
    result = main(args)
    if GUI:
        root.mainloop()
    sys.exit(result)
