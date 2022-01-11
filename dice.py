from modelo.DocProcessing import DocProcessing

def dice_coefficient(a, b):
    #dice coefficient 2nt/(na + nb)
    #example of biagram --> night = ni ig gh ht (4 bigrams)
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a=a+u'.'
    if len(b) == 1:  b=b+u'.'
    
    a_bigram_list=[] 
    for i in range(len(a)-1):
      a_bigram_list.append(a[i:i+2])
    b_bigram_list=[]
    for i in range(len(b)-1):
      b_bigram_list.append(b[i:i+2])
      
    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0/(len(a_bigrams) + len(b_bigrams))
    return dice_coeff

#more precise duplicate bigrams in a word should be counted distinctly
def dice_coefficient_v2(a,b): 
    if not len(a) or not len(b): 
        return 0.0
    if a == b: # quick case for true duplicates
        return 1.0
    if len(a) == 1 or len(b) == 1: 
        return 0.0 # if a != b, and a or b are single chars, then they can't possibly match 
    
    a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
    b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
    
    a_bigram_list.sort()
    b_bigram_list.sort()
    
    # assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)
    # initialize match counters
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1

    #dice coefficient --> 2nt/(na + nb)
    score = float(matches)/float(lena + lenb) #apply the formula
    return score

#Proof of the why the second one is better
var1 = dice_coefficient("AA","AAAA")
var2 = dice_coefficient_v2("AA","AAAA")

print(var1) # 1.0
print(var2) # 0.5 more accurate


'''####################################################'''
def recomendation_tags(id):
        #start de recomendation
        tags = process.docs_tags #Nos descargamos los tags
        reco = [] #Creamos la lista de resultados
        n = 0 #Contador favorito
        while n != len(tags):
            #print("Tags a comparar : ",tags[id])
            #print("Tag cambia      : ",tags[n])
            #print(n)
            var = dice_coefficient_v2(tags[id],tags[n])
            #print(n,": ",var)
            if n == id:
                var = -1 #so it does not recommend itself
            reco.append(var)
            n=n+1
        return reco 




import time
inicio = time.time()
process = DocProcessing()
reco = recomendation_tags(2)
print(reco)

fin = time.time()
print(fin-inicio, "secs")