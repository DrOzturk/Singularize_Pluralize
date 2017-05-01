# -*- coding: utf-8 -*-
import unittest
import grammar.english as ge
#import importlib

class eglish(unittest.TestCase):

#    importlib.reload(gg)
    def test_singular_plural_ize(self):
        words = [
            [ u'child', u'children' ]
        ]
        for pair in words:
            self.assertEqual(ge.singularize(pair[1]), pair[0])
            self.assertEqual(ge.pluralize(pair[0]), pair[1])

if __name__ == '__main__':
    unittest.main()
