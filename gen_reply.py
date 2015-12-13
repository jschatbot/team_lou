# -*- coding: utf-8 -*-

import chatapi
import random

capi = chatapi.ChatbotAPI()
th_num = 100

# 言語モデルか何かで応答文を評価
def choiceReply(replylist):
        return random.choice(replylist)

# マルコフ連鎖で応答文を生成
def generateMarkovReply(replytext):
        morphs = capi.getMorphs(replytext)
        keypos = [u"一般名詞", u"固有一般", u"固有人性", u"固有人名", u"固有人他", u"固有地名", u"固有組織", u"固有賞品"]

        malkovlist = []
        for morph in morphs:
                if morph[u"pos"] in keypos:
                        malkovs = capi.generateMarkov(self, surface=morph[u"surface"], pos=morph[u"pos"])
                        str = ""
                        for mal in malkovs:
                                str += mal.split(":").rstrip('"')
                        malkovlist.append(str)
        return malkovlist

def exampleBasedReply(chunks):
        for words in chunks:
                print words.encode("utf-8")
                norm = words["norm_surface"]
                examples = capi.searchReply(norm,limit=10) # 10?
                responselist += examples[u"texts"]

def generateReply(replytext):
        chunks = capi.getChunks(replytext)

        replylist = exampleBasedReply(chunks)

        if len(examplelist) < th_num: # いつマルコフ連鎖にするか？
                replylist += generateMarkovReply(replytext)

        if len(replylist) == 0: # 返答文が作れなかった
                replylist = [u"分からないぞ？",u"もう一回"] # 辞書読み込む
                reply = random.choice(replylist)
        else:
                reply = choice_reply(replylist)

        return reply

exampleBasedReply("こんにちは今日はいい天気ですね。")
