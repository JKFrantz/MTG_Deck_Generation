import csv
import glob
import os
import numpy
from collections import defaultdict

class Card:
    def __init__(self, val_list):
        # val_list must be a list of card attributes with the right
        # number of values
        assert len(val_list) == 10, "List has the wrong number of values."
# there could easily be more card attributes than this, such as a card's
# entire rules text, but these are the ones I chose to work with.


        self.types = val_list[1]
        self.colors = val_list[2]
        self.practical_cmc = val_list[3]
        self.cmc = val_list[4]
        self.practical_mana_pips = val_list[5]
        self.mana_pips = val_list[6]
        self.mana_source = val_list[7]
        self.properties = val_list[8]
        self.oracle_id = val_list[9]
                                    # MTGO decklists only include the first
                                    # of a split card's names, but the
                                    # Scryfall database has both, so we split
                                    # out the first card from the two.
        if ("Creature" in self.types) or ("Land" in self.types):
            self.name = val_list[0].split(" //")[0]
        else:
            self.name = val_list[0]

# return methods for all variables
    def get_name(self):
        return self.name
    def get_types(self):
        return self.types
    def get_colors(self):
        return self.colors
    def get_practical_cmc(self):
        return self.practical_cmc
    def get_cmc(self):
        return self.cmc
    def get_mana_pips(self):
        return self.mana_pips
    def get_practical_mana_pips(self):
        return self.practical_mana_pips
    def get_properties(self):
        return self.properties
    def get_mana_source(self):
        return self.mana_source
    def get_oracle_id(self):
        return self.oracle_id

