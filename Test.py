
# coding: utf-8

# # Introduction to the Script.
# v1 of this script was written by Saurav Kumar (skumar2@utep.edu) to prepare finals for the CE2385 class in Fall of 2016.
# In a nutshell, the script reads two columns from an excel sheet ("Question_text" and "Key") and uses them to prepare several unique (possibly one for each student) multiple choice question set and answer key.
# 
# ## The input excel sheet
# In the question_text column, the text for the question is written. The numerical or text values that may be randomly chosen are marked by {} (see example). **The order of {} is important** (do not worry, it will become clear later what do I mean by this statement). 
# 
# The key defines how to fill the {} and compute answers.There are two types of keys 
# 1) No computation keys. Where all the options and answer are given and the script does not have to compute the answer. These are the simpler of the two types.
# 2) Computation keys. They have the power to evaluate expressions. Expression have to be in Python lingo see https://en.wikibooks.org/wiki/Python_Programming/Basic_Mathhttps://en.wikibooks.org/wiki/Python_Programming/Basic_Math, https://docs.python.org/3/library/math.html
# 
# 
# Lets look at some examples to illustrate keys and the question_text
# 
# **Sr #**|**Question\_text**|**Key**
# :-----:|:-----:|:-----:
# 1|`On a clear day, a scientist noted that the atmospheric stability condition is {}. Nearby, from a stack {}m high (h) a contaminant plume was observed to be rising another 15m (∆h). In these conditions, how far on the ground directly downwind from the stack should the scientist place his air quality measurement equipment to get maximum pollutant reading? Pick the closest answer from the following.`|`{[["A",85,0.4], ["B",85,0.7], ["C",85,1], ["D",85,3], ["A",55,0.3], ["B",55,0.5], ["C",55,0.8], ["D",55,2]]} Km`
# 2|`If the environmental lapse rate is {} than dry adiabatic lapse rate, then the atmosphere is ______ `|`{[["less ( Γenv < Γad )","stable"],["greater ( Γenv > Γad )","unstable"]]}`
# 3|`Express {} ppmv of Nitric Oxide (NO) in mg/m³ at 25C.`|`{{"a":[10,30,40,50,60,70,80,90,100,200], "ANSWER":"30/22.414*273.15/298.15*{a}"}} mg/m³`
# 4|`Some waste has a 5 day BOD at 20C equal to {} mg/L and an ultimate BOD of {} mg/L. Find the 5 day BOD at 25C.`|`{{"a":[200,210,220], "b":[400,375,425],"ANSWER":"{b} *(1-math.e**(-k_t*5))","STATEMENT":"k_t = -1/5*math.log(({b}-{a})/{b})*1.047**5","ROUND":2}} mg/L`
# 5|`A factory continuously releases a carcinogen X with a potency factor of 0.30 (mg/kg-day)⁻¹ in a stream flowing at a rate of 1 mph. The in-stream concentration of X at point of release is {}. The carcinogen also decays with at a rate of 0.10/day. {} miles downstream a family uses this stream as water supply for drinking water. What is the risk to an adult member of the family due to this water supply? Assume that the only transformation for the carcinogen is the in-stream decay. `|`{{"a":[0.2,0.3,0.4,0.5],"b":[100,125,150],"ANSWER":"_cdi*0.30","STATEMENT_t={b}/24;_c={a}*math.e**(-0.10*_t);_cdi=_c*2*360*30/70/365/70","ROUND":6}} `
# 
# Examples 1 and 2 are 'No computation' type problems. Note the key format, it is akin to creating an *array or array* or a *list of list* enclosed in curly braces. Anything outside the curly braces (usually units) is be reproduced directly on all answers. Each list is the *list of **list*** (enclosed lists) represents a set of options (numbers to fill and respective answer). The last element in the option set is always the answer. Other elements in the option set (**in order**) are used to fill the "{}" in the corresponding question. This is how the algorithm works:
# 1. Randomly pick the desired number of options(5) from the list of list (chosen list of list). If there are not enough pick them all.
# 2. From chosen list of list, pick one and crown it the correct answer.
# 3. Use the data in the correct answer list to fill {} in the question text. The first {} is filled by the first element, second {} by the second element and so on... The last element in the list is the answer.
# 
# Examples 3,4,5 have 'Computation Keys'. These are more powerful and have more options. Lets look at the example 5 to understand this key. The question in example 5, like earlier, has {} to be filled. Unlike 'no computation keys' here the lists with possible values to fill are labeled with characters a and b (python speak--> we are creating a dict; map for Java guys). The values in 'a' will be used to fill the first {}, 'b' the second {} and so on... Besides characters we have there reserved keywords "STATEMENT", "ANSWER", and "ROUND". Providing an ANSWER is required. In the ANSWER you can use pythonic math to describe how to compute answers using chosen variables from list a,b and more if present. "STATEMENT" is not required, but it makes writing formula to compute ANSWER easier. STATEMENT is executed before ANSWER, so the variables created in the STATEMENT are available in ANSWER. In our example 5 \_cdi is created in STATEMENT and used in ANSWER (python way of saying raise to power is \*\* not ^); also note that \_cdi itself uses \_c created before \_cdi in the STATEMENT. "ROUND" decides how many decimals to display, it defaults to 2. Note that ROUND is also used for "close check" described later. 
# This is how the algorithm works:
# 1. Make list of all possible combinations. IN example 5 that will be 12 combinations. It we had a c number of combinations will further increase.
# 2. Compute answers for all combinations based and create a list of list (not literally) as earlier
# 2. Randomly pick the desired number of options(5) from the list of list (chosen list of list). If there are not enough pick them all.
# 3. From chosen list of list, pick one and crown it the correct answer.
# 4. Use the data in the correct answer list to fill {} in the question text. The first {} is filled by the first element, second {} by the second element and so on... The last element in the list is the answer.
# 
# 
# ## Software requirements
# 1. Python 3x
# 2. Free, pandas and itertools python packages (pip may install these packages)
# 
# 
# If you have any inclination to use python more that for this script install anaconda (see https://www.continuum.io/downloads). Remember v3 installer for your system   
#     
#     
# ## Similar options test... the thing that fails!!
# If several of your variables yield same or similar answerers. There is a possibility in random picking (without replacement) that multiple options may be similar or same (e.g. A, B options have same answers). The script tries to address this problem by using two variables CLOSE_CHECK and CLOSE_CHECK_SKIP. This is used **only** for 'computation keys'; for 'no computation key' it is assumed you are smart not to create a pool with answers that are too close.
# 
# ### Check method
# The difference between all possible option pairs should be greater that the CLOSE_CHECK to be valid. Note that decimal are converted to the whole number by multiplying by $10^{ROUND}$. **If there are not enough viable options the script will enter an infinite loop**. To get out of this press ctrl+c to break script and turn DEBUG = True (if False... I always keep it True) and see which question is messing up and change accordingly.
# 
# If for some reason some question/questions cannot fit the CLOSE_CHECK algorithm (it is a quick and dirty algorithm) and you are happy with the options generated for those questions, put these questions in the CLOSE_CHECK_SKIP list, to avoid any infinite loops.
# 
# 
# ## TIPS and Notes
# * The script generates a text file (no tabs, bolds, formatting etc.), UTF8 so ensure that proper character set is in use. Subscripts and superscripts have to be UTF8 https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts. Maybe in a future version will implement MS Word or HTML formatting. Changing formatting will help to embed figures too.
# * Before printing, make sure the text editor you are printing from has the **same font** that was used to generate questions in excel. 
# * Some page formatting in needed in the generated text file with exam questions. I found it useful to open them in MS Word and then apply page breaks as necessary.
# 
# ## Coming in version 2
# * Handle MS Word/Excel formatting
# * Formatted and properly paged outputs
# * HTML renderer with a server to automate grading 
# 

