# -*- coding: utf-8 -*-
# Extracted code from http://www.clips.ua.ac.be/pages/pattern
# and ported to python 3
# by Ozgur Ozturk

# Copyright (c) 2012 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).

####################################################################################################
# Regular expressions-based rules for German word inflection:
# - pluralization and singularization of nouns and adjectives,
# - conjugation of verbs,
# - attributive and predicative of adjectives,
# - comparative and superlative of adjectives.

# Accuracy (measured on CELEX German morphology word forms):
# 75% for gender()
# 72% for pluralize()
# 84% for singularize() (for nominative)

VERB, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB"

#### ARTICLE #######################################################################################
# German inflection of depends on gender, role and number + the determiner (if any).

# Inflection gender.
# Masculine is the most common, so it is the default for all functions.
MASCULINE, FEMININE, NEUTER, PLURAL = \
    MALE, FEMALE, NEUTRAL, PLURAL = \
        M, F, N, PL = "m", "f", "n", "p"

# Inflection role.
# - nom = subject, "Der Hund bellt" (the dog barks).
# - acc = object, "Das Mädchen küsst den Hund" (the girl kisses the dog).
# - dat = object (indirect), "Der Mann gibt einen Knochen zum Hund" (the man gives the dog a bone).
# - gen = property, "die Knochen des Hundes" (the dog's bone).
NOMINATIVE, ACCUSATIVE, DATIVE, GENITIVE = SUBJECT, OBJECT, INDIRECT, PROPERTY = \
    "nominative", "accusative", "dative", "genitive"


#### PLURALIZE ######################################################################################

