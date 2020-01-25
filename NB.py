import json
import math

# 2a
# Training:
import os


def constructing_parameters(total_dict, label_dict_1, label_dict_2, label_name_1, label_name_2):
    param_dict = {}
    total_words_label_1 = 0
    total_words_label_2 = 0
    for v in label_dict_1.values():
        total_words_label_1 += v
    for v in label_dict_2.values():
        total_words_label_2 += v
    for word in total_dict:
        if word in label_dict_1:
            prob_label_1 = (label_dict_1[word] + 1) / (total_words_label_1 + len(total_dict))
        else:
            prob_label_1 = 1 / (total_words_label_1 + len(total_dict))
        if word in label_dict_2:
            prob_label_2 = (label_dict_2[word] + 1) / (total_words_label_2 + len(total_dict))
        else:
            prob_label_2 = 1 / (total_words_label_2 + len(total_dict))
        prob1 = (word, label_name_1)
        prob2 = (word, label_name_2)
        param_dict[prob1] = prob_label_1
        param_dict[prob2] = prob_label_2
    return param_dict


# Testing
def testing(features_in_document, param_dict, prior_prob_1, prior_prob_2, label_name_1, label_name_2, total_dict):
    label_1_candidate = 0
    for feature in features_in_document:
        if feature not in total_dict:
            continue
        label_1_candidate += math.log(param_dict[(feature, label_name_1)], 2)

    label_2_candidate = 0
    for feature in features_in_document:
        if feature not in total_dict:
            continue
        label_2_candidate += math.log(param_dict[(feature, label_name_2)], 2)

    return (math.log(prior_prob_1) + label_1_candidate), math.log(prior_prob_2) + label_2_candidate


# Making Dictionaries for Analysis
def make_dictionary(file_name):
    word_frequency = {};
    file = open(file_name, 'r')
    file_as_text = file.read()
    file.close()
    individual_words = file_as_text.split()
    for word in individual_words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return word_frequency


def combine_texts(file_list):
    texts_combined = open('analysis_texts_combined.txt', 'a+')
    for index in range(0, len(file_list)):
        file_part = open(file_list[index], 'r', encoding='ISO-8859-1')
        file_string = file_part.read()
        texts_combined.write(file_string + " ")
        file_part.close()
    texts_combined.close()


# Question 2b
# Manually converting small corpus
test_sentence = "fast,couple,shoot,fly"
comedy_dict = {"fun": 3, "couple": 2, "love": 2, "fly": 1, "fast": 1}
action_dict = {"fast": 2, "furious": 2, "shoot": 4, "fun": 1, "love": 1, "fly": 1}
amass_above = {"fun": 4, "couple": 2, "love": 3, "fly": 2, "fast": 3, "furious": 2, "shoot": 4}
comedy_prob = 2 / 5
action_prob = 3 / 5
small_label_1 = "comedy"
small_label_2 = "action"
small_params = constructing_parameters(amass_above, comedy_dict, action_dict, small_label_1, small_label_2)
small_file = open('movie-review-small.txt', 'a+')
for k1, k2 in small_params.keys():
    s = "Probability of {} in label {} is {} \n".format(k1, k2, small_params[(k1, k2)])
    small_file.write(s)
small_file.close()
small_test_features = test_sentence.split(',')
small_result = testing(small_test_features, small_params, comedy_prob, action_prob, small_label_1, small_label_2,
                       amass_above)
print(
    "For the test sentence, comedy has a label of %s and action has a label of %s" % (small_result[0], small_result[1]))

# Question 2c
# Getting prior probabilities
positiveTrain = "movie-review-HW2/aclImdb/train/pos/"
negativeTrain = "movie-review-HW2/aclImdb/train/neg/"
positiveTrain = os.listdir(positiveTrain)
negativeTrain = os.listdir(negativeTrain)
positive_prior_prob = len(positiveTrain) / (len(positiveTrain) + len(negativeTrain))
negative_prior_prob = len(negativeTrain) / (len(positiveTrain) + len(negativeTrain))

# Getting the Dictionaries in order
with open('pos_training.json') as f:
    pos_training = json.load(f)

with open('total_dictionary.json') as f:
    all_words = json.load(f)

with open('neg_training.json') as f:
    neg_training = json.load(f)

# Getting and Writing the Parameters to a file
all_parameters = constructing_parameters(all_words, pos_training, neg_training, 'positive', 'negative')
all_params_file = open('movie-review-BOW-NB.txt', 'a+')
for k1, k2 in all_parameters.keys():
    s = "Probability of {} in label {} is {} \n".format(k1, k2, all_parameters[(k1, k2)])
    all_params_file.write(s)
all_params_file.close()

# Testing
# Positive Dataset
pos_test_inaccuracies = []
os.chdir("movie-review-HW2/aclImdb/test/pos/")
positiveTest = os.listdir(".")
test_results_file = open("all-test-results.txt", 'a+')
positives = 0
negatives = 0
for file_name in positiveTest:
    file = open(file_name, 'r', encoding= 'ISO-8859-1')
    file_text = file.read()
    file.close()
    test_features = file_text.split()
    test_result = testing(test_features, all_parameters, positive_prior_prob, negative_prior_prob, 'positive',
                          'negative',
                          all_words)
    if test_result[0] > test_result[1]:
        test_results_file.write(
            file_name + " has a higher probability for the positive label: %s \n" % (test_result[0]))
        positives += 1
    else:
        test_results_file.write(
            file_name + " has a higher probability for the negative label: %s \n" % (test_result[1]))
        negatives += 1
        pos_test_inaccuracies.append(file_name)
test_results_file.write("The model has a total accuracy of %s" % (positives / (positives + negatives)))

combine_texts(pos_test_inaccuracies)
pos_test_inaccuracies = make_dictionary('analysis_texts_combined.txt')
with open('pos_test_inaccuracies.json', 'w+') as fp:
    json.dump(pos_test_inaccuracies, fp)

# Negative Dataset
neg_test_inaccuracies = []
os.chdir("../neg/")
negativeTest = os.listdir(".")
test_results_file = open("all-test-results.txt", 'a+')
positives = 0
negatives = 0
for file_name in negativeTest:
    file = open(file_name, 'r', encoding='ISO-8859-1')
    file_text = file.read()
    file.close()
    test_features = file_text.split()
    test_result = testing(test_features, all_parameters, positive_prior_prob, negative_prior_prob, 'positive',
                          'negative',
                          all_words)
    if test_result[0] > test_result[1]:
        test_results_file.write(
            file_name + " has a higher probability for the positive label: %s \n" % (test_result[0]))
        positives += 1
        neg_test_inaccuracies.append(file_name)
    else:
        test_results_file.write(
            file_name + " has a higher probability for the negative label: %s \n" % (test_result[1]))
        negatives += 1
test_results_file.write("The model has a total accuracy of %s" % (negatives / (positives + negatives)))

combine_texts(neg_test_inaccuracies)
neg_test_inaccuracies = make_dictionary('analysis_texts_combined.txt')
with open('neg_test_inaccuracies.json', 'w+') as fp:
    json.dump(neg_test_inaccuracies, fp)
