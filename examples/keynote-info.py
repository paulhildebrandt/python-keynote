#!/usr/bin/env python
"""
This file dumps everything the KeynoteAPI library knows about a keynote file.
"""
import sys

from KeynoteAPI import Keynote


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: keynote-info.py <filename.key>")
        sys.exit()
    keynote_file = sys.argv[1]

    keynote = Keynote(keynote_file)
    print("Keynote Size: %s" % keynote.size)
    print("Number of slides: %s" % len(keynote.slides))
    for i, slide in enumerate(keynote.slides):
        print("Slide %s: %s" % (i, slide.id))
        for j, picture in enumerate(slide.pictures):
            print("    Picture %s : %s" % (j, picture.relative_path))
            print("        natural_width  : %s" % picture.natural_width)
            print("        natural_height : %s" % picture.natural_height)
            print("        display_width  : %s" % picture.display_width)
            print("        display_height : %s" % picture.display_height)
            print("        display_x      : %s" % picture.display_x)
            print("        display_y      : %s" % picture.display_y)
            picture.save_as()
            print("Picture saved")