plural_inflections = [
    ("aal", u"äle"   ), ("aat",  "aaten"), ( "abe",  "aben" ), ("ach", u"ächer"), ("ade",  "aden"  ),
    ("age",  "agen"  ), ("ahn",  "ahnen"), ( "ahr",  "ahre" ), ("akt",  "akte" ), ("ale",  "alen"  ),
    ("ame",  "amen"  ), ("amt", u"ämter"), ( "ane",  "anen" ), ("ang", u"änge" ), ("ank", u"änke"  ),
    ("ann", u"änner" ), ("ant",  "anten"), ( "aph",  "aphen"), ("are",  "aren" ), ("arn",  "arne"  ),
    ("ase",  "asen"  ), ("ate",  "aten" ), ( "att", u"ätter"), ("atz", u"ätze" ), ("aum",  "äume"  ),
    ("aus", u"äuser" ), ("bad", u"bäder"), ( "bel",  "bel"  ), ("ben",  "ben"  ), ("ber",  "ber"   ),
    ("bot",  "bote"  ), ("che",  "chen" ), ( "chs",  "chse" ), ("cke",  "cken" ), ("del",  "del"   ),
    ("den",  "den"   ), ("der",  "der"  ), ( "ebe",  "ebe"  ), ("ede",  "eden" ), ("ehl",  "ehle"  ),
    ("ehr",  "ehr"   ), ("eil",  "eile" ), ( "eim",  "eime" ), ("eis",  "eise" ), ("eit",  "eit"   ),
    ("ekt",  "ekte"  ), ("eld",  "elder"), ( "ell",  "elle" ), ("ene",  "enen" ), ("enz",  "enzen" ),
    ("erd",  "erde"  ), ("ere",  "eren" ), ( "erk",  "erke" ), ("ern",  "erne" ), ("ert",  "erte"  ),
    ("ese",  "esen"  ), ("ess",  "esse" ), ( "est",  "este" ), ("etz",  "etze" ), ("eug",  "euge"  ),
    ("eur",  "eure"  ), ("fel",  "fel"  ), ( "fen",  "fen"  ), ("fer",  "fer"  ), ("ffe",  "ffen"  ),
    ("gel",  "gel"   ), ("gen",  "gen"  ), ( "ger",  "ger"  ), ("gie",  "gie"  ), ("hen",  "hen"   ),
    ("her",  "her"   ), ("hie",  "hien" ), ( "hle",  "hlen" ), ("hme",  "hmen" ), ("hne",  "hnen"  ),
    ("hof", u"höfe"  ), ("hre",  "hren" ), ( "hrt",  "hrten"), ("hse",  "hsen" ), ("hte",  "hten"  ),
    ("ich",  "iche"  ), ("ick",  "icke" ), ( "ide",  "iden" ), ("ieb",  "iebe" ), ("ief",  "iefe"  ),
    ("ieg",  "iege"  ), ("iel",  "iele" ), ( "ien",  "ium"  ), ("iet",  "iete" ), ("ife",  "ifen"  ),
    ("iff",  "iffe"  ), ("ift",  "iften"), ( "ige",  "igen" ), ("ika",  "ikum" ), ("ild",  "ilder" ),
    ("ilm",  "ilme"  ), ("ine",  "inen" ), ( "ing",  "inge" ), ("ion",  "ionen"), ("ise",  "isen"  ),
    ("iss",  "isse"  ), ("ist",  "isten"), ( "ite",  "iten" ), ("itt",  "itte" ), ("itz",  "itze"  ),
    ("ium",  "ium"   ), ("kel",  "kel"  ), ( "ken",  "ken"  ), ("ker",  "ker"  ), ("lag", u"läge"  ),
    ("lan", u"läne"  ), ("lar",  "lare" ), ( "lei",  "leien"), ("len",  "len"  ), ("ler",  "ler"   ),
    ("lge",  "lgen"  ), ("lie",  "lien" ), ( "lle",  "llen" ), ("mel",  "mel"  ), ("mer",  "mer"   ),
    ("mme",  "mmen"  ), ("mpe",  "mpen" ), ( "mpf",  "mpfe" ), ("mus",  "mus"  ), ("mut",  "mut"   ),
    ("nat",  "nate"  ), ("nde",  "nden" ), ( "nen",  "nen"  ), ("ner",  "ner"  ), ("nge",  "ngen"  ),
    ("nie",  "nien"  ), ("nis",  "nisse"), ( "nke",  "nken" ), ("nkt",  "nkte" ), ("nne",  "nnen"  ),
    ("nst",  "nste"  ), ("nte",  "nten" ), ( "nze",  "nzen" ), ("ock", u"öcke" ), ("ode",  "oden"  ),
    ("off",  "offe"  ), ("oge",  "ogen" ), ( "ohn", u"öhne" ), ("ohr",  "ohre" ), ("olz", u"ölzer" ),
    ("one",  "onen"  ), ("oot",  "oote" ), ( "opf", u"öpfe" ), ("ord",  "orde" ), ("orm",  "ormen" ),
    ("orn", u"örner" ), ("ose",  "osen" ), ( "ote",  "oten" ), ("pel",  "pel"  ), ("pen",  "pen"   ),
    ("per",  "per"   ), ("pie",  "pien" ), ( "ppe",  "ppen" ), ("rag", u"räge" ), ("rau", u"raün"  ),
    ("rbe",  "rben"  ), ("rde",  "rden" ), ( "rei",  "reien"), ("rer",  "rer"  ), ("rie",  "rien"  ),
    ("rin",  "rinnen"), ("rke",  "rken" ), ( "rot",  "rote" ), ("rre",  "rren" ), ("rte",  "rten"  ),
    ("ruf",  "rufe"  ), ("rzt",  "rzte" ), ( "sel",  "sel"  ), ("sen",  "sen"  ), ("ser",  "ser"   ),
    ("sie",  "sien"  ), ("sik",  "sik"  ), ( "sse",  "ssen" ), ("ste",  "sten" ), ("tag",  "tage"  ),
    ("tel",  "tel"   ), ("ten",  "ten"  ), ( "ter",  "ter"  ), ("tie",  "tien" ), ("tin",  "tinnen"),
    ("tiv",  "tive"  ), ("tor",  "toren"), ( "tte",  "tten" ), ("tum",  "tum"  ), ("tur",  "turen" ),
    ("tze",  "tzen"  ), ("ube",  "uben" ), ( "ude",  "uden" ), ("ufe",  "ufen" ), ("uge",  "ugen"  ),
    ("uhr",  "uhren" ), ("ule",  "ulen" ), ( "ume",  "umen" ), ("ung",  "ungen"), ("use",  "usen"  ),
    ("uss", u"üsse"  ), ("ute",  "uten" ), ( "utz",  "utz"  ), ("ver",  "ver"  ), ("weg",  "wege"  ),
    ("zer",  "zer"   ), ("zug", u"züge" ), (u"ück", u"ücke" )
]

