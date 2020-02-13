# exj_gender.py
# assigns gender and calculates gender percentage to name-lists of judicial debt collectors
# (RO: executori judecătorești)

import os
import csv
import json
import string

def assign_gender():
    """
    :return: none; overwrites existing, genderless csv files
    """

    prct_change = []

    file_counter = 0  # for debugging
    for f in os.listdir("csv"):  # iterate through name-lists and open them
        year = f[0:4]
        file_counter += 1
        new_rows = []
        with open("csv/" + f) as inFile:
            csv_reader = csv.reader(inFile, delimiter=';')
            headers = next(csv_reader)  # catch and skip headers

            person_count = 0
            fml = 0
            for row in csv_reader:
                if row[0] != '':  # skip empty rows
                    person_count += 1
                    given_names = row[2]
                    gndr = gndr_assgn(given_names)
                    if gndr == "f":
                        fml += 1
                    new_rows.append(row[0:3] + [gndr] + row[4:])

        prcnt_fml = round(((fml / person_count) * 100), 1)
        prct_change.append([year, prcnt_fml])

        # now write in the updated .csv
        with open("gndrd_prcnt/" + f, 'w') as outFile:
            writer = csv.writer(outFile, delimiter=';')
            writer.writerow(headers[0:3] + ["sex"] + headers[4:])
            for r in new_rows:
                writer.writerow(r)

        # if file_counter > 1:
        #    return

    # make file with percent change
    prct_change.sort()
    with open("gndrd_prcnt/female_percent_change.txt", 'w') as outFile:
        writer = csv.writer(outFile, delimiter=' ')
        writer.writerow(["year", "percent female"])
        for r in prct_change:
            writer.writerow(r)


def check_equal(lst):
    """
    Check if every entry in the list is identical
    :param lst: a list
    :return: True or False
    """
    return lst[1:] == lst[:-1]


def gndr_assgn(given_names):
    """
    Go through a list of given names, compare it to a dictionary of name-gender links, and
    decide whether the list represents a male or female name.
    :param given_names: list of given names
    :return: a string with the person's gender, "f", "m", or "dk" for "don't know"
    """

    with open("ro_gender_dict.txt") as dict_file:  # load name-gender dict
        gend_dict = json.load(dict_file)

        # make a string cleaner for removing pucntuation for later use
        cleaner = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

        person_gender = []
        given_names = given_names.translate(cleaner).strip().split(' ')

        for name in given_names:
            if (name.upper() not in gend_dict) and (name != ""):  # if no match, mark as "don't know"
                person_gender.append('dk')
            else:
                person_gender.append(gend_dict[name.upper()])

        # now assign full given name gender, by majority vote
        m, f = 0, 0
        for g in person_gender:
            if g == "m":
                m += 1
            if g == "f":
                f += 1
        if m > f:
            person_gender = "m"
        elif f > m:
            person_gender = "f"
        else:  # if they're even, it's ambiguous
            person_gender = "dk"

        if type(person_gender) == list:
            person_gender = ' '.join(map(str, person_gender))

        return person_gender


assign_gender()
