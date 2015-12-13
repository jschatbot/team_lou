# -*- coding: utf-8 -*-

import chatapi
import random

capi = chatapi.ChatbotAPI()

if capi.isLocal == False:
    import twitter_lm
    lm = twitter_lm.twitter_lm()

th_num = 10 # 候補数がいくつ以下ならマルコフ連鎖を考えるか

# ランダムで応答文を選ぶ
def choiceReply_Random(replylist):
        return random.choice(replylist)

# 言語モデルで応答文を評価
def choiceReply_withLM(replylist):
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
                        for i in range(0, 10):
                            malkovs = capi.generateMarkov(surface=morph[u"surface"], pos=morph[u"pos"])
                            str = ""
                            for mal in malkovs:
                                    str += mal.split(":")[0].rstrip('"')
                            malkovlist.append(str.lstrip("BOS").rstrip("EOS"))
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
        markov_used = False

        # チャンキング結果から用例を検索
        replylist = exampleBasedReply(capi.getChunks(replytext))

        if len(replylist) < th_num:
                replylist += generateMarkovReply(replytext)
                markov_used = True 

        if len(replylist) == 0: # 返答文が作れなかった
                replylist = [u"分からないぞ？",u"もう一回"] # 辞書読み込む or ~って何?
                reply = random.choice(replylist)
        elif markov_used and capi.isLocal == False:
                reply = choiceReply_withLM(replylist)
        else:
                reply = choiceReply_Random(replylist)

#        print reply
        return reply

#generateReply("こんにちは今日はいい天気ですね。")