# In[6]:

MAX_OPTIONS=5 # Max 5 options to be picked. Note it is possible that the options are less than this value, then all possible options will be picked 
OPTIONS = ["A","B","C","D","E"] # What to label the options
MASTER_XLSX=r"C:\Users\saurav\sauravk@vt.edu\Classes\Intro to EE\UTEP-CE 2385\Finals\master_q.xlsx"
FOLDER = r"C:\Users\saurav\sauravk@vt.edu\Classes\Intro to EE\UTEP-CE 2385\Finals"
SET=10 # sets of questions to create
RAND_SEED = 6 # initial seed for randomness.
DEBUG = True # outputs all options for each question and other info. 

CLOSE_CHECK= 5 # do not pick alternatives if in solutions are within this range. Essentially for all pairs of options difference
# is computed and multiplied by 10**(ROUND) if the number is less than close_check then it is too close and not chosen.Note 
# if there are not enough viable options this will hang the program :(.. TODO: Hang check...
CLOSE_CHECK_SKIP=[36] #skip close test on these questions. indexed form 1

SHUFFLE_QUESTIONS= True # shuffle questions order

INITIAL_TEXT= '''

CE 2385 - Environmental Engineering Fundamentals
Fall 2016
EXAM CODE {}{}
EXAM DURATION 7:00 - 9:45 AM

Name__________________ Email ID ________________  Reef ID _______________ 

Instructions
1) All 50 questions are 1 point. The maximum score is thus 50 points. 
2) Answer all questions.
3) No extra time will be given. At the end of the exam or when you finish please return your question book with answers marked, cheat sheet, and any other document provided.
4) This is a closed book exam. You are allowed to bring a cheat sheet that will be collected at the end of the exam. Cheat sheet will not be graded.
5) Only a calculator is allowed. POSSESSION OF PHONES, COMPUTERS OR ANY OTHER ELECTRONIC COMMUNICATION DEVICE(S) IS NOT ALLOWED.
6) A list of equations and tables is provided.

BEST OF LUCK!

------------------------------------SIGN BELOW AFTER FINISHING------------------------------------
I have neither given nor received unauthorized aid on this examination. Furthermore, I swear that I have not committed any form of academic dishonesty, on witnessed anyone commits academic dishonesty during the exam. 

Signature: ___________________________ Date: ___________________     
'''


