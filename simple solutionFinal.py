# -*- coding: utf-8 -*-

import unicodecsv as csv
import codecs
from datetime import datetime
import numpy as np
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

print(str(datetime.now()))
# объявим где хранятся исходные данные
PATH_TRAIN = './input/train.csv'
PATH_TEST = './input/test.csv'

PATH_NEW_DICT = './input/frequently_words.csv'

fl_exter_dict = codecs.open(PATH_NEW_DICT, 'r','utf-8')

external_dict = {}

for line in fl_exter_dict :
    num,freq,s1 = line.strip().split(' ')
    key = s1[:2]
    if key not in external_dict and len(s1)>2:
        external_dict[key] = s1

# объявим куда сохраним результат
PATH_PRED = 'pred.csv'

PATH_PRED2 = 'predNot.csv'

## Из тренировочного набора собираем статистику о встречаемости слов

# создаем словарь для хранения статистики
word_stat_dict = {}

# открываем файл на чтение в режиме текста
fl = codecs.open(PATH_TRAIN, 'r','utf-8')

# считываем первую строчку - заголовок (она нам не нужна)
l = fl.readline()
max_phrase = ""
max_count = 0
words_data = {}
words_count = {}
end_words = {}

words_stat_one_ch = {}


# найти наиболее популярные связки (пример существительное + глагол)
words_comb = {}
most_freq_comb = {}


# в цикле читаем строчки из файла
for line in fl:
    # разбиваем строчку на три строковые переменные
    Id, Sample, Prediction = line.strip().split(',')
    # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
    word1, word2 = Prediction.split(' ')
    wordS1, wordS2 = Sample.split(' ')
    
   # pPos1 = morph.parse(word1)[0]
    #pPos1 = pPos1.tag.POS
    #pPos2 = morph.parse(word2)[0]
    #pPos2 = pPos2.tag.POS
    
    #if pPos1 not in words_comb:
     #   words_comb[pPos1] = {}
    #if pPos2 not in words_comb[pPos1]:
    #    words_comb[pPos1][pPos2] = 0
    #words_comb[pPos1][pPos2] += 1
    
    if word1 not in words_data:
        words_data[word1] = word2
         
    if Prediction not in words_count:
        words_count[Prediction] = 1
    else:
        words_count[Prediction] += 1



    # возьмем в качестве ключа 2 первые буквы, т.к. их наличие гарантировано
    key = word2[:2]
    # возьмем в качестве ключа первую букву, т.к. их наличие гарантировано
    key_s = word2[:1]
    # возьмем окончание первого слова 
    key_end = word1[-2:]

    
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    
    if key_s not in words_stat_one_ch:
        words_stat_one_ch[key_s] = {}

    if key_end not in end_words:
        end_words[key_end] = {}

    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if word2 not in word_stat_dict[key]:
        word_stat_dict[key][word2] = 0
    word_stat_dict[key][word2] += 1


    if word2 not in words_stat_one_ch[key_s]:
        words_stat_one_ch[key_s][word2] = 0
    words_stat_one_ch[key_s][word2] += 1


    if word2[-2:] not in end_words[key_end]:
        end_words[key_end][word2[-2:]] = 0
    # увеличим значение счетчика по текущему слову на 1
    end_words[key_end][word2[-2:]] += 1


# закрываем файл
fl.close()

## Строим модель
#print(max_phrase)
# создаем словарь для хранения статистики
most_freq_dict = {}
most_freq_dict_list = {}


# проходим по словарю word_stat_dict
for key in word_stat_dict:
    #print("key", word_stat_dict[key])
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)
    most_freq_dict_list[key] = [x for x in word_stat_dict[key].keys() if word_stat_dict[key][x] > 2 ]
    #print("data ", most_freq_dict[key])

most_freq_dict_single = {}

for key in words_stat_one_ch:
    #print("key", word_stat_dict[key])
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict_single[key] = max(words_stat_one_ch[key], key=words_stat_one_ch[key].get)
    #most_freq_dict_list[key] = [x for x in word_stat_dict[key] if ]
    #print("data ", most_freq_dict[key])    
    
    
# находим самую популярную связку 
for key in words_comb:
    #print("key", word_stat_dict[key])
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_comb[key] = max(words_comb[key], key=words_comb[key].get)
    #print("data ", most_freq_dict[key])    
    
    
    
# создаем словарь для хранения статистики окончания слов
most_freq_dict_end = {}
# проходим по словарю с окончанием слов
for key in end_words:
    #print("key", word_stat_dict[key])
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict_end[key] = max(end_words[key], key=end_words[key].get)
    
    #print("data ", most_freq_dict[key])

for key in words_count:
    if words_count[key] > max_count:
        max_count = words_count[key]
        max_phrase = key
        
#не угадали
out_fl2 = open(PATH_PRED2, 'wt')        
        
