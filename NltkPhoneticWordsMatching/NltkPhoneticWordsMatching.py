# -*- coding: utf-8 -*-
import re
import json

import nltk
from nltk.corpus import stopwords


class NltkPhoneticWordsMatching(object):
    """A practical samll program to do the phonetic matching with nltk"""
    
    def __init__(self):
        self.phonetic_list = list()
        self.phonetic_list_final_unique = list()
    
    def get_the_phonetic_from_nltk_cmudict(self):
        phonetic_list_final_tmp = list()
        
        for items in nltk.corpus.cmudict.entries():
            self.phonetic_list.append(items[1])

        for extracted_items in self.phonetic_list:
            for phonetics in extracted_items:
                phonetic_list_final_tmp.append(phonetics)
        
        # nltk还有重读音节等等，这个地方直接判断为有这种音节就算有这个音素
        for index in range(len(phonetic_list_final_tmp)):
            if (phonetic_list_final_tmp[index][-1] == "0") | (phonetic_list_final_tmp[index][-1] == "1") | (phonetic_list_final_tmp[index][-1] == "2"):
                phonetic_list_final_tmp[index] = phonetic_list_final_tmp[index][:-1]
 
        for items in phonetic_list_final_tmp:
            if items in self.phonetic_list_final_unique:
                pass
            else:
                self.phonetic_list_final_unique.append(items)
        
        return self.phonetic_list_final_unique

    @staticmethod
    def get_data_from_raw_sents():
        # 绝对路径，请把py文件和data文件放在一起
        with open("phonetic_transaction_raw_data") as file:
            data = file.read()
        
        # 先根据换行符切分
        tmp_list = data.split("\n")
        
        for index in range(len(tmp_list)):
            tmp_list[index] = re.sub("\.", "", tmp_list[index])
            
        final_list = []
        bracket = []

        for index in range(len(tmp_list)):
            if len(bracket) == 11:
                final_list.append(bracket)
                bracket = list()
                bracket.append(tmp_list[index])
            else:
                bracket.append(tmp_list[index])

        # 由于未知的原因缺少了list 72，只有一个那就直接人工按照规则补上
        final_list.append(
            ['List 72',
             'A gold ring will please most any girl',
             'The long journey home took a year',
             "She saw a cat in the neighbor's house",
             'A pink shell was found on the sandy beach',
             'Small children came to see him',
             'The grass and bushes were wet with dew',
             'The blind man counted his old coins',
             'A severe storm tore down the barn',
             'She called his name many times',
             'When you hear the bell, come quickly']
        )

        return final_list
    
    @staticmethod
    def get_phoneics_in_each_list(the_phonetic_list: list):
        # 设置使用英语的停止词
        stop = set(stopwords.words('english'))
    
        # 列表解析获取第一个数值并做成初始列表，得到各个list去除stopwords的版本
        finished_list = [i for i in the_phonetic_list[0:1]]
        for sents in the_phonetic_list[1:]:
            process_finished_sents = [i for i in sents.lower().split() if i not in stop]
            # 处理掉一些逗号什么的
            for index in range(len(process_finished_sents)):
                process_finished_sents[index] = re.sub(",", "", process_finished_sents[index])
                # 如果有这种连接词，那就split好了之后去掉本身这个并extends拆分出来的词
                if "-" in process_finished_sents[index]:
                    tmp_words_list = process_finished_sents[index].split("-")
                    process_finished_sents.pop(index)
                    process_finished_sents.extend(tmp_words_list)

            finished_list.append(process_finished_sents)

        tmp_list = list()
        # 设置应用cmudict的arpabet
        arpabet = nltk.corpus.cmudict.dict()
        finished_list0 = [i for i in finished_list[0:1]]
        for lists in finished_list[1:]:
            for word in lists:
                try:
                    tmp_list.append(arpabet[word])
                except KeyError:  # 很可能存在无法辨识的word
                    print(word)
                finished_list0.append(tmp_list)
                tmp_list = list()

        finished_list_final = [i for i in finished_list0[0:1]]
        for items in finished_list0[1:]:
            try:
                for index in range(len(items)):
                    for phonetics in items[index][0]:
                        # 先进行尾部的处理，适应39个音素的需求
                        if (phonetics[-1] == "0") | (phonetics[-1] == "1") | (phonetics[-1] == "2"):
                                phonetics = phonetics[:-1]
                        if phonetics not in finished_list_final:
                            finished_list_final.append(phonetics)
                        else:
                            pass
            except IndexError:
                print(items)
        
        return finished_list_final
    
    def gen_the_final_phonetics_list(self):
        finished_phonetic_list_final = list()
        print(len(self.get_data_from_raw_sents()))
        for lists in self.get_data_from_raw_sents():
            finished_phonetic_list_final.append(self.get_phoneics_in_each_list(lists))
        
        return finished_phonetic_list_final
    
    # matching check, 因为是unique的，只要是len为39的就可以确定为全部match
    def matching_check(self):
        all_matched_phonetics_from_lists = list()
        matching_check_list = self.gen_the_final_phonetics_list()
        list_tag = 1
        for phonetics_lists_index in range(len(matching_check_list)):
            if len(matching_check_list[phonetics_lists_index]) == 39:
                all_matched_phonetics_from_lists.append(matching_check_list[phonetics_lists_index])
                all_matched_phonetics_from_lists.append("List {}".format(str(phonetics_lists_index)))
                all_matched_phonetics_from_lists.append(len(matching_check_list[phonetics_lists_index]))
            else:
                all_matched_phonetics_from_lists.append("List {}, ".format(str(phonetics_lists_index)))
                all_matched_phonetics_from_lists.append(len(matching_check_list[phonetics_lists_index]))

        with open("matching_check.txt", 'w', encoding='utf-8') as file:
            json.dump(all_matched_phonetics_from_lists, file)
        
        # 输出所有能找到的phonetics
        with open("all_results_for_phonetics.txt", 'w', encoding='utf-8') as file:
            json.dump(matching_check_list, file)
    
        return 0


if __name__ == "__main__":
    phonetic_obj = NltkPhoneticWordsMatching()
    all_phonetics = phonetic_obj.get_the_phonetic_from_nltk_cmudict()
    print(all_phonetics)
    results_for_console_checking = phonetic_obj.gen_the_final_phonetics_list()
    print(results_for_console_checking)
    phonetic_obj.matching_check()
    # a = nltk.corpus.cmudict.dict()
    # print(a["shaped"])