def pluralize(word, pos=NOUN, gender=MALE, role=SUBJECT, custom={}):
    """ Returns the plural of a given word.
        The inflection is based on probability rather than gender and role.
    """
    w = word.lower()
    if word in custom:
        return custom[word]
    if pos == NOUN:
        for a, b in plural_inflections:
            if w.endswith(a):
                return w[:-len(a)] + b
        # Default rules (baseline = 69%).
        if w.startswith("ge"):
            return w
        if w.endswith("gie"):
            return w
        if w.endswith("e"):
            return w + "n"
        if w.endswith("ien"):
            return w[:-2] + "um"
        if w.endswith(("au", "ein", "eit", "er", "en", "el", "chen", "mus", u"tät", "tik", "tum", "u")):
            return w
        if w.endswith(("ant", "ei", "enz", "ion", "ist", "or", "schaft", "tur", "ung")):
            return w + "en"
        if w.endswith("in"):
            return w + "nen"
        if w.endswith("nis"):
            return w + "se"
        if w.endswith(("eld", "ild", "ind")):
            return w + "er"
        if w.endswith("o"):
            return w + "s"
        if w.endswith("a"):
            return w[:-1] + "en"
        # Inflect common umlaut vowels: Kopf => Köpfe.
        if w.endswith(("all", "and", "ang", "ank", "atz", "auf", "ock", "opf", "uch", "uss")):
            umlaut = w[-3]
            umlaut = umlaut.replace("a", u"ä")
            umlaut = umlaut.replace("o", u"ö")
            umlaut = umlaut.replace("u", u"ü")
            return w[:-3] + umlaut + w[-2:] + "e"
        for a, b in (
          ("ag",  u"äge"),
          ("ann", u"änner"),
          ("aum", u"äume"),
          ("aus", u"äuser"),
          ("zug", u"züge")):
            if w.endswith(a):
                return w[:-len(a)] + b
        return w + "e"
    return w

#### SINGULARIZE ###################################################################################

