python-keynote
==============

python-keynote contains keynote_api a very simple Apple Keynote 09 file reader.

My current goal was to read all the pictures out of a keynote file and
figure out their sizes.  I wrote enough to do that but tried to keep
it general.  I hope to expand on it later but thought I would publish
what I had now.

I hope that maybe 4 people fine this handy. ;-)

It only works on Apple Keynote 09 files.

I wrote this on Python 2.7 and know it at least works there.

The idea is to present a Keynote file as series of nested Python objects.
keynote_api contains three classes and a few helper functions.

- keynote: The keynote document object.  It contains slides.
- slide: The slide object is really only useful to group pictures.
- picture: The picture object holds sizing and position information.

Here is a code snippet that demonstrates the library.  It is included as
a working program, keynote-info.py, in the examples directory.

.. code-block:: python

    keynote = Keynote(keynote_file)
    print("Keynote Size: %sx%s" % (keynote.width, keynote.height))
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
            picture.export(".")
            print("Picture saved")
