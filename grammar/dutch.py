# -*- coding: utf-8 -*-
# Extracted code from http://www.clips.ua.ac.be/pages/pattern
# and ported to python 3
# by Ozgur Ozturk

# Copyright (c) 2010 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).

####################################################################################################
# Regular expressions-based rules for Dutch word inflection:
# - pluralization and singularization of nouns,
# - conjugation of verbs,
# - predicative and attributive of adjectives.

# Accuracy (measured on CELEX Dutch morphology word forms):
# 79% for pluralize()
# 91% for singularize()
import re
VERB, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB"

VOWELS = ("a", "e", "i", "o", "u")
re_vowel = re.compile(r"a|e|i|o|u|y", re.I)
is_vowel = lambda ch: ch in VOWELS

#### PLURALIZE ######################################################################################

plural_irregular_en = set(("dag", "dak", "dal", "pad", "vat", "weg"))
plural_irregular_een = set(("fee", "genie", "idee", "orgie", "ree"))
plural_irregular_eren = set(("blad", "ei", "gelid", "gemoed", "kalf", "kind", "lied", "rad", "rund"))
plural_irregular_deren = set(("hoen", "been"))

plural_irregular = {
     "centrum": "centra",
    "escargot": "escargots",
      "gedrag": "gedragingen",
       "gelid": "gelederen",
       "kaars": "kaarsen",
       "kleed": "kleren",
         "koe": "koeien",
         "lam": "lammeren",
      "museum": "museums",
        "stad": "steden",
       "stoel": "stoelen",
         "vlo": "vlooien"
}

def pluralize(word, pos=NOUN, custom={}):
    """ Returns the plural of a given word.
        For example: stad => steden.
        The custom dictionary is for user-defined replacements.
    """
    if word in list(custom.keys()):
        return custom[word]
    w = word.lower()
    if pos == NOUN:
        if w in plural_irregular_en:    # dag => dagen
            return w + "en"
        if w in plural_irregular_een:   # fee => feeën
            return w + "ën"
        if w in plural_irregular_eren:  # blad => bladeren
            return w + "eren"
        if w in plural_irregular_deren: # been => beenderen
            return w + "deren"
        if w in plural_irregular:
            return plural_irregular[w]
        # Words ending in -icus get -ici: academicus => academici
        if w.endswith("icus"):
            return w[:-2] + "i"
        # Words ending in -s usually get -sen: les => lessen.
        if w.endswith(("es", "as", "nis", "ris", "vis")):
            return w + "sen"
        # Words ending in -s usually get -zen: huis => huizen.
        if w.endswith("s") and not w.endswith(("us", "ts", "mens")):
            return w[:-1] + "zen"
        # Words ending in -f usually get -ven: brief => brieven.
        if w.endswith("f"):
            return w[:-1] + "ven"
        # Words ending in -um get -ums: museum => museums.
        if w.endswith("um"):
            return w + "s"
        # Words ending in unstressed -ee or -ie get -ën: bacterie => bacteriën
        if w.endswith("ie"):
            return w + "s"
        if w.endswith(("ee","ie")):
            return w[:-1] + "ën"
        # Words ending in -heid get -heden: mogelijkheid => mogelijkheden
        if w.endswith("heid"):
            return w[:-4] + "heden"
        # Words ending in -e -el -em -en -er -ie get -s: broer => broers.
        if w.endswith(("é", "e", "el", "em", "en", "er", "eu", "ie", "ue", "ui", "eau", "ah")):
            return w + "s"
        # Words ending in a vowel get 's: auto => auto's.
        if w.endswith(VOWELS) or w.endswith("y") and not w.endswith("e"):
            return w + "'s"
        # Words ending in -or always get -en: motor => motoren.
        if w.endswith("or"):
            return w + "en"
        # Words ending in -ij get -en: boerderij => boerderijen.
        if w.endswith("ij"):
            return w + "en"
        # Words ending in two consonants get -en: hand => handen.
        if len(w) > 1 and not is_vowel(w[-1]) and not is_vowel(w[-2]):
            return w + "en"
        # Words ending in one consonant with a short sound: fles => flessen.
        if len(w) > 2 and not is_vowel(w[-1]) and not is_vowel(w[-3]):
            return w + w[-1] + "en"
        # Words ending in one consonant with a long sound: raam => ramen.
        if len(w) > 2 and not is_vowel(w[-1]) and w[-2] == w[-3]:
            return w[:-2] + w[-1] + "en"
        return w + "en"
    return w

#### SINGULARIZE ###################################################################################

singular_irregular = dict((v,k) for k,v in plural_irregular.items())

def singularize(word, pos=NOUN, custom={}):
    if word in list(custom.keys()):
        return custom[word]
    w = word.lower()
    if pos == NOUN and w in singular_irregular:
        return singular_irregular[w]
    if pos == NOUN and w.endswith(("ën", "en", "s", "i")):
        # auto's => auto
        if w.endswith("'s"):
            return w[:-2]
        # broers => broer
        if w.endswith("s"):
            return w[:-1]
        # academici => academicus
        if w.endswith("ici"):
            return w[:-1] + "us"
        # feeën => fee
        if w.endswith("ën") and w[:-2] in plural_irregular_een:
            return w[:-2]
        # bacteriën => bacterie
        if w.endswith("ën"):
            return w[:-2] + "e"
        # mogelijkheden => mogelijkheid
        if w.endswith("heden"):
            return w[:-5] + "heid"
        # artikelen => artikel
        if w.endswith("elen") and not w.endswith("delen"):
            return w[:-2]
        # chinezen => chinees
        if w.endswith("ezen"):
            return w[:-4] + "ees"
        # neven => neef
        if w.endswith("even") and len(w) > 4 and not is_vowel(w[-5]):
            return w[:-4] + "eef"
        if w.endswith("en"):
            w = w[:-2]
            # ogen => oog
            if w in ("og","om","ur"):
                return w[:-1] + w[-2] + w[-1]
            # hoenderen => hoen
            if w.endswith("der") and w[:-3] in plural_irregular_deren:
                return w[:-3]
            # eieren => ei
            if w.endswith("er") and w[:-2] in plural_irregular_eren:
                return w[:-2]
            # dagen => dag (not daag)
            if w in plural_irregular_en:
                return w
            # huizen => huis
            if w.endswith("z"):
                return w[:-1] + "s"
            # brieven => brief
            if w.endswith("v"):
                return w[:-1] + "f"
             # motoren => motor
            if w.endswith("or"):
                return w
            # flessen => fles
            if len(w) > 1 and not is_vowel(w[-1]) and w[-1] == w[-2]:
                return w[:-1]
            # baarden => baard
            if len(w) > 1 and not is_vowel(w[-1]) and not is_vowel(w[-2]):
                return w
            # boerderijen => boerderij
            if w.endswith("ij"):
                return w
            # idealen => ideaal
            if w.endswith(("eal", "ean", "eol", "ial", "ian", "iat", "iol")):
                return w[:-1] + w[-2] + w[-1]
            # ramen => raam
            if len(w) > 2 and not is_vowel(w[-1]) and is_vowel(w[-2]) and not is_vowel(w[-3]):
                return w[:-1] + w[-2] + w[-1]
            return w
    return w