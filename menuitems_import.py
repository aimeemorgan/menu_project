import csv


def build_menuid_dict():
# map menu_page_ids to menu_ids
    with open('./ref_docs/MenuPage.csv') as csvfile:
        menu_ids = {}
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:
            menu_ids[row[0]] = row[1]
    return menu_ids


def build_new_lines(menu_ids):
# read old file, replace menu_page_ids with menu_ids, write
# lines to list
    with open('./ref_docs/MenuItem_old.csv') as old_csvfile:
        itemreader = csv.reader(old_csvfile, delimiter=",")
        newlines = []
        for row in itemreader:
            row[1] = menu_ids[row[1]]
            newline = [row[0], row[1], row[2], row[4]]
            newlines.append(newline)
    return newlines

def write_csv(newlines):
# read lines from list, write to new csv file
    with open('menuitems.csv', 'wb') as new_csvfile:
        writer = csv.writer(new_csvfile, delimiter=',')
        writer.writerows(newlines)


if __name__ == "__main__":
    menu_ids = build_menuid_dict()
    newlines = build_new_lines(menu_ids)
    write_csv(newlines)