class Deck:
    def __init__(self):
        self.color_pips = defaultdict(int)
        self.mb = []
        self.sb = []
        self.seventyfive = []
        self.curve = defaultdict(int)
        self.mb_size = 0
        self.sb_size = 0

    # return methods for all variables
    def get_color_pips(self):
        return self.color_pips
    def get_mb(self):
        return self.mb
    def get_sb(self):
        return self.sb
    def get_seventyfive(self):
        return self.seventyfive
    def get_curve(self):
        return self.curve
    def get_mb_size(self):
        return self.mb_size
    def get_sb_size(self):
        return self.sb_size

        # gives a representation of the deck with card-type counts.
        # probably could be made much more efficient
    def save_to_file(self, MTGO_Deck_Num, Formatted_Deck_Num):
        words = ["Creatures", "Planeswalkers", "Spells", "Artifacts", "Enchantments", "Lands"]
        word_map = {
            "Creatures": ["Creature"],
            "Planeswalkers": ["Planeswalker"],
            "Spells": ["Instant", "Sorcery"],
            "Artifacts": ["Artifact"],
            "Enchantments": ["Enchantment"],
            "Lands": ["Land"]
        }
        card_map = {
            "Creatures": [],
            "Planeswalkers": [],
            "Spells": [],
            "Artifacts": [],
            "Enchantments": [],
            "Lands": []
        }
        m = self.get_mb()
        out_cardnames = []
        for val in words:
            for val2 in m:
                for val3 in word_map[val]:
                    if (val3 in val2.get_types()) and (val2.get_name() not in out_cardnames):
                        card_map[val].append(val2)
            for val4 in card_map[val]:
                if val4.get_name() not in out_cardnames:
                    out_cardnames.append(val4.get_name())

        print_map = {
            "Creatures": defaultdict(int),
            "Planeswalkers": defaultdict(int),
            "Spells": defaultdict(int),
            "Artifacts": defaultdict(int),
            "Enchantments": defaultdict(int),
            "Lands": defaultdict(int)
        }
        for val in words:
            for val2 in card_map[val]:
                print_map[val][val2.get_name()] += 1
        m = open(f"MTGO_Decklists/MTGO_Deck{MTGO_Deck_Num}.txt", "w")
        f = open(f"Formatted_Decklists/Formatted_Deck{Formatted_Deck_Num}.txt", "w")
        for val in print_map.keys():
            if not print_map[val] == {}:
                f.write(f"{val} ({sum(print_map[val].values())}):\n")
                for val2 in print_map[val].keys():
                    m.write(f"{print_map[val][val2]} {val2}\n")
                    f.write(f"{print_map[val][val2]} {val2}\n")
                f.write("\n")
        m.write("\n")
        f.write("\n")
        sb_print_map = {}
        for val in self.sb:
            if val.get_name() in sb_print_map.keys():
                sb_print_map[val.get_name()] += 1
            else:
                sb_print_map[val.get_name()] = 1
        f.write("Sideboard (15):\n")
        for val in sb_print_map.keys():
            m.write(f"{sb_print_map[val]} {val}\n")
            f.write(f"{sb_print_map[val]} {val}\n")
        f.close()

    def display(self):
        words = ["Creatures", "Planeswalkers", "Spells", "Artifacts", "Enchantments", "Lands"]
        word_map = {
            "Creatures": ["Creature"],
            "Planeswalkers": ["Planeswalker"],
            "Spells": ["Instant", "Sorcery"],
            "Artifacts": ["Artifact"],
            "Enchantments": ["Enchantment"],
            "Lands": ["Land"]
        }
        card_map = {
            "Creatures": [],
            "Planeswalkers": [],
            "Spells": [],
            "Artifacts": [],
            "Enchantments": [],
            "Lands": []
        }
        m = self.get_mb()
        out_cardnames = []
        for val in words:
            for val2 in m:
                for val3 in word_map[val]:
                    if (val3 in val2.get_types()) and (val2.get_name() not in out_cardnames):
                        card_map[val].append(val2)
            for val4 in card_map[val]:
                if val4.get_name() not in out_cardnames:
                    out_cardnames.append(val4.get_name())

        print_map = {
            "Creatures": defaultdict(int),
            "Planeswalkers": defaultdict(int),
            "Spells": defaultdict(int),
            "Artifacts": defaultdict(int),
            "Enchantments": defaultdict(int),
            "Lands": defaultdict(int)
        }
        for val in words:
            for val2 in card_map[val]:
                if val2.get_name() in print_map[val].keys():
                    print_map[val][val2.get_name()] += 1
                else:
                    print_map[val][val2.get_name()] = 1
        for val in print_map.keys():
            if not print_map[val] == {}:
                print(f"     {val} ({sum(print_map[val].values())}):")
            for val2 in print_map[val].keys():
                print(f"{print_map[val][val2]} {val2}")
        sb_print_map = {}
        for val in self.sb:
            if val.get_name() in sb_print_map.keys():
                sb_print_map[val.get_name()] += 1
            else:
                sb_print_map[val.get_name()] = 1
        print("     Sideboard (15):")
        for val in sb_print_map.keys():
            print(sb_print_map[val], val)
        print("")



    def mb_add(self, newcard):
        assert isinstance(newcard, Card), "object passed to method isn't a Card"
        self.mb.append(newcard)
        self.seventyfive.append(newcard)
        self.mb_size += 1

        if 'Land' not in newcard.get_types():
            self.curve[newcard.get_practical_cmc()] = 1
        for val in newcard.get_practical_mana_pips():
            self.color_pips[val] += 1

    def sb_add(self, newcard):
        assert isinstance(newcard, Card), "object passed to method isn't a Card"
        self.sb.append(newcard)
        self.seventyfive.append(newcard)
        self.sb_size += 1

    def sb_add_by_name(self, name, master_list, number = 1):
        n = name_retrieve(name, master_list)
        for val in range(0, number):
            self.sb_add(n)

    def mb_add_by_name(self, name, master_list, number = 1):
        n = name_retrieve(name, master_list)
        for val in range(0, number):
            self.mb_add(n)



