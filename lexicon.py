lexicon_names = ['poultry', 
                 'meat',
                 'seafood',
                 'breakfast',  
                 'fruit',
                 'pasta',
                 'beverage',
                 'nut',
                 'fakemeat',
                 'grain',
                 'bread',
                 'dairy',
 #                'condiment',
                 'soup',
                 'dessert',
                 'vegetable'
                ]

def lexicon_setup():
    lexicon_lists = {}
    for name in lexicon_names:
        filepath = './lexicon/' + name + '.txt'
        f = open(filepath)
        lexicon_lists.setdefault(name, {})
        for row in f:
            new_entry = row.strip().lower()
            lexicon_lists[name][new_entry] = 1
    return lexicon_lists

