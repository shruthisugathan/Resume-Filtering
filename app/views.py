from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import pickle 



import os, math
import pandas as pd
import numpy as np

from gensim.models import Word2Vec as w2v
from os import path as osp
model = w2v.load('stackexchange_model')

cvs = pd.read_csv('prc_data.csv', sep='\t')
cvs = cvs.set_index('Unnamed: 0')

def get_closest(word, n):
    word = word.lower()
    words = [word]
    similar_vals = [1]
    try:
        similar_list = model.most_similar(positive=[word],topn=n)  
        for tupl in similar_list:
            words.append(tupl[0])
            similar_vals.append(tupl[1])
    except:
        pass
    return words, similar_vals



def mug(prc_description):


    word_value = {}
    similar_words_needed = 2
    for word in prc_description.split():
        similar_words, similarity = get_closest(word, similar_words_needed)
        for i in range(len(similar_words)):
            word_value[similar_words[i]] = word_value.get(similar_words[i], 0)+similarity[i]


    no_of_cv = 150

    count = {}
    idf = {}
    for word in word_value.keys():
        count[word] = 0
        for i in range(no_of_cv):
            try:
                if word in cvs.loc(0)['skill'][i].split() or word in cvs.loc(0)['exp'][i].split():
                    count[word] += 1
            except:
                pass
        if (count[word] == 0):
            count[word] = 1
        idf[word] = math.log(no_of_cv/count[word])



    score = {}
    for i in range(no_of_cv):
        score[i] = 0
        try:
            for word in word_value.keys():
                tf = cvs.loc(0)['skill'][i].split().count(word) + cvs.loc(0)['exp'][i].split().count(word)
                score[i] += word_value[word]*tf*idf[word]
        except:
            pass


    sorted_list = []
    for i in range(no_of_cv):
        sorted_list.append((score[i], i))
        
    sorted_list.sort(reverse = True)

    fg=[]

    for s, i in sorted_list:
        if list(cvs)[i] != '.DS_Store':
            fg.append([list(cvs)[i], ':', s])

    return fg



def home(request):
    if request.method=="POST":

        sentiment=request.POST["sentiment"]
        print(sentiment)

        f=mug(sentiment)

        context = {
        "data" : f,
    }

       

        
        return render(request, 'output.html',context)
        


    return render(request,'home.html')

def output(request):
    return render(request,'output.html')

def voice(request):
    return render(request,'voice.html')




def login(request):
    if request.method=="POST":
        uname=request.POST["uname"]
        password1=request.POST["p_password"]
        u=auth.authenticate(username=uname,password=password1)
        if u is not None:
            auth.login(request,u)
            return redirect(home)
        else:
            dic={'lkey':"invalid login"}
            return render(request,'login.html',dic)
            
    return render(request,'login.html')



def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        mail=request.POST['mail']
        p_password=request.POST['p_password']
        pp_password=request.POST['pp_password']
        if p_password==pp_password:
            if User.objects.filter(username=uname):
                dic={'rkey':"USERNAME ALREADY TAKEN!!"}
                
                return render(request,'register.html',dic)
            elif User.objects.filter(email=mail):
                dic={'rkey':"EMAIL ALREADY TAKEN"}
              
                return render(request,'register.html',dic)
            else:
                
                
                user=User.objects.create_user(username=uname,email=mail,password=p_password,)
                user.save()
                dic={'rkey':"registered successfully!!"}
                return render(request,'register.html',dic)
                
                # return redirect(login)
        else:
            dic={'rkey':"password does not matching"}
            return render(request,'register.html',dic)
    else:
        return render(request,'register.html')
    
    
    



