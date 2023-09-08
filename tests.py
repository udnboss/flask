import unittest

def myFunc(x:int):
    if type(x) is not int: 
        raise Exception("not int")
    return x*x

class TestMyFunc(unittest.TestCase):
    def test_myFunc(self):
        self.assertEqual(myFunc(2), 4)
        self.assertEqual(myFunc(3), 9)
        with self.assertRaises(Exception):
            myFunc('a')

if __name__ == '__main__':
    unittest.main()
