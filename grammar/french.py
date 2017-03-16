# -*- coding: utf-8 -*-
# Extracted code from http://www.clips.ua.ac.be/pages/pattern
# and ported to python 3
# by Ozgur Ozturk

# Copyright (c) 2013 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).

####################################################################################################
# Regular expressions-based rules for French word inflection:
# - pluralization and singularization of nouns
# Accuracy:
# 92% for pluralize()
# 93% for singularize()

import re

VERB, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB"

VOWELS = ("a", "e", "i", "o", "u")
re_vowel = re.compile(r"a|e|i|o|u", re.I)
is_vowel = lambda ch: ch in VOWELS

#### PLURALIZE #####################################################################################

plural_irregular = {
       "bleu": "bleus",
       "pneu": "pneus",
    "travail": "travaux",
    "vitrail": "vitraux"
}

def pluralize(word, pos=NOUN, custom={}):
    """ Returns the plural of a given word.
        The custom dictionary is for user-defined replacements.
    """
    if word in custom:
        return custom[word]
    w = word.lower()
    if w in plural_irregular:
        return plural_irregular[w]
    if w.endswith(("ais", "ois")):
        return w + "es"
    if w.endswith(("s", "x")):
        return w
    if w.endswith("al"):
        return w[:-2] + "aux"
    if w.endswith(("au", "eu")):
        return w + "x"
    return w + "s"

#### SINGULARIZE ###################################################################################

def singularize(word, pos=NOUN, custom={}):
    if word in custom:
        return custom[word]
    w = word.lower()
    # Common articles, determiners, pronouns:
    if pos in ("DT", "PRP", "PRP$", "WP", "RB", "IN"):
        if w == "du" : return "de"
        if w == "ces": return "ce"
        if w == "les": return "le"
        if w == "des": return "un"
        if w == "mes": return "mon"
        if w == "ses": return "son"
        if w == "tes": return "ton"
        if w == "nos": return "notre"
        if w == "vos": return "votre"
        if w.endswith(("'", u"’")):
            return w[:-1] + "e"
    if w.endswith("nnes"):  # parisiennes => parisien
        return w[:-3]
    if w.endswith("ntes"):  # passantes => passant
        return w[:-2]
    if w.endswith("euses"): # danseuses => danseur
        return w[:-3] + "r"
    if w.endswith("s"):
        return w[:-1]
    if w.endswith(("aux", "eux", "oux")):
        return w[:-1]
    if w.endswith("ii"):
        return w[:-1] + "o"
    if w.endswith(("ia", "ma")):
        return w[:-1] + "um"
    if "-" in w:
        return singularize(w.split("-")[0]) + "-" + "-".join(w.split("-")[1:])
    return w
