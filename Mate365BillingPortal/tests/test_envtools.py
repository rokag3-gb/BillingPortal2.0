from django.test import TestCase
from Mate365BillingPortal.settings import envtools
import os

class EnvtoolsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        os.environ["BOOL_TRUE"] = "True"
        os.environ["BOOL_FALSE"] = "False"
        os.environ["BOOL_T"] = "T"
        os.environ["BOOL_F"] = "F"
        os.environ["INT_NINE"] = "9"
        os.environ["INT_MINUS1K"] = "-1000"


    def test_getBool(self):
        self.assertEqual(envtools.getBool(""), None)
        self.assertEqual(envtools.getBool("BOOL_TRUE"), True)
        self.assertEqual(envtools.getBool("BOOL_FALSE"), False)
        self.assertNotEqual(envtools.getBool("BOOL_T"), True)
        self.assertNotEqual(envtools.getBool("BOOL_F"), False)

    def test_getInt(self):
        self.assertEqual(envtools.getInt(""), None)
        self.assertEqual(envtools.getInt("INT_NINE"), 9)
        self.assertEqual(envtools.getInt("INT_MINUS1K"), -1000)