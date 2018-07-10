import numpy as np
import preprop as pp
import os
import psutil

epochs = 50

trainSentences = pp.readfile("train.english.v4_auto_conll")
devSentences = pp.readfile("dev.english.v4_auto_conll")
testSentences = pp.readfile("test.english.v4_gold_conll")
process = psutil.Process(os.getpid())
print(process.memory_info().rss)