singular_inflections = [
    ( "innen", "in" ), (u"täten", u"tät"), ( "ahnen",  "ahn"), ( "enten", "ent"), (u"räser",  "ras"),
    ( "hrten", "hrt"), (u"ücher",  "uch"), (u"örner",  "orn"), (u"änder", "and"), (u"ürmer",  "urm"),
    ( "ahlen", "ahl"), ( "uhren",  "uhr"), (u"ätter",  "att"), ( "suren", "sur"), ( "chten",  "cht"),
    ( "kuren", "kur"), ( "erzen",  "erz"), (u"güter",  "gut"), ( "soren", "sor"), (u"änner",  "ann"),
    (u"äuser", "aus"), ( "taten",  "tat"), ( "isten",  "ist"), (u"bäder", "bad"), (u"ämter",  "amt"),
    ( "eiten", "eit"), ( "raten",  "rat"), ( "ormen",  "orm"), ( "ionen", "ion"), ( "nisse",  "nis"),
    (u"ölzer", "olz"), ( "ungen",  "ung"), (u"läser",  "las"), (u"ächer", "ach"), ( "urten",  "urt"),
    ( "enzen", "enz"), ( "aaten",  "aat"), ( "aphen",  "aph"), (u"öcher", "och"), (u"türen", u"tür"),
    ( "sonen", "son"), (u"ühren", u"ühr"), (u"ühner",  "uhn"), ( "toren", "tor"), (u"örter",  "ort"),
    ( "anten", "ant"), (u"räder",  "rad"), ( "turen",  "tur"), (u"äuler", "aul"), ( u"änze",  "anz"),
    (  "tten", "tte"), (  "mben",  "mbe"), ( u"ädte",  "adt"), (  "llen", "lle"), (  "ysen",  "yse"),
    (  "rben", "rbe"), (  "hsen",  "hse"), ( u"raün",  "rau"), (  "rven", "rve"), (  "rken",  "rke"),
    ( u"ünge", "ung"), ( u"üten", u"üte"), (  "usen",  "use"), (  "tien", "tie"), ( u"läne",  "lan"),
    (  "iben", "ibe"), (  "ifen",  "ife"), (  "ssen",  "sse"), (  "gien", "gie"), (  "eten",  "ete"),
    (  "rden", "rde"), ( u"öhne",  "ohn"), ( u"ärte",  "art"), (  "ncen", "nce"), ( u"ünde",  "und"),
    (  "uben", "ube"), (  "lben",  "lbe"), ( u"üsse",  "uss"), (  "agen", "age"), ( u"räge",  "rag"),
    (  "ogen", "oge"), (  "anen",  "ane"), (  "sken",  "ske"), (  "eden", "ede"), ( u"össe",  "oss"),
    ( u"ürme", "urm"), (  "ggen",  "gge"), ( u"üren", u"üre"), (  "nten", "nte"), ( u"ühle", u"ühl"),
    ( u"änge", "ang"), (  "mmen",  "mme"), (  "igen",  "ige"), (  "nken", "nke"), ( u"äcke",  "ack"),
    (  "oden", "ode"), (  "oben",  "obe"), ( u"ähne",  "ahn"), ( u"änke", "ank"), (  "inen",  "ine"),
    (  "seen", "see"), ( u"äfte",  "aft"), (  "ulen",  "ule"), ( u"äste", "ast"), (  "hren",  "hre"),
    ( u"öcke", "ock"), (  "aben",  "abe"), ( u"öpfe",  "opf"), (  "ugen", "uge"), (  "lien",  "lie"),
    ( u"ände", "and"), ( u"ücke", u"ück"), (  "asen",  "ase"), (  "aden", "ade"), (  "dien",  "die"),
    (  "aren", "are"), (  "tzen",  "tze"), ( u"züge",  "zug"), ( u"üfte", "uft"), (  "hien",  "hie"),
    (  "nden", "nde"), ( u"älle",  "all"), (  "hmen",  "hme"), (  "ffen", "ffe"), (  "rmen",  "rma"),
    (  "olen", "ole"), (  "sten",  "ste"), (  "amen",  "ame"), ( u"höfe", "hof"), ( u"üste",  "ust"),
    (  "hnen", "hne"), ( u"ähte",  "aht"), (  "umen",  "ume"), (  "nnen", "nne"), (  "alen",  "ale"),
    (  "mpen", "mpe"), (  "mien",  "mie"), (  "rten",  "rte"), (  "rien", "rie"), ( u"äute",  "aut"),
    (  "uden", "ude"), (  "lgen",  "lge"), (  "ngen",  "nge"), (  "iden", "ide"), ( u"ässe",  "ass"),
    (  "osen", "ose"), (  "lken",  "lke"), (  "eren",  "ere"), ( u"üche", "uch"), ( u"lüge",  "lug"),
    (  "hlen", "hle"), (  "isen",  "ise"), ( u"ären", u"äre"), ( u"töne", "ton"), (  "onen",  "one"),
    (  "rnen", "rne"), ( u"üsen", u"üse"), ( u"haün",  "hau"), (  "pien", "pie"), (  "ihen",  "ihe"),
    ( u"ürfe", "urf"), (  "esen",  "ese"), ( u"ätze",  "atz"), (  "sien", "sie"), ( u"läge",  "lag"),
    (  "iven", "ive"), ( u"ämme",  "amm"), ( u"äufe",  "auf"), (  "ppen", "ppe"), (  "enen",  "ene"),
    (  "lfen", "lfe"), ( u"äume",  "aum"), (  "nien",  "nie"), (  "unen", "une"), (  "cken",  "cke"),
    (  "oten", "ote"), (   "mie",  "mie"), (   "rie",  "rie"), (   "sis", "sen"), (   "rin",  "rin"),
    (   "ein", "ein"), (   "age",  "age"), (   "ern",  "ern"), (   "ber", "ber"), (   "ion",  "ion"),
    (   "inn", "inn"), (   "ben",  "ben"), (  u"äse", u"äse"), (   "eis", "eis"), (   "hme",  "hme"),
    (   "iss", "iss"), (   "hen",  "hen"), (   "fer",  "fer"), (   "gie", "gie"), (   "fen",  "fen"),
    (   "her", "her"), (   "ker",  "ker"), (   "nie",  "nie"), (   "mer", "mer"), (   "ler",  "ler"),
    (   "men", "men"), (   "ass",  "ass"), (   "ner",  "ner"), (   "per", "per"), (   "rer",  "rer"),
    (   "mus", "mus"), (   "abe",  "abe"), (   "ter",  "ter"), (   "ser", "ser"), (  u"äle",  "aal"),
    (   "hie", "hie"), (   "ger",  "ger"), (   "tus",  "tus"), (   "gen", "gen"), (   "ier",  "ier"),
    (   "ver", "ver"), (   "zer",  "zer"),
]

singular = {
    u"Löwen": u"Löwe",
}

def singularize(word, pos=NOUN, gender=MALE, role=SUBJECT, custom={}):
    """ Returns the singular of a given word.
        The inflection is based on probability rather than gender and role.
    """
    w = word.lower()
    if word in custom:
        return custom[word]
    if word in singular:
        return singular[word]
    if pos == NOUN:
        for a, b in singular_inflections:
            if w.endswith(a):
                return w[:-len(a)] + b
        # Default rule: strip known plural suffixes (baseline = 51%).
        for suffix in ("nen", "en", "n", "e", "er", "s"):
            if w.endswith(suffix):
                w = w[:-len(suffix)]
                break
        # Corrections (these add about 1% accuracy):
        if w.endswith(("rr", "rv", "nz")):
            return w + "e"
        return w
    return w
