import math

keywords=["canada"]
doc_data=[]                    # store data of every document
file=open("reuters_cleaned_2.csv","r")

for data in file:
    data=data.replace(","," ")
    data = data.replace('\"', " ")
    data = data.replace(".", " ")
    data =data.replace("/", " ")
    data=data.lower()
    doc_data.append(data)
    words=data.split(" ")
    # words=[word for word in words if len(word)!=0]
    for word in words:
        if word.isalpha():
            if word not in keywords:
                keywords.append(word)

    # if len(doc_data)==10000:
    #     break

print("total words",len(keywords))
print("total documents",len(doc_data))
print("Keywords :",keywords)

tf = [[0.0 for i in range(len(keywords))] for j in range(len(doc_data))]
idf = [[0.0 for i in range(len(keywords))] for j in range(1)]
keyword_count=[[0.0 for i in range(len(keywords))] for j in range(1) ]      # store total ocurrence of each keyword
query="canada"
doc_count=len(doc_data)
#
for row in range(len(doc_data)):          #  create tf matrix
    for col in range(len(keywords)):
        if doc_data[row].count(keywords[col])>0:
            # tf[row][col]=1
            tf[row][col]=doc_data[row].count(keywords[col])
        else:
            tf[row][col] = 0
print("Term Frequency matrix :",tf)
#
for key in range(len(keywords)):         # get occurence of each word in the document
    # print("key",key)
    for col in range(doc_count):
        if tf[col][key]>0:
            # print(col)
            keyword_count[0][key]=keyword_count[0][key]+1

print("Frequency count of each word :",keyword_count)

for i in range(len(keywords)):         # IDF matrix storing idf value of each keyword
    x=doc_count/keyword_count[0][i]
    idf[0][i]=math.log(x,2)

print("IDF table :",idf)

tf_idf = [[0.0 for i in range(len(keywords))] for j in range(len(doc_data))]   # multiply tf with idf value to generate tf_idf
for i in range(len(doc_data)):
    for j in range(len(keywords)):
        tf_idf[i][j]=idf[0][j]*tf[i][j]
#
index=0
for i in range(len(keywords)):
    if keywords[i]==query:
        print("keyword",keywords[i])
        index=i
print("Index of query word",index)
query_matrix=[[0.0 for i in range(len(keywords))] for j in range(1)]

print("idf of query word",idf[0][index])
print("No of documents having the query",keyword_count[0][index])

# Gneretae query matrix uisng the idf value of word in the query
query_matrix[0][index]=(1/keyword_count[0][index])*idf[0][index]
print("Query matrix using idf value and frequency count",query_matrix)

dist_matrix=[[0.0 for i in range(1)] for j in range(doc_count)]
# calculate the distance of each document
for i in range(doc_count):
    sum=0
    for j in range(len(keywords)):
        sum=sum+tf_idf[i][j]**2
    dist_matrix[i][0]=math.sqrt(sum)
print("Distnace matrix of each document",dist_matrix)

sum=0
# calculate the distance of query matrix
for i in range(len(keywords)):
    sum=sum+query_matrix[0][i]**2
query_distance=math.sqrt(sum)
print("Calculate query distance :",query_distance)

# find the coisne value for each document
cosine_values=[]
for i in range(doc_count):
    sum=0
    try:
        for j in range(len(keywords)):
            sum=sum+tf_idf[i][j]*query_matrix[0][j]
        # print(sum)
        cosine_values.append(sum / (dist_matrix[i][0] * query_distance))
    except:
        cosine_values.append(0)

ranked_documents=[doc_data for cosine_values,doc_data in sorted(zip(cosine_values,doc_data),reverse=True)] # rank document based on coisne values
print("cosine similarity between document and query :",cosine_values)
doc_index=cosine_values.index(max(cosine_values)) # index of highest ranked document
print("Index of the highest ranked document :",doc_index, " and its cosine value :",max(cosine_values))
print("Number of times query appeared in the highest ranked document :", ranked_documents[0].count(query))
print("Data in the highest ranked document : \n",ranked_documents[0])