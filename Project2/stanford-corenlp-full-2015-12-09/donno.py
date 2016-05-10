itr = 0
sentiment = {}
reading = True;
with open("lego.review", 'r') as r:
    while reading:
        itr += 1
        sentimen = r.readline().rstrip();
        value = 0
        if sentimen != "  Very positive" and sentimen != "  Very negative" and sentimen != "  Positive" and sentimen != "  Negative" and sentimen != "  Neutral":
            line = r.readline().rstrip()
            if line == "  Positive" or line == "  Negative" or line == "  Neutral" or line == "  Very negative" or line == "  Very positive":
                if line == "  Positive":
                    sentiment[sentimen] = 2
                elif line == "  Negative":
                    sentiment[sentimen] = -0.5
                elif line == "  Neutral":
                    sentiment[sentimen] = 0
                elif line == "  Very negative":
                    sentiment[sentimen] = -1
                else:
                    sentiment[sentimen] = 3
       #         else:
  #                  print "ERROR!", line
      #      else:
 #               print "ERROR!", sentimen
#                sentiment[sentimen] = line
        if sentimen.rstrip() == "I tought it would be good to post it here if somone else want to do the same...":
            reading = False
#        print itr
#print len(sentiment)

with open("../lego.txt", 'r') as f:
    reviews = f.readlines()

keys = list(sentiment.keys())

final = []
#print len(reviews)
for review in reviews:
    value = []
    for key in keys:
        if key in review:
            value.append(sentiment[key])
    if len(value) > 0:
        v = sum(value)/len(value)
        if v > 0.1:
            v = 1
        elif v < -0.3:
            v = -1
        else:
            v = 0
        final.append(v)
    else:
        final.append(0)
with open("outs", 'w') as f:
    for send in final:
#    for rev, send in zip(reviews, final):
        f.write(str(send) + "\n")#) + ", " + str(rev))
#print final, len(final)
#    else:
#        it += 1
#        line.rstrip() == "  Positive" or line.rstrip() == "  Negative" or line.rstrip() == "  Neutral":
#    sentiment[''] = 4127
#    line = r.readline()
#    with open("../lego.txt", 'r') as f:
#        reviews = f.readlines()
#        print reviews[0]
#        print str(line).rstrip() in str(reviews[0])
#    for review in reviews:
#        itr += 1
#        while str(line).rstrip() in str(review):
#            print "."
#            line=r.readline()
#            if line.rstrip() == "  Positive" or line.rstrip() == "  Negative" or line.rstrip() == "  Neutral":
"""                line=r.readline()
            else:
                print "",
        #        print line
        print " -- ",
    print itr"""