import json


def make_dictionary(file_name):
    word_frequency = {};
    file = open(file_name,'r')
    file_as_text = file.read()
    file.close()
    individual_words = file_as_text.split()
    for word in individual_words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return word_frequency


def make_json_file(word_dict, json_name):
    with open(json_name, 'w+') as fp:
        json.dump(word_dict, fp)


#Making the Positive and Negative Dictionaries
pos_training_dict = make_dictionary('all_positive_training_texts.txt')
make_json_file(pos_training_dict, 'pos_training.json')
neg_training_dict = make_dictionary('all_negative_training_texts.txt')
make_json_file(neg_training_dict, "neg_training.json")

#Making all texts into one dictionary and putting it into json
pos_file = open("all_positive_training_texts.txt", 'r')
neg_file = open("all_negative_training_texts.txt", 'r')
pos_file_string = pos_file.read()
neg_file_string = neg_file.read()
pos_file.close()
neg_file.close()
total_string = pos_file_string + " " + neg_file_string
total_file = open("total_file.txt", 'w+')
total_file.write(total_string)
total_file.close()
total_dictionary = make_dictionary("total_file.txt")
make_json_file(total_dictionary, "total_dictionary.json")