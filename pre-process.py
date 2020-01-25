import re
import os
import sys


def preprocessFile(filepath):
    file = open(filepath, 'r')
    fileText = file.read()
    file.close()
    fileText = fileText.lower()
    fileText = re.sub('([.,:;*&^%$#@~\'\"?/!()])', r' \1 ',fileText)
    fileText = re.sub('\s{2,}', ' ', fileText)
    fileText = fileText.replace("<br / ><br / >",'\n\n')
    file = open(filepath, 'w')
    file.write(fileText)
    file.close()


positiveTrain = "movie-review-HW2/aclImdb/train/pos/"
negativeTrain = "movie-review-HW2/aclImdb/train/neg/"
positiveTest = "movie-review-HW2/aclImdb/test/pos/"
negativeTest = "movie-review-HW2/aclImdb/test/neg/"

positiveTrain = os.listdir(positiveTrain)
negativeTest = os.listdir(negativeTest)
positiveTest = os.listdir(positiveTest)
negativeTrain = os.listdir(negativeTrain)

os.chdir("movie-review-HW2/aclImdb/test/pos/")
for file in positiveTest:
    preprocessFile(file)


os.chdir("../../train/pos/")
for file in positiveTrain:
    preprocessFile(file)


os.chdir("../../test/neg/")
for file in negativeTest:
    preprocessFile(file)


os.chdir("../../train/neg/")
for file in negativeTrain:
    preprocessFile(file)


os.chdir(os.path.dirname(sys.argv[0]))
