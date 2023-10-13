from django.test import SimpleTestCase
from . import dummy

class TestDummy(SimpleTestCase):

    def testAdd(self):

        response = dummy.addFunc(1,1)
        return self.assertEqual(response, 2)

    def testSubtract(self):

        response = dummy.subFunc(100,50)
        return self.assertEqual(response,50)