class Synergy_Group:
    def __init__(self, l):
        self.name = l[0]
        self.colors = l[1]
        self.cards = l[2]
        self.mb_multipliers = l[3]
        self.sb_multipliers = l[4]

    def get_name(self):
        return self.name
    def get_colors(self):
        return self.colors
    def get_cards(self):
        return self.cards
    def get_mb_multipliers(self):
        return self.mb_multipliers
    def get_sb_multipliers(self):
        return self.sb_multipliers
    def get_all(self):
        return([self.name, self.colors, self.cards, self.mb_multipliers,
        self.sb_multipliers])


    def apply(self, colors, deck, mb_spinner, sb_spinner, master_list):
        for val in self.get_cards():
            a = int(val[1] // 1)
            in_color = True
            for val2 in name_retrieve(val[0], master_list).get_colors():
                if val2 not in colors:
                    in_color = False
            if in_color:
                for val2 in range(0, a):
                    deck.mb_add(name_retrieve(val[0], master_list))
                m = a = val[1] % 1
                if m > 0:
                    add = numpy.random.choice([True, False], p = [m, 1-m])
                    if add:
                        deck.mb_add(name_retrieve(val[0], master_list))
        for val in self.get_mb_multipliers():
            mb_spinner.multiply(val[0], val[1])
        for val in self.get_sb_multipliers():
            sb_spinner.multiply(val[0], val[1])

class Spinner:
    def __init__(self, dictionary):
        self.spinner = dictionary

    def spin(self):
        keys = []
        values = []
        for val in self.spinner.keys():
            keys.append(val)
            values.append(self.spinner[val])
        new_card = numpy.random.choice(keys, p = values)
        return (new_card)

    def multiply(self, card_name, multiplier):
        self.spinner[card_name] *= multiplier
        self.balance()

    def color_prune(self, color_list, master_list):
        vals_for_deletion = []
        for val in self.spinner:
            for val2 in name_retrieve(val, master_list).get_colors():
                if val2 not in color_list:
                    if val not in vals_for_deletion:
                        vals_for_deletion.append(val)
        for val in vals_for_deletion:
            del self.spinner[val]
        self.balance()
    def balance(self):
        s = sum(self.spinner.values())
        if s != 1:
            r = 1 / s
            for val in self.spinner:
                self.spinner[val] *= r

    def get_spinner(self):
        return self.spinner

def csv_to_synergy_list(file_name):
    synergy_list = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        line_count = 0
        for row in csv_reader:
            # this is just so the header isn't included as an object
            if line_count == 0:
                line_count += 1
            else:
                for val in range(2, 5):
                    row[val] = row[val].split("|")
                    for val2 in range(len(row[val])):
                        row[val][val2] = row[val][val2].split("/")
                        if len(row[val][val2]) > 1:
                            if row[val][val2][1].isdigit():
                                row[val][val2][1] = int(row[val][val2][1])
                            else:
                                row[val][val2][1] = float(row[val][val2][1])
                    if row[val] == [['']]:
                        row[val] = []
                synergy_list.append(Synergy_Group(row))
                line_count += 1

    return synergy_list

def get_synergy_group_by_name(name, list):
    for val in list:
        if name == val.get_name():
            return val

# removes all cards that are in colors outside the specified list

def color_prune(c, l):
    sublist = []
    for val in l:
        a = True
        for val2 in val.get_colors():
            if val2 not in c:
                a = False
        if a:
            sublist.append(val)
    return sublist

# removes all lands that produce mana outside the specified colors.
def land_mana_prune(c, l):
    sublist = []
    for val in l:
        a = True
        for val2 in val.get_mana_source():
            if (val2 not in c) and ('Land' in val.get_types()):
                a = False
        if a:
            sublist.append(val)
    return sublist

# removes all cards with a certain keyword
def keyword_prune(k, l):
    sublist = []
    for val in l:
        a = True
        if k in val.get_properties():
            a = False
        if a:
            sublist.append(val)
    return sublist

# reads a csv file and returns a list of card objects
def csv_to_list(file_name):
    card_list = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        line_count = 0
        for row in csv_reader:
            # this is just so the header isn't included as an object
            if line_count == 0:
                line_count += 1
            else:
                card_list.append(Card(row))
                line_count += 1
    return card_list

# Makes a Deck object out of a normal MTGO decklist
def txt_to_deck(file_name, master_list):
    f = open(file_name, "r")
    mainboard = []
    sideboard = []
    mb = True
    for line in f:
        if line == "\n":
            mb = False
        else:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            if mb:
                mainboard.append([int(line_list[0]), ' '.join(line_list[1:])])
            else:
                sideboard.append([int(line_list[0]), ' '.join(line_list[1:])])
    the_deck = Deck()
    for val in mainboard:
        matching_card = ""
        for val2 in master_list:
            if val2.get_name() == val[1]:
                matching_card = val2
        for val3 in range(0, val[0]):
            the_deck.mb_add(matching_card)
    for val in sideboard:
        matching_card = ""
        for val2 in master_list:
            if val2.get_name() == val[1]:
                matching_card = val2
                break
        for val3 in range(0, val[0]):
            the_deck.sb_add(matching_card)
    return the_deck

# takes a directory and returns a list of Deck objects for every
# txt file in that directory
# Don't forget the final slash in the directory path!
def dir_to_decks(l, master_list):
    decks_list = []
    for filename in glob.glob(f"{l}*.txt"):
        decks_list.append(txt_to_deck(filename, master_list))
    return decks_list

def dir_to_csv(l, name, master_list):
    d = dir_to_decks(l, master_list)
    unique_card_names = []
    unique_card_list = []
    for val in d:
        for val2 in val.get_seventyfive():
            if val2.get_name() not in unique_card_names:
                unique_card_names.append(val2.get_name())
                unique_card_list.append(val2)
    csv_list = []
    for val in unique_card_list:
        csv_list.append([val.get_name(), val.get_types(), val.get_colors(),
        val.get_practical_cmc(), val.get_cmc(), val.get_practical_mana_pips(),
        val.get_mana_pips(), val.get_mana_source(), val.get_properties(),
        val.get_oracle_id()])
    file = open(name, 'w+', newline = '')
    with file:
        write = csv.writer(file)
        write.writerow(["name","type_line","colors", "practical_cmc",
        "cmc","practical_mana_pips", "mana_pips",
        "produced_mana","properties","oracle_id"])
        write.writerows(csv_list)

# gives the avg curves for the pool of decks in a directory
def dir_curve(l, master_list):
    d = dir_to_decks(l, master_list)

    master_curve = dict()
    deck_total = 0

    for val in d:
        c = val.get_curve()
        deck_total += 1
        for val2 in c.keys():
            if val2 in master_curve.keys():
                master_curve[val2] += c[val2]
            else:
                master_curve[val2] = c[val2]

    avg_curve = dict()

    for val in master_curve.keys():
        avg_curve[val] = master_curve[val] / deck_total

    for val in range(0, 15):
        strval = str(val)
        if strval in avg_curve.keys():
            print(f"CMC{strval}: {avg_curve[strval]} spells")

# reads a directory and returns a dictionary with each card's percentage
# representation in the overall pool of mainboards
def dir_mb_spinner(l, master_list):
    d = dir_to_decks(l, master_list)
    card_total = 0
    card_pool = {}
    for val in d:
        for val2 in val.get_mb():
            card_total += 1
            if val2.get_name() in card_pool.keys():
                card_pool[val2.get_name()] += 1
            else:
                card_pool[val2.get_name()] = 1
    for val in card_pool.keys():
        card_pool[val] = card_pool[val] / card_total
    s = Spinner(card_pool)
    return s

# reads a directory and returns a dictionary with each card's percentage
# representation in the overall pool of sideboards
def dir_sb_spinner(l, master_list):
    d = dir_to_decks(l, master_list)
    card_total = 0
    card_pool = {}
    for val in d:
        for val2 in val.get_sb():
            card_total += 1
            if val2.get_name() in card_pool.keys():
                card_pool[val2.get_name()] += 1
            else:
                card_pool[val2.get_name()] = 1
    for val in card_pool.keys():
        card_pool[val] = card_pool[val] / card_total
    s = Spinner(card_pool)
    return s

def decks_with_these_cards_inclusive(card_list, decks, master_list):
    yes_decks = []
    for val in decks:
        add = False
        for val2 in val.get_seventyfive():
            for val3 in card_list:
                if val3 == val2.get_name():
                    add = True
        if add:
            yes_decks.append(val)
    return yes_decks

def card_types_per_card(card_type_names, decks):
    cardtypename_totals = {}
    card_total = 0
    for val in decks:
        for val2 in val.get_mb():
            card_total += 1
            for val3 in card_type_names:
                if val3 in val2.get_types():
                    if val3 in cardtypename_totals.keys():
                        cardtypename_totals[val3] += 1
                    else:
                        cardtypename_totals[val3] = 1
    for val in cardtypename_totals:
        cardtypename_totals[val] /= card_total
    return cardtypename_totals

def keywords_per_card(keywords, decks):
    keyword_totals = {}
    card_total = 0
    for val in decks:
        for val2 in val.get_mb():
            card_total += 1
            for val3 in keywords:
                if val3 in val2.get_properties():
                    if val3 in keyword_totals.keys():
                        keyword_totals[val3] += 1
                    else:
                        keyword_totals[val3] = 1
    for val in keyword_totals:
        keyword_totals[val] /= card_total
    return keyword_totals

def cards_per_deck(card_names, decks):
    cardname_totals = {}
    deck_total = 0
    for val in decks:
        deck_total += 1
        for val2 in val.get_mb():
            for val3 in card_names:
                if val3 == val2.get_name():
                    if val3 in cardname_totals.keys():
                        cardname_totals[val3] += 1
                    else:
                        cardname_totals[val3] = 1
    for val in cardname_totals:
        cardname_totals[val] /= deck_total
    return cardname_totals

def decks_with_this_many_colors(decks, number):
    decks_to_return = []
    for val in decks:
        colors = []
        for val2 in val.get_seventyfive():
            for val3 in val2.get_colors():
                if val3 not in colors:
                    colors.append(val3)
        if len(colors) == number:
            decks_to_return.append(val)
    return decks_to_return

# functions telling you whether an oracle_id or name are in a list
# of card objects

def id_in_list_boolean(o, l):
    for val in l:
        if o == val.get_oracle_id():
            return True
    return False

def name_in_list_boolean(n, l):
    for val in l:
        if n == val.get_name():
            return True
    return False

# functions for returning the number of times an oracle_id or name
# appears in a submitted list

def id_in_list_number(o, l):
    total = 0
    for val in l:
        if o == val.get_oracle_id():
            total += 1
    return total

def name_in_list_number(n, l):
    total = 0
    for val in l:
        if n == val.get_name():
            total += 1
    return total

# these functions return card objects corresponding to
# an oracle_id or card name

def id_retrieve(i, l):
    for val in l:
        if i == val.get_oracle_id():
            return val

def name_retrieve(n, l):
    for val in l:
        if n == val.get_name():
            return val

def keyword_occurrences(keyword, deck):
    total = 0
    for val in deck:
        if keyword in val.get_properties():
            total += 1
    return total

# This asks the user if they want to see a list of available keywords.
def keyword_list_prompt():
    while True:
        val = input("Would you like to see a list of all available keywords?\n")
        if val.upper() == "yes".upper():
            f = open("Keyword_List.txt", "r")
            print(f.read())
            break
        elif val.upper() == "no".upper():
            break
        else:
            print("Sorry, you didn't type yes or no.")

# Asks the user for which keywords they'd like included in their deck,
# rating them in importance with integers from 1 to 10.
def keyword_prompt_weighted():
    print("Decide which keywords you'd like to include, and how strongly.")
    print("Note that if you don't select Small_Creature, Medium_Creature,")
    print("or Large_Creature, your deck may have few or no threats.")
    print("You have to ask for at least one keyword.")
    keyword_list_prompt()
    keywords = {}
    while True:
        new_keyword = input("Go ahead and type a keyword.\n")
        if new_keyword in keywords.keys():
            print("You chose that keyword already.")
        else:
            new_keyword_value = input("Rate how important this is on a scale of 1 to 10\n")
            while True:
                try:
                    new_keyword_value = int(new_keyword_value)
                    keywords[new_keyword] = new_keyword_value
                    break
                except ValueError:
                    print("You didn't input an integer between 1 and 10.")
                    print(f"How important is {new_keyword} on a scale of 1 to 10?")
                    continue
        keep_going = input("Do you want to keep adding keywords? Type 'yes' or 'no'\n")
        if keep_going == 'yes':
            continue
        elif keep_going == 'no':
            if len(keywords.keys()) == 0:
                print("You haven't chosen any keywords!")
                continue
            else:
                break
        else:
            print("You didn't type 'yes' or 'no'. ")
    print("Your deck will have these keywords to these degrees:")
    for val in keywords.keys():
        print(f"{val} {keywords[val]}")
    return keywords

def keyword_prompt():
    keywords = []
    while True:
        new_keyword = input("Go ahead and type a keyword.\n")
        if new_keyword in keywords:
            print("You chose that keyword already.")
        else:
            keywords.append(new_keyword)
        keep_going = input("Do you want to keep adding keywords? Type 'yes' or 'no'\n")
        if keep_going == 'yes':
            continue
        elif keep_going == 'no':
            if len(keywords) == 0:
                print("You haven't chosen any keywords!")
                continue
            else:
                break
        else:
            print("You didn't type 'yes' or 'no'. ")
    return keywords

# Asks the user to select colors for their deckself.
# If they want, they can select no colors.
def color_prompt():
    colors = []
    while True:
        new_color = input("Type 'W', 'U', 'B', 'R', or 'G', case-sensitive.\n")
        if new_color in colors:
            print("You chose that color already.")
        elif new_color in ['W', 'B', 'U', 'R', 'G']:
            colors.append(new_color)
        else:
            print("Sorry, you didn't type your color correctly.")
        keep_going = input("Do you want to keep adding colors? Type 'yes' or 'no', case sensitive.\n")
        if keep_going == 'yes':
            continue
        elif keep_going == 'no':
            break
        else:
            print("You didn't type 'yes' or 'no'. ")
    return colors

def color_map():
    color_map = {
        'W' : 'White',
        'U' : 'Blue',
        'B' : 'Black',
        'R' : 'Red',
        'G' : 'Green'
    }
    return color_map

def random_colors(number_of_colors, forced_colors = [],
    W = .2, U = .2, B = .2, R = .2, G = .2):
    colors = []
    for val in forced_colors:
        colors.append(val)
    while len(colors) < number_of_colors:
        new_color = numpy.random.choice(['W', 'U', 'B', 'R', 'G'],
        p = [W, U, B, R, G])
        if new_color not in colors:
            colors.append(new_color)
    return colors
