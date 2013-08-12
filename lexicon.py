lexicon_names = ['POULTRY', 
                 'MEAT',
                 'SEAFOOD',
                 'BREAKFAST',  
                 'FRUITS',
                 'PASTA',
                 'BEVERAGES',
                 'NUTS',
                 'FAKEMEAT',
                 'GRAINS',
                 'BREAD',
                 'DAIRY',
                 'FLAVORS',
                 'SOUPS',
                 'DESSERT'
                ]

def lexicon_setup():
    lexicon = {}
    for name in lexicon_names:
        filepath = './lexicon/' + str(name).lower() + '.txt'
        f = open(filepath)
        lexicon.setdefault(name, [])
        for row in f:
            lexicon[name].append(row.strip().lower())
    return lexicon


