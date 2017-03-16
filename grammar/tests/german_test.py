# -*- coding: utf-8 -*-
import unittest
import grammar.german as gg
#import importlib

class german(unittest.TestCase):

#    importlib.reload(gg)
    def test_singular_plural_ize(self):
        words = [
            [ u'katze', u'katzen' ]
        ]
        for pair in words:
            self.assertEqual(gg.singularize(pair[1]), pair[0])
            self.assertEqual(gg.pluralize(pair[0]), pair[1])

if __name__ == '__main__':
    unittest.main()
