import os

# def makeDictionary(file):
#     word_frequency = {}
#     for file in file_list:
#         file_string = file.read()
#         word_frequency



#Getting the File names
positiveTrain = "movie-review-HW2/aclImdb/train/pos/"
negativeTrain = "movie-review-HW2/aclImdb/train/neg/"
positiveTrain = os.listdir(positiveTrain)
negativeTrain = os.listdir(negativeTrain)


#Storing the total amount of documents in each class
total_documents = len(positiveTrain) + len(negativeTrain)
total_positive_documents = total_documents - len(negativeTrain)
total_negative_documents = total_documents - len(positiveTrain)


# Combining All texts with a positive label
os.chdir("movie-review-HW2/aclImdb/train/pos/")
pos_training_texts_combined = open('all_positive_training_texts.txt', 'a+')
for index in range(0, len(positiveTrain)):
    file_part = open(positiveTrain[index],'r')
    file_string = file_part.read()
    pos_training_texts_combined.write(file_string + " ")
    file_part.close()
pos_training_texts_combined.close()



#Combining All texts with a negative label
os.chdir("../neg/")
neg_training_texts_combined = open('all_negative_training_texts.txt', 'a+')
for index in range(0, len(negativeTrain)):
    file_part = open(negativeTrain[index],'r')
    file_string = file_part.read()
    neg_training_texts_combined.write(file_string + " ")
    file_part.close()

neg_training_texts_combined.close()