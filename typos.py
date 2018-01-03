# coding=utf-8

from __future__ import print_function, unicode_literals, division
from codecs import open

from collections import defaultdict
import sys

import time

from edit_distance import edit_distance
from typos_utils import remove_polish_symbols_and_duplicates, get_unigrams, normalized_morphosyntactic, generate_near_words


MAX_EDIT_DISTANCE = 2


def more_search(near_words, morphosyntactic):
    return None
    # min_length = len(min(near_words, key=lambda x: len(x)))
    # for word in near_words:
    #     if len(word) <= min_length + 3:
    #         for char_index in range(len(word), 0, -1):
    #             if word[:char_index] + word[char_index + 1:] in morphosyntactic:
    #                 return word[:char_index] + word[char_index + 1:]


# def fin_edit_distances(file_path="./literowki_dev1.txt"):
#     ed = defaultdict(lambda: 0)
#
#     with open(file_path, encoding="utf8") as file:
#         ambigous = 0
#         missing = 0
#         unigrams = get_unigrams()
#         morphosyntactic = normalized_morphosyntactic(unigrams)
#         for line in file:
#             line = line.split()
#             if len(line) == 2:
#                 ed[edit_distance(remove_polish_symbols_and_duplicates(line[0]),
#                                  remove_polish_symbols_and_duplicates(line[1]))] += 1
#                 if len(morphosyntactic[remove_polish_symbols_and_duplicates(line[0])]) > 1:
#                     ambigous += 1
#                     print("a", line[0],
#                           [(amb_word, edit_distance(amb_word[0], line[1])) for amb_word in morphosyntactic[remove_polish_symbols_and_duplicates(line[0])]])
#                 if len(morphosyntactic[remove_polish_symbols_and_duplicates(line[0])]) == 0:
#                     missing += 1
#                     print("m", line[0])
#                 # if edit_distance(remove_polish_symbols_and_duplicates(line[0]),
#                 #                  remove_polish_symbols_and_duplicates(line[1])) == 5:
#                 #     print(line)
#     print(missing, ambigous)
#     print(ed)


def correct_typos(file_path="./literowki_dev1.txt", unigrams_path="1grams",
                  morph_dictionary_path="./polimorfologik-2.1.txt"):
    unigrams = get_unigrams(unigrams_path)
    morphosyntactic = normalized_morphosyntactic(unigrams, morph_dictionary_path)

    max_time = 0

    with open(file_path, encoding="utf8") as file:
        t1 = time.time()
        ambigous2 = 0
        working = 0
        line_number = -1
        for line_number, line in enumerate(file):
            t0 = time.time()
            correct, wrong = line.split()
            possibly_corrected = []
            possibly_corrected_polish = []
            k = 0
            near_words = generate_near_words(remove_polish_symbols_and_duplicates(wrong), MAX_EDIT_DISTANCE)
            for i in range(MAX_EDIT_DISTANCE + 1):
                for w in near_words[i]:
                    if w in morphosyntactic:
                        k += 1
                        possibly_corrected.append(w)
                if k > 0:
                    break
            if k > 1:
                ambigous2 += 1

            for word in possibly_corrected:
                for polish_word in morphosyntactic[word]:
                    possibly_corrected_polish.append((polish_word, unigrams.get(polish_word, 0)))

            if len(possibly_corrected_polish) > 0:
                min_edit_distance = edit_distance(
                    min(possibly_corrected_polish, key=lambda x: edit_distance(x[0], wrong))[0], wrong)
                corrected = max(
                    possibly_corrected_polish,
                    key=lambda x: x[1] / (edit_distance(x[0], wrong) - min_edit_distance + 1))[0]
            else:
                # more_distant_words = []
                more_distant_word = more_search(near_words[MAX_EDIT_DISTANCE], morphosyntactic)
                if more_distant_word is None:
                    corrected = "okoń"
                else:
                    pass
                    # for polish_word in morphosyntactic[more_distant_word]:
                    #     more_distant_words.append((polish_word, unigrams[polish_word]))
                    #
                    # if more_distant_words == []:
                    #     corrected = "okoń"
                    # else:
                    #     min_edit_distance = edit_distance(
                    #         min(more_distant_words, key=lambda x: edit_distance(x[0], wrong))[0], wrong)
                    #     corrected = max(
                    #         more_distant_words,
                    #         key=lambda x: x[1] / (edit_distance(x[0], wrong) - min_edit_distance + 1))[0]

            if corrected == correct:
                working += 1
                print(line.split(), edit_distance(correct, wrong))
                print("\n".join([str(p) for p in possibly_corrected_polish]))
                print("c ", corrected)
                print("\n\n\n")
            else:
                print(line.split(), edit_distance(correct, wrong), file=sys.stderr)
                print("\n".join([str(p) for p in possibly_corrected_polish]), file=sys.stderr)
                print("c ", corrected, file=sys.stderr)
                print("\n\n\n", file=sys.stderr)
            max_time = max(max_time, time.time() - t0)

        print("Max time: ", max_time)
        print("Average time: ", (time.time() - t1) / line_number, line_number)

        print(working / line_number + 1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        correct_typos(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        correct_typos()
