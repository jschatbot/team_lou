# -*- coding: utf-8 -*-

import chatapi
import random
import twitter_lm

capi = chatapi.ChatbotAPI()
lm = twitter_lm.twitter_lm()
th_num = 100 # 候補数がいくつ以下ならマルコフ連鎖を考えるか

# 言語モデルで応答文を評価
def choiceReply(replylist):
        ans = ("", -10000)
        for line in replylist:
            morphs = capi.getMorphs(line)
            tok_line = ""
            for morph in morphs:
                if morph["surface"] != "BOS" and morph["surface"] != "EOS":
                    tok_line += morph["surface"] + " "
            score = lm.calc_score(tok_line)
            if score > ans[1]:
                ans = (line, lm.calc_score(tok_line))

        return ans[0]

# マルコフ連鎖で応答文を生成
def generateMarkovReply(replytext):
        morphs = capi.getMorphs(replytext)
        keypos = [u"一般名詞", u"固有一般", u"固有人性", u"固有人名", u"固有人他", u"固有地名", u"固有組織", u"固有賞品"]

        malkovlist = []
        for morph in morphs:
                if morph[u"pos"] in keypos:
                        malkovs = capi.generateMarkov(surface=morph[u"surface"], pos=morph[u"pos"])
                        str = ""
                        for mal in malkovs:
                                str += mal.split(":")[0].rstrip('"')
                        malkovlist.append(str)
        return malkovlist

def exampleBasedReply(chunks):
        examplelist = []
        for words in chunks:
                norm = words["norm_surface"]
                examples = capi.searchReply(norm,limit=10) # 10?
                examplelist += examples[u"texts"]
        return examplelist

# リプライの姿勢
def generateReply(replytext):
        # チャンキング結果から用例を検索
        replylist = exampleBasedReply(capi.getChunks(replytext))

        if len(replylist) < th_num:
                replylist += generateMarkovReply(replytext)

        if len(replylist) == 0: # 返答文が作れなかった
                replylist = [u"分からないぞ？",u"もう一回"] # 辞書読み込む or ~って何?
                reply = random.choice(replylist)
        else:
                reply = choiceReply(replylist)

#        print reply
        return reply

#generateReply("こんにちは今日はいい天気ですね。")
