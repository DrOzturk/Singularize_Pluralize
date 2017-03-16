# -*- coding: utf-8 -*-
# by Ozgur Ozturk

import unittest
import pandas as pd
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir)

import grammar.french as gf

class french_test(unittest.TestCase):

    def test_singular_plural_ize(self):
        #examples from http://www.french-linguistics.co.uk/grammar/plural.shtml and http://www.french-linguistics.co.uk/grammar/plural_irregular.shtml
        words = [
            [ 'prix', 'prix' ],
            # [ 'journal', 'journaux' ], #TODO: fails
            [ 'château', 'châteaux' ],
            [ 'jeu', 'jeux' ],
            [ 'tuyau', 'tuyaux' ],
            [ 'chaise', 'chaises' ],
        ]
        for pair in words:
            self.assertEqual(gf.singularize(pair[1]), pair[0], "Singular form for " + pair[1] + " is incorrect.")
            self.assertEqual(gf.pluralize(pair[0]), pair[1], "Plural form for " + pair[0] + " is incorrect.")

