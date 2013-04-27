import os
from unittest import TestCase

from keynote_api import Keynote

TEST_IMG = "IMG_2258-1.jpg"


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
        self.assertEquals(picture.display_width, 1374.0)
        self.assertEquals(picture.display_height, 1839.15625)
        self.assertEquals(picture.display_x, 2228.5)
        self.assertEquals(picture.display_y, -105.0)

    def test_export(self):
        picture = self.slide.pictures[0]
        picture.export(".")
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

    def test_width(self):
        self.assertEquals(self.keynote.width, 3456)

    def test_height(self):
        self.assertEquals(self.keynote.height, 1728)