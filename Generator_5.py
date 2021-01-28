import mtg
import csv
import random
import math
import numpy
import itertools
import copy

def make(number_of_decks, master_list, synergy_list, master_mb_spinner, master_sb_spinner):
    for deck_number in range(0, number_of_decks):
        mb_spinner = copy.deepcopy(master_mb_spinner)
        sb_spinner = copy.deepcopy(master_sb_spinner)
        the_deck = mtg.Deck()

        number_of_colors = numpy.random.choice([2, 3, 4, 5], p = [.02, .27, .42, .29])
        colors = mtg.random_colors(number_of_colors, forced_colors = ['U'],
                    W = .25, U = 0, R = .25, G = .3)

        yorion = numpy.random.choice([True, False], p = [.11, .89])
        if yorion:
            mb_target_size = 80
            n = mtg.name_retrieve("Yorion, Sky Nomad", master_list)
            the_deck.sb_add(n)
            mb_spinner.multiply("Ice-Fang Coatl", 2.5)
        else:
            mb_target_size = 60

        have_synergy_group = numpy.random.choice([True, False], p = [.28, .72])
        synergy_name = ""
        if have_synergy_group:
            while True:
                synergy_name = numpy.random.choice(["GSZ", "Wheels", "RIP_Helm", "Worldgorger", "PFire_Dack"],
                p = [.36, .33, .04, .11, .16])
                our_synergy_group = mtg.get_synergy_group_by_name(synergy_name, synergy_list)
                fine = True
                for val in our_synergy_group.get_colors():
                    if val not in colors:
                        fine = False
                if fine:
                    break
            our_synergy_group.apply(colors, the_deck, mb_spinner, sb_spinner, master_list)
        else:
            mb_spinner.multiply("Hullbreacher", .6)
            mb_spinner.multiply("Narset, Parter of Veils", .8)

        keyword_values = dict()
        if number_of_colors == 2:
            keyword_values['Land'] = .325
            keyword_values['Threat'] = .186
            keyword_values['Answer'] = .117
            keyword_values['Fetch'] = .133
            keyword_values['Basic'] = .067
            keyword_values['Dual'] = .058
            keyword_values['Utility'] = 0
        elif number_of_colors == 3:
            keyword_values['Land'] = .333
            keyword_values['Threat'] = .087
            keyword_values['Answer'] = .090
            keyword_values['Fetch'] = .146
            keyword_values['Basic'] = .074
            keyword_values['Dual'] = .061
            keyword_values['Utility'] = .041
        elif number_of_colors == 4:
            keyword_values['Land'] = .333
            keyword_values['Threat'] = .085
            keyword_values['Answer'] = .112
            keyword_values['Fetch'] = .149
            keyword_values['Basic'] = .090
            keyword_values['Dual'] = .062
            keyword_values['Utility'] = .022
        elif number_of_colors == 5:
            keyword_values['Land'] = .333
            keyword_values['Threat'] = .114
            keyword_values['Answer'] = .147
            keyword_values['Fetch'] = .152
            keyword_values['Basic'] = .1
            keyword_values['Dual'] = .068
            keyword_values['Utility'] = .016
        keyword_minima= {}
        for val in keyword_values:
            keyword_minima[val] = math.floor(keyword_values[val] * mb_target_size) - 1
        lt = round(keyword_values['Land'] * mb_target_size)
        lands_target = random.choice([lt - 1, lt, lt + 1])
        spells_target = mb_target_size - lands_target
        if synergy_name == "PFire_Dack":
            spells_target += 2

        the_deck.mb_add_by_name("Brainstorm", master_list, number = 4)
        the_deck.mb_add_by_name("Force of Will", master_list, number = 4)
        the_deck.mb_add_by_name("Ponder", master_list, number = 3)
        if len(colors) == 2:
            mb_spinner.multiply("Arcum's Astrolabe", 0)
        elif len(colors) == 3:
            the_deck.mb_add_by_name("Arcum's Astrolabe", master_list, number = 1)
        else:
            the_deck.mb_add_by_name("Arcum's Astrolabe", master_list, number = 4)

        mb_spinner.color_prune(colors, master_list)
        sb_spinner.color_prune(colors, master_list)
        mb_spell_spinner = {}
        old_mb_spinner = mb_spinner.get_spinner()
        for val in old_mb_spinner:
            if ("Land" not in mtg.name_retrieve(val, master_list).get_types()) and \
             ("Synergy_Only" not in mtg.name_retrieve(val, master_list).get_properties()):
                mb_spell_spinner[val] = old_mb_spinner[val]
        mb_spell_spinner = mtg.Spinner(mb_spell_spinner)
        mb_spell_spinner.balance()
        mb_land_spinner = {}
        for val in old_mb_spinner:
            if ("Land" in mtg.name_retrieve(val, master_list).get_types()) and \
             ("Synergy_Only" not in mtg.name_retrieve(val, master_list).get_properties()):
                mb_land_spinner[val] = old_mb_spinner[val]
        mb_land_spinner = mtg.Spinner(mb_land_spinner)
        mb_land_spinner.balance()
        new_sb_spinner = {}
        old_sb_spinner = sb_spinner.get_spinner()
        for val in old_sb_spinner:
            if ("Synergy_Only_SB" not in mtg.name_retrieve(val, master_list).get_properties()):
                new_sb_spinner[val] = old_sb_spinner[val]
        sb_spinner = mtg.Spinner(new_sb_spinner)
        sb_spinner.balance()

        while the_deck.get_mb_size() < spells_target:
            new_card_name = mb_spell_spinner.spin()
            new_card = mtg.name_retrieve(new_card_name, master_list)
            if (mtg.name_in_list_number(new_card_name, the_deck.get_seventyfive()) < 4) or \
            ("Basic" in mtg.name_retrieve(new_card_name, master_list).get_types()):
                if ("Threat" not in new_card.get_properties()) and \
                (mtg.keyword_occurrences("Threat", the_deck.get_mb()) < \
                keyword_minima["Threat"]):
                    if ("Answer" in new_card.get_properties()) and \
                    (mtg.keyword_occurrences("Answer", the_deck.get_mb()) < \
                    keyword_minima["Answer"]):
                        the_deck.mb_add(new_card)
                    else:
                        continue
                elif ("Answer" not in new_card.get_properties()) and \
                    (mtg.keyword_occurrences("Answer", the_deck.get_mb()) < \
                    keyword_minima["Answer"]):
                    continue
                else:
                    the_deck.mb_add(new_card)

        the_deck.mb_add_by_name("Snow-Covered Island", master_list, number = 2)

        colors_minus_blue = []
        for val in colors:
            if val != 'U':
                colors_minus_blue.append(val)

        for val in master_list:
            for val2 in colors_minus_blue:
                if (val2 in val.get_mana_source()) and ('U' in val.get_mana_source()) \
                and (("Dual" in val.get_properties()) or (("Fetch" in val.get_properties()) and ("Prismatic Vista" not in val.get_name()))):
                    the_deck.mb_add(val)
                if (val2 in val.get_mana_source()) and ("Snow Land" in val.get_types()) \
                and (the_deck.get_color_pips()[val2] > 2):
                    the_deck.mb_add(val)


        for val in master_list:
            if (("Dual" in val.get_properties()) or ("Basic" in val.get_properties() \
            or ("Utility" in val.get_properties()))):
                for val2 in val.get_mana_source():
                    if val2 not in colors:
                        mb_land_spinner.multiply(val.get_name(), 0)
            if ("Fetch" in val.get_properties()) and ("Prismatic Vista" not in val.get_name()):
                for val2 in val.get_mana_source():
                    if val2 not in colors:
                        mb_land_spinner.multiply(val.get_name(), .3)

        while the_deck.get_mb_size() < mb_target_size:
            new_card_name = mb_land_spinner.spin()
            new_card = mtg.name_retrieve(new_card_name, master_list)
            properties = new_card.get_properties()
            current_mb = the_deck.get_mb()
            under_any_minima = False
            added_already = False
            if (mtg.name_in_list_number(new_card_name, current_mb) < 4) or \
            ("Basic" in mtg.name_retrieve(new_card_name, master_list).get_types()):
                for val in ["Utility", "Fetch", "Basic", "Dual"]:
                    if (mtg.keyword_occurrences(val, current_mb) < \
                    keyword_minima[val]):
                        if (val in properties):
                             the_deck.mb_add(new_card)
                             added_already = True
                             break
                        else:
                             under_any_minima = True
                if under_any_minima:
                    continue
                else:
                    if not added_already:
                        the_deck.mb_add(new_card)

        while the_deck.get_sb_size() < 15:
            new_card_name = sb_spinner.spin()
            if (mtg.name_in_list_number(new_card_name, the_deck.get_seventyfive()) < 4) or \
            ("Basic" in mtg.name_retrieve(new_card_name, master_list).get_types()):
                the_deck.sb_add_by_name(new_card_name, master_list)

        print("This many decks finished:", deck_number)

        deck_number_str = str(deck_number)
        the_deck.save_to_file(deck_number_str, deck_number_str)

master_list = mtg.csv_to_list("Blue_Stew_Cards.csv")
synergy_list = mtg.csv_to_synergy_list("Synergy_Groups - Sheet1.csv")
master_mb_spinner = mtg.dir_mb_spinner("Blue_Stew_Decks/", master_list)
master_sb_spinner = mtg.dir_sb_spinner("Blue_Stew_Decks/", master_list)

make(25000, master_list, synergy_list, master_mb_spinner, master_sb_spinner)
