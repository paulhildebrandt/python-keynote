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
    """ This removes the namespace text from the tag and just returns the tag text """
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
    def __init__(self, root):
        self.root = root
        self.relative_path = None
        self.natural_width = None
        self.natural_height = None
        self.display_width = None
        self.display_height = None
        self.display_x = None
        self.display_y = None

    def __repr__(self):
        return str(self.__dict__)


class Slide(object):
    def __init__(self, root):
        self.root = root
        self.__id = None
        self.__pictures = []

    def __repr__(self):
        return str(self.__dict__)

    @property
    def id(self):
        if not self.__id:
            self.__id = _xpa(self.root, "@sfa:ID")
        return self.__id

    @property
    def pictures(self):
        if not self.__pictures:
            self.__populate_pictures()
        return self.__pictures

    # TODO: Internalize this into the picture object
    def __populate_pictures(self):
        """ Get the picture data out of the Keynote file and put it into our Python object"""
        path_to_data = ".//key:page/sf:layers/sf:layer/sf:drawables/sf:media/sf:content/sf:image-media" \
                       "/sf:filtered-image/sf:unfiltered/sf:data"
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
            self.__pictures.append(picture)


class Keynote(object):
    """
    Class to make the Apple Keynote pythonic
    """
    def __init__(self, path):
        self.path = path
        self.doc = lxml.etree.parse(zipfile.ZipFile(path).open('index.apxl'))
        self.__size = None
        self.__slides = []

    @property
    def size(self):
        if not self.__size:
            width = _xpa(self.doc.getroot(), "//key:presentation/key:size/@sfa:w")
            height = _xpa(self.doc.getroot(), "//key:presentation/key:size/@sfa:h")
            self.__size = width + "x" + height
        return self.__size

    @property
    def slides(self):
        if not self.__slides:
            self.__populate_slides()
        return self.__slides

    def __populate_slides(self):
        slide_roots = _xp(self.doc.getroot(), "//key:slide ")
        for slide_root in slide_roots:
            slide = Slide(slide_root)
            self.__slides.append(slide)


    # TODO:
    # find out what media really does and maybe get all media
    # extent is cropping, look into that



    #for data in keynote.data:
    #    print("Path: %s" % _xp(data, "@sf:path"))
    #    print lxml.etree.tostring(data)
    #print(_xp(keynote.data[0].attrib, '@sf:path'))
    # Path to image path
    #self.data = _xp(self.doc.getroot(), "//key:presentation/key:slide-list/key:slide/key:page/sf:layers/sf:layer/sf:drawables/sf:media/sf:content/sf:image-media/sf:filtered-image/sf:unfiltered/sf:data")

