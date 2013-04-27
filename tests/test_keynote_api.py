import os
from unittest import TestCase

from keynote_api import Keynote

TEST_IMG = "IMG_2274-1.jpg"


def _get_fixture_path(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), name)


class TestPicture(TestCase):
    def setUp(self):
        self.keynote = Keynote(_get_fixture_path("test.key"))
        self.slide = self.keynote.slides[1]

    def test_picture_count(self):
        self.assertEquals = self.slide.pictures[0]

    def test_picture_properties(self):
        picture = self.slide.pictures[0]
        self.assertEquals(picture.relative_path, TEST_IMG)
        self.assertEquals(picture.natural_width, 1920)
        self.assertEquals(picture.natural_height, 2570)
        self.assertEquals(picture.display_width, 507.2684020996094)
        self.assertEquals(picture.display_height, 678.9998779296875)
        self.assertEquals(picture.display_x, 37.0)
        self.assertEquals(picture.display_y, -33.0)

    def test_saveas(self):
        picture = self.slide.pictures[0]
        picture.save_as()
        self.assertTrue(os.path.exists(TEST_IMG))
        os.remove(TEST_IMG)


class TestSlide(TestCase):
    def setUp(self):
        self.keynote = Keynote(_get_fixture_path("test.key"))

    def test_count(self):
        self.assertEquals(len(self.keynote.slides), 2)

    def test_id(self):
        self.assertEquals(self.keynote.slides[0].id, "BGSlide-0")


class TestKeynote(TestCase):
    def setUp(self):
        self.keynote = Keynote(_get_fixture_path("test.key"))

    def test_size(self):
        self.assertEquals(self.keynote.size, "1920x1080")
