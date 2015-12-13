# coding: utf-8

import kenlm

class twitter_lm:
    def __init__(self):
        self.model = kenlm.LanguageModel('/home/cbtuser014/corpus/lm.arpa')

    def calc_score(self, text):
        return self.model.score(text)

if __name__ == "__main__":
    lm = twitter_lm()
    print(lm.calc_score("今日 は 良い 天気 です ．"))
    print(lm.calc_score("電気 水 は 天気 大統領 ．"))