# In[7]:

import pandas as pd
import random
import re
import itertools as it
import math # needed for log etc
random.seed(RAND_SEED)


# In[10]:

master_questions=pd.read_excel(MASTER_XLSX)
def execution_seq(x,k):# called in loop to generate answers
    #print(x,k)
    if "STATEMENT" in k.keys():
        exec(k["STATEMENT"].format(**x))
    return(eval(k["ANSWER"].format(**x)))


def close_test(df, qno, round_no):# returns true if too close 
    if qno+1 in CLOSE_CHECK_SKIP:
        return False
    combi = list(it.combinations(df["ANSWER"].tolist(),2))
    df_c = pd.DataFrame(combi)
    check_val = min(abs ((df_c[1]-df_c[0])))*10**round_no
#     if check_val > CLOSE_CHECK_LIMIT:
#         return False
#     return  min(abs ((df_c[1]-df_c[0])/df_c.min(axis=1))) < CLOSE_CHECK 
    return check_val < CLOSE_CHECK
    
for i in range(SET):
    final_questions = pd.DataFrame(columns= ["Questions","Solution key"])
    save_file="exam{}".format(i)
    for index, row in master_questions.iterrows():
        #print(row[3])
        keys_js=re.search(r'{(.*)}', row[3]).group(1) # everything between curly brackets
        option_template_units = re.sub(r'{(.*)}',"{}",row[3])
        #print (option_template_units)
        #print(keys_js)
        k = eval(keys_js)
        decimals = 0
        if type(k) is dict: # dict datatype means that the answeres have to be computed
            l = list(k.keys()) # keys in the dict ... should we a,b,c... in order and finally ANSWER
            l.remove('ANSWER') # remove answer
            if "ROUND" in l:
                l.remove('ROUND') # remove rounding 
            if "STATEMENT" in l:
                l.remove('STATEMENT')
            l.sort() # get the order back
            combinations = list(it.product(*(k[Name] for Name in l))) # get all combinations
            df=pd.DataFrame(data=combinations)
            df.columns=l # put column names back
            decimals = k.get("ROUND",2) 

            df["ANSWER"]=df.apply(lambda x:execution_seq(x,k),axis=1).round(decimals) # evaluate the expression 
        else:
            df=pd.DataFrame(data=eval(keys_js))# read keys in a dataframe
            
        if DEBUG:
            print ("Question : {}".format(index+1))
            print (df)
            print ("Sorted")
            print (df.sort_values(by=df.columns[len(df.columns)-1]))
        
        close_check_bit = True
        while close_check_bit:
