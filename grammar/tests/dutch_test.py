import unittest
import pandas as pd
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,parentdir)

import grammar.dutch as gd

class dutch_test(unittest.TestCase):

    def test_singular_plural_ize(self):
        words = [
            [ 'fiets', 'fietsen' ],
        ]
        for pair in words:
            self.assertEqual(gd.singularize(pair[1]), pair[0], "Singular form for " + pair[1] + " is incorrect.")
            self.assertEqual(gd.pluralize(pair[0]), pair[1], "Plural form for " + pair[0] + " is incorrect.")

    def test_pluralize_stat(self):
        # Assert "auto's" as plural of "auto".
        self.assertEqual("auto's", gd.pluralize("auto"))
        # Assert the accuracy of the pluralization algorithm.
        i, n = 0, 0
        for row in pd.read_csv(os.path.join(currentdir, "corpora", "wordforms-nl-celex.csv")).itertuples():
            sg = row[3]
            pl = row[4]
            if gd.pluralize(sg) == pl:
                i +=1
            n += 1
        accuracy = float(i) / n
        print("pattern.nl.pluralize() accuracy: {}".format(str(accuracy)))
        desired_accuracy = 0.74
        self.assertTrue(float(i) / n > desired_accuracy, "pattern.nl.pluralize() accuracy {} is below desired {}.".format(str(accuracy),desired_accuracy))

    def test_singularize_stat(self):
        # Assert the accuracy of the singularization algorithm.
        i, n = 0, 0
        for row in pd.read_csv(os.path.join(currentdir, "corpora", "wordforms-nl-celex.csv")).itertuples():
            sg, pl = row[3], row[4]
            if gd.singularize(pl) == sg:
                i +=1
            n += 1
        accuracy = float(i) / n
        desired_accuracy = 0.88
        print( "pattern.nl.pluralize() accuracy: {}".format(str(accuracy)) )
        self.assertTrue(float(i) / n > desired_accuracy, "pattern.nl.singularize() accuracy {} is below desired {}.".format(str(accuracy),desired_accuracy))

if __name__ == '__main__':
    unittest.main()