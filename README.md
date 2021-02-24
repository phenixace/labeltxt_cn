# labeltxt_cn
Help Researchers easy to label Chinese NER dataset.

## Envrionment
python >= 3.7;

java >= 1.8.0;

## Requirement
pyqt5;

snownlp;

fastNLP;  #I made some changes in the original codes of fastNLP, changes will be shown in the directory--FASTNLP
          #You can put the file in dir "fastNLP.core" to replace original "tester.py"

hanlp;

harvesttext;

configparser;

progressbar;

if there is no special mark, all version is ok.

## usage
0.please download my ner model, I put it in the "save" directory

1.run "python labeltxt.py"

2.choose your source-directory and save-directory

3.window would init and show all your txt files and their according ner initial label in the directory by name sequence

4.press "保存"(save) button to save labeled txt file
5.press "上一个"(last)/"下一个"(next) to change previous file shown on the screen

## future version
I plan to add emotion label function in future versions