def find_corr(word_dict, wordPr):
    sum_min = np.inf
    sum_d = 0
    key = ''
    if len(wordPr) == 2:
        sum_min = sum_d
        key = most_freq_dict[wordPr]
        analog_key = ""
        if wordPr in external_dict:
            analog_key = external_dict[wordPr]
            
        if analog_key != "" and len(key) > len(analog_key):
            key = analog_key
        #out_fl2.write('%s %s %s\n' % (key, " вот сколько", analog_key))
    else: 
        for value in word_dict.keys():   
            #print(wordPr, " case ", "value", value, value[wordPr.index(wordPr[-1])])
            if ((len(value) >= len(wordPr)) and (wordPr[-1] == value[wordPr.index(wordPr[-1])]) and (wordPr[2] == value[2])):
                wordPred = wordPr #+ " "*(len(value) - len(wordPr))
                #print("value", value, "len", len(value), " wordPr", wordPr, "len", len(wordPr))
                #print("first ", sum_d)
                for i in range(len(wordPred)):
                    sum_d += abs(ord(wordPred[i])-ord(value[i]))
                
                sum_d *= 100
                sum_d += len(value) - len(wordPred)
                    #print("end ", sum_d)    
                if(sum_min > sum_d):
                    #print("sum_min", sum_d, "value", value)
                    sum_min = sum_d
                    key = value 
                sum_d = 0
    if key == '':
        pPos1 = morph.parse(wordPr)[0]
        if pPos1.tag.POS !=None:
            key = pPos1.normalized.word
            out_fl2.write('%s %s\n' % (wordPr, key))
        else:
            key = most_freq_dict[wordPr[:2]]
            out_fl2.write('%s %s\n' % (wordPr, "не угадал"))
    return (key, sum_min)
    
        
        
print(max_phrase)
## Выполняем предсказание

# открываем файл на чтение в режиме текста
fl = codecs.open(PATH_TEST, 'r','utf-8')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()

# открываем файл на запись в режиме текста
out_fl = open(PATH_PRED, 'wt')

# записываем заголовок таблицы
out_fl.write('Id,Prediction\n')
count = 0
count_an = 0
# в цикле читаем строчки из тестового файла
for line in fl:
    # разбиваем строчку на две строковые переменные
    Id, Sample = line.strip().split(',')
    # строковая переменная Sample содержит в себе полностью первое слово и кусок второго слова, разделим их
    word1, word2_chunk = Sample.split(' ')
    # вычислим ключ для заданного фрагмента второго слова
    key = word2_chunk[:2]
    key_one = word2_chunk[:1]
    key_end = word1[-2:]
    
    if key in most_freq_dict:
        # если ключ есть в нашем словаре, пишем в файл предсказаний: Id, первое слово, наиболее вероятное второе слово
        word_good, sum_d = find_corr(word_stat_dict[key], word2_chunk)
        #print("word_good ", word_good)
        #проверка на окончание слов
        p1 = morph.parse(word1)[0]
        p2 = morph.parse(word_good)[0]
        num_p1 = p1.tag.number
        copy_p2 = p2
        try:
            p2 = p2.inflect({num_p1})
            if p2 != None:
                word_good = p2.word
            else: 
                p2 = copy_p2
        except ValueError:
                word_good = word_good 
                
        if p1.tag.POS =='VERB' and p2.tag.POS =='ADJF':
            gen_word = p1.tag.gender 
            try:
                p2 = p2.inflect({gen_word})
                if p2 != None:
                    word_good = p2.word
            except ValueError:
                word_good = word_good
        elif (p1.tag.POS =='NOUN'  or p1.tag.POS =='NPRO') and p2.tag.POS =='VERB':
            gen_word = p1.tag.gender   
            try:
                p2 = p2.inflect({gen_word})
                if p2 != None:
                    word_good = p2.word
            except ValueError:
                word_good = word_good
        elif p1.tag.POS =='VERB' and p2.tag.POS =='NOUN':
            num_p1 = p1.tag.number 
            p2 = p2.inflect({num_p1})
            if p2 != None:
                word_good = p2.word
        elif p1.tag.POS =='VERB' and p2.tag.POS =='VERB':
            p2 = p2.normalized
            word_good = p2.word
        elif p1.tag.POS =='NOUN' and p2.tag.POS =='NOUN': 
            p2 = p2.inflect({'gent'})
            if p2 != None:
                word_good = p2.word
        elif p1.tag.POS =='ADJF' and p2.tag.POS =='NOUN':
            case_d = p1.tag.case  
            p2 = p2.inflect({case_d})
            if p2 != None:
                word_good = p2.word
        elif p1.tag.POS =='NOUN' and p2.tag.POS =='ADJF':
            case_d = p1.tag.case 
            p2 = p2.inflect({case_d})
            if p2 != None:
                word_good = p2.word
               
        out_fl.write('%s,%s %s\n' % (Id, word1, word_good))
    else:
        if key in external_dict:
            out_fl.write('%s,%s %s\n' % (Id, word1, external_dict[key]))      
        elif key_one in most_freq_dict_single.keys():
            count +=1
            out_fl.write('%s,%s %s\n' % (Id, word1, most_freq_dict_single[key_one]))        
        else:
            count_an +=1
        # иначе пишем наиболее часто встречающееся словосочетание в целом
            out_fl.write('%s,%s\n' % (Id, max_phrase))
            

# закрываем файлы
fl.close()
fl_exter_dict.close()
out_fl.close()
out_fl2.close()

print("count", count)
print("count_an", count_an)

print(str(datetime.now()))