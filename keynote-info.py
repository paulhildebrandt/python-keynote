import sys

from KeynoteAPI import Keynote


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: keynote-info.py <filename.key>")
    keynote_file = sys.argv[1]

    keynote = Keynote(keynote_file)
    print("Keynote Size: %s" % keynote.size)
    print("Number of slides: %s" % len(keynote.slides))
    for i, slide in enumerate(keynote.slides):
        print("Slide %s" % slide.id)
        for picture in slide.pictures:
            print(picture)