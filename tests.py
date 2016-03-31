#
# Test Unitaires
# TODO : compléter les tests
#
from models import City, User, Travel, Transport, Accomodation
import unittest

class City_TestCase(unittest.TestCase):
    """Tests unitaires du modèle City
    """
    def test_HasDoc(self):
        self.assertLess(10, len(City.__doc__))

class User_TestCase(unittest.TestCase):
    """Tests unitaires du modèle User
    """
    def test_HasDoc(self):
        self.assertLess(10, len(User.__doc__))

class Travel_TestCase(unittest.TestCase):
    """Tests unitaires du modèle Travel
    """
    def test_HasDoc(self):
        self.assertLess(10, len(Travel.__doc__))

class Transport_TestCase(unittest.TestCase):
    """Tests unitaires du modèle Transport
    """
    def test_HasDoc(self):
        self.assertLess(10, len(Transport.__doc__))

class Accomodation_TestCase(unittest.TestCase):
    """Tests unitaires du modèle Accomodation
    """
    def test_HasDoc(self):
        self.assertLess(10, len(Accomodation.__doc__))

if __name__ == '__main__':
    print("======Tests Start")
    unittest.main(exit=False,verbosity=2)
    a=input("fini : appuyez sur une touche!")
    print("=================")
    print (__doc__)