ProjectName: NltkPhoneticWordsMatching
author:bingcong.wu
version:1.0-released
updated at : 8/13/2017 1:27:00
status:released, all bugs fixed

概况：大量35至37音素的列表，可考虑使用

逻辑：如果有matching，会直接整个列表输入（很遗憾没有）

如果没有matching：会指出每个列表有多少个音素，具体哪些音素请对照all_results

运行方法：在有python3.6的情况下需要nltk，需要nltk的stopwords和corpus.cmudict

环境配置方法请Google，用pip和nltk.download可以解决，在此不赘述

// 请先阅读项目相关

项目相关：

脚本使用的是NLP工程界认可的NLTK

根据一般NLP规则借鉴cmu提供的stopwords对stopwords进行了去除

字典用的是cmudict以及cmu的phonetic alphabet

一切符合NLTK官方规范

matching的检查没有发现完全拟合的list

按照39个音素的标准NLP工程规范进行的match

找到音素输出在all_results中

matching的结果在matching文件中，为空array

dump后是json文件（代码里写的是）

我已经改成了txt

=======================================================

代码相关：

如果有需要可以参考注释，删除掉unique音素的判断条件

进行带0,1,2后缀的matching check（NLP alphabet规则：0,1,2分别是：是否重读，请google相关资料）

但是预测matching结果应该不会改变

可能需要跟你们boss讨论一下他的实际需求

如对代码的细节有什么疑问请直接联系


如果需要进行完成的代码调试并沿用此脚本进行修改

请把所有data放在和py文件同个文件夹下

raw_data已经在里面

改后直接运行，不需要修改路径，全部都是相对路径



祝好！

吴秉聪