#             print(close_check_bit)
#             print (type(k))
            if df.shape[0] > MAX_OPTIONS:
                chosen = random.sample(list(df.index),MAX_OPTIONS) # randomly choose MAX_OPTIONS (5) keys
            else:
                chosen = list(df.index)  # if less than 5 (MAX_OPTION) use all keys 
            
            if type(k) is dict:
                close_check_bit = close_test(df.ix[chosen],index,decimals)
            else:
                close_check_bit = False
        
                    
        random.shuffle(chosen) # shuffle chosen keys... necessary if number of options = max_options
        #print(chosen)
        correct_index = random.randrange(0,len(chosen)) # among the chosen pick one as correct index
        correct=chosen[correct_index] # filter the correct option
        #print(correct)
        question = row[2].format(*list(df.ix[correct,:])) # use correct option to fill in
        #print(question)
        options = df.ix[chosen,df.shape[1]-1] # filtering chosen options to present as possible answers
        options = options.apply(lambda x:option_template_units.format(x)) # applying units etc.
        option_labels = dict(zip(options.index,OPTIONS[0:len(chosen)])) # mapping ABCDE labels to indexes
        #print(option_labels)
        options.rename(option_labels, inplace=True)
        q_text=question +"\n"+options.to_string()
        #print(q_text)
        #print("correct {} {}".format(OPTIONS[correct_index],df.ix[correct,df.shape[1]-1]))
        if DEBUG:
            print ("Chosen Options")
            print (df.ix[chosen])
            print ("Correct")
            print (df.ix[correct])
            
        correct_option="{}: {}".format(OPTIONS[correct_index],df.ix[correct,df.shape[1]-1])
        t_data= [q_text,correct_option]  
        temp_q = dict(zip( ["Questions","Solution key"],t_data))
        final_questions=final_questions.append(temp_q,ignore_index=True)
    # print final questions 
    # shuffle questions
    if SHUFFLE_QUESTIONS:
        final_questions = final_questions.ix[random.sample(list(final_questions.index),len(final_questions.index)),:]

    # write files
    count = 0
    with open(FOLDER+"\\"+save_file+".txt", 'w',encoding='utf-8') as exam, open(FOLDER+"\\"+save_file+"key.txt","w",encoding='utf-8') as key:
        exam.write(INITIAL_TEXT.format(i,'-'.join(random.choice('0123456789ABCDEF') for i in range(16))))
        key.write("*************CODE{}\n\n\n".format(i))
        for index, row in final_questions.iterrows():
            exam.write("Question {}".format(count+1))
            exam.write("\n")
            exam.write(row[0])
            exam.write("\n"*3)
            key.write("Question {}  {}\n".format(count+1,row[1]))
            count+=1   


# In[11]:

"DONE"

