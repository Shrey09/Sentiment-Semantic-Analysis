import csv
import re

from langdetect import detect

tweet=[] #store raw tweets
tweets=[] # store cleaned tweets
f1=open("positive-words.txt","r") #dictionary of positive words
f2=open("negative-words.txt","r") #dictionary of negative words
f3=open("stop-words.txt","r")     #dictionary of stop-words

pos=f1.read()
pos=pos.split("\n")
neg=f2.read()
neg=neg.split("\n")
stopwords=f3.read()
stopwords=stopwords.split("\n")
print("positive dictionary :",pos)
print("negative dictionary :",neg)
print("stopwords dictionary :",stopwords)

with open('stream.csv', 'r') as csvFile: #read tweets
    reader = csv.reader(csvFile)
    for row in reader:
        if len(row)!=0:
            try:
                language=detect(row[3]) #consider only text from the tweets i.e row[3]
                # print(b)
                if language=="en":     # consider only english tweets
                    # print(row[3])
                    tweet.append(row[3])
                    row = re.sub(r"[^a-zA-Z0-9]+", ' ', row[3])  #reomve sepcial characters
                    row=row.replace("rt"," ")  #remove rt from the tweets
                    tweets.append(row)
            except:
                pass


print("Raw tweets\n",tweet)
print("Cleaned tweets \n",tweets)

words=[]
for i in tweets:
    # generate tokens by splitting tweets into words
    tokens=i.split(" ")
    tokens=[token for token in tokens if len(token)!=0]
    words.append(tokens)

print("Tokenising tweets \n",words)
no_stopwords=[]
temp=[]

for i in words:         #remove stopwords from tweets
    for j in i:
        if j not in stopwords:
            temp.append(j)
    no_stopwords.append(temp)
    temp=[]
print("Removed the stopwords\n",no_stopwords)

count=0
tweet_polarity=[]
positive=0
negative=0
neutral=0
# determine polarity of tweets
for twt in no_stopwords:
    pos_count=0
    neg_count=0
    polarity=""
    temp=[]
    for word in twt:
        if word in pos:
            pos_count+=1
        if word in neg:
            neg_count+=1
    if pos_count>neg_count:
        polarity="positive"
        positive+=1
    elif neg_count>pos_count:
        polarity="negative"
        negative+=1
    else:
        polarity="neutral"
        neutral+=1
    temp.append(tweets[count])
    temp.append(polarity)
    tweet_polarity.append(temp)
    with open("tweet_sentiment.csv","a+",newline='') as csvFile:
        columns=["Tweets","Polarity"]
        writer=csv.DictWriter(csvFile,fieldnames=columns)
        Dict={"Tweets":tweets[count],"Polarity":polarity}
        writer.writerow(Dict)
    count+=1

print("Total tweets :",count)
print("Tweets with polarity \n",tweet_polarity)
print("Total Positive Tweets :",positive)
print("Total Negative Tweets :",negative)
print("Total Neutral Tweets :",neutral)