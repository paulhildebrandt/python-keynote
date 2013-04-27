"""
keynote_api
~~~~~~~~~~

Pythonic interface to Apples Keynote 09 file format.

It currently is a read only interface.

Requires Python 2.6

:license: MIT, see LICENSE for more details.
"""
__version__ = "0.5"

import zipfile
import lxml.etree


def _xp(elem, path):
    """ A quick way to access XPath """
    return elem.xpath(path, namespaces=elem.nsmap)


def _xpa(elem, path):
    """ A quick way to access XPath attribute """
    attribute = elem.xpath(path, namespaces=elem.nsmap)
    if attribute:
        return attribute[0]
    else:
        return None


def _get_element_text(element):
    """ This removes the namespace text from the tag and just returns the tag
        text
    """
    tag = element.tag
    return tag[tag.index("}") + 1:]


def _get_element_lineage(element):
    try:
        parent = element.getparent()
        lineage = _get_element_lineage(parent)
        tag_text = _get_element_text(element)
        if lineage:
            return lineage + "::" + tag_text
        else:
            return tag_text
    except AttributeError:
        return ""


class Picture(object):
    """This object holds attributes for images used in a keynote file.

    """
    # The pictures in a keynote document can be found using the following xpath
    # "//key:presentation/key:slide-list/key:slide/key:page/sf:layers/" +
    # "sf:layer/sf:drawables/sf:media/sf:content/sf:image-media/" +
    # "sf:filtered-image/sf:unfiltered/sf:data"
    def __init__(self, root):
        self.root = root
        self.relative_path = None  #: Path including name of the image
        self.natural_width = None  #: Width of picture as it was when imported into Keynote
        self.natural_height = None  #: Height of picture as it was when imported into Keynote
        self.display_width = None  #: Width of picture displayed in slide
        self.display_height = None  #: Height of picture displayed in slide
        self.display_x = None  #: Upper right corner X coordinate of picture on slide
        self.display_y = None  #: Upper right corner Y coordinate of picture on slide
        self.keynote_path = ""

    def __repr__(self):
        return str(self.__dict__)

    def export(self, directory):
        """
        Save the picture to the given path.

        The image will retain its name.  This may be confusing if the image
        was dropped on the keynote file because keynote renames them to
        droppedImage<xx>.<ext>  which isn't very helpful.

        :param directory: dir where to put the image.
        """
        # Is it a problem that we do this for each picture?
        # Maybe we need a method on the slide to save all pictures.
        keynote_file = zipfile.ZipFile(self.keynote_path)
        keynote_file.extract(self.relative_path, directory)


class Slide(object):
    """
    This object allows you to access Keynote Slide attributes and objects the
    slide contains.
    """
    def __init__(self, root):
        self.root = root
        self.__id = None
        self.__pictures = []
        self.keynote_path = ""

    def __repr__(self):
        return str(self.__dict__)

    @property
    def id(self):
        """
        Name of slide
        """
        if not self.__id:
            self.__id = _xpa(self.root, "@sfa:ID")
        return self.__id

    @property
    def pictures(self):
        """
        List of picture objects that appear on the slide
        """
        if not self.__pictures:
            self.__populate_pictures()
        return self.__pictures

    # TODO: Internalize this into the picture object
    def __populate_pictures(self):
        """ Get the picture data out of the Keynote file and put it into
            our Python object
        """
        path_to_data = ".//key:page/sf:layers/sf:layer/sf:drawables/sf:media"\
            "/sf:content/sf:image-media/sf:filtered-image/sf:unfiltered/sf:data"
        self.data = _xp(self.root, path_to_data)
        for element in self.data:
            picture = Picture(element)
            picture.relative_path = _xp(element, "@sf:path")[0]
            # this is perfectly fine... nothing to worry about here... :-(
            media_element = element.getparent().getparent().getparent().getparent().getparent()
            picture.display_x = float(_xpa(media_element, "sf:geometry/sf:position/@sfa:x"))
            picture.display_y = float(_xpa(media_element, "sf:geometry/sf:position/@sfa:y"))
            picture.display_width = float(_xpa(media_element, "sf:geometry/sf:size/@sfa:w"))
            picture.display_height = float(_xpa(media_element, "sf:geometry/sf:size/@sfa:h"))
            picture.natural_width = int(_xpa(media_element, "sf:geometry/sf:naturalSize/@sfa:w"))
            picture.natural_height = int(_xpa(media_element, "sf:geometry/sf:naturalSize/@sfa:h"))
            picture.keynote_path = self.keynote_path
            self.__pictures.append(picture)


class Keynote(object):
    """
    Class to make the Apple Keynote file Pythonic
    """
    def __init__(self, path):
        self.path = path  #: Path on disk to the keynote file.
        self.doc = lxml.etree.parse(zipfile.ZipFile(path).open('index.apxl'))
        self.__width = None
        self.__height = None
        self.__slides = []

    @property
    def width(self):
        """ Width of the presentation in pixels.

         Example: 1920
        """
        if not self.__width:
            self.__width = int(_xpa(self.doc.getroot(),
                                    "//key:presentation/key:size/@sfa:w"))
        return self.__width

    @property
    def height(self):
        """ Height of the presentation in pixels.

         Example: 1024
        """
        if not self.__height:
            self.__height = int(_xpa(self.doc.getroot(),
                                     "//key:presentation/key:size/@sfa:h"))
        return self.__height

    @property
    def slides(self):
        """
        List of slide objects in the presentation.
        """
        if not self.__slides:
            self.__populate_slides()
        return self.__slides

    def __populate_slides(self):
        slide_roots = _xp(self.doc.getroot(), "//key:slide ")
        for slide_root in slide_roots:
            slide = Slide(slide_root)
            slide.keynote_path = self.path
            self.__slides.append(slide)