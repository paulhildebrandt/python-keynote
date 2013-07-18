#!/usr/bin/env python
"""
This file dumps everything the KeynoteAPI library knows about a keynote file.
"""
import sys

from keynote_api import Keynote

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: keynote-info.py <filename.key>")
        sys.exit()
    keynote_file = sys.argv[1]

    keynote = Keynote(keynote_file)
    print("Keynote Size: %sx%s" % (keynote.width, keynote.height))
    print("Number of slides: %s" % len(keynote.slides))
    for i, slide in enumerate(keynote.slides):
        print("Slide %s: %s" % (i, slide.id))
        for j, picture in enumerate(slide.pictures):
            print("    Picture %s : %s" % (j, picture.relative_path))
            print("        unfiltered_id  : %s" % picture.unfiltered_id)
            print("        natural_width  : %s" % picture.natural_width)
            print("        natural_height : %s" % picture.natural_height)
            print("        display_width  : %s" % picture.display_width)
            print("        display_height : %s" % picture.display_height)
            print("        display_x      : %s" % picture.display_x)
            print("        display_y      : %s" % picture.display_y)
            print("        rotate_angle   : %s" % picture.rotate_angle)
        for j, movie in enumerate(slide.movies):
            print("    Movie %s : %s" % (j, movie.relative_path))
            print("        poster_frame_path : %s" % movie.poster_frame_path)
            print("        natural_width  : %s" % movie.natural_width)
            print("        natural_height : %s" % movie.natural_height)
            print("        display_width  : %s" % movie.display_width)
            print("        display_height : %s" % movie.display_height)
            print("        display_x      : %s" % movie.display_x)
            print("        display_y      : %s" % movie.display_y)
            print("        rotate_angle   : %s" % movie.rotate_angle)

