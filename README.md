# Singularize_Pluralize Repository 
Contains a Python module called grammar.
It is a Python 3 port of German, Dutch, and French singularization and pluralization extracted from CLIPS's Pattern NLP Library in Python 2.

# Usage:
```
import grammar.dutch as gd

gd.singularize("fietsen") #returns "fiets"
gd.pluralize(("fiets") #returns "fietsen"
```

# Accuracy Levels on Corpora
## Dutch Accuracy (measured on CELEX Dutch morphology word forms):
79% for pluralize()
91% for singularize()

## Accuracy (measured on CELEX German morphology word forms):
75% for gender()
72% for pluralize()
84% for singularize() (for nominative)

## French Accuracy:
92% for pluralize()
93% for singularize()
