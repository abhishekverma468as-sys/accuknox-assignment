from django.test import SimpleTestCase
from .rectangle import Rectangle


class TestRectangleInit(SimpleTestCase):

    def test_attributes_stored(self):
        r = Rectangle(10, 5)
        self.assertEqual(r.length, 10)
        self.assertEqual(r.width, 5)


class TestRectangleIterable(SimpleTestCase):

    def test_iteration_yields_two_items(self):
        r = Rectangle(7, 3)
        items = list(r)
        self.assertEqual(len(items), 2)

    def test_first_item_is_length(self):
        r = Rectangle(7, 3)
        items = list(r)
        self.assertEqual(items[0], {'length': 7})

    def test_second_item_is_width(self):
        r = Rectangle(7, 3)
        items = list(r)
        self.assertEqual(items[1], {'width': 3})

    def test_for_loop_works(self):
        r = Rectangle(12, 6)
        results = []
        for item in r:
            results.append(item)
        self.assertEqual(results, [{'length': 12}, {'width': 6}])