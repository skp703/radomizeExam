# radomizeExam
# Introduction to the Script.
v1 of this script was written by Saurav Kumar (skumar2@utep.edu or kumar.saurav@gmail.com) to prepare finals for the CE2385 class in Fall of 2016.

In a nutshell, the script reads two columns from an excel sheet ("Question_text" and "Key") and uses them to prepare several unique (possibly one for each student) multiple choice question set and answer key.

## The input excel sheet
In the "question_text" column, the text for the question is written. The numerical or text values that may be randomly chosen are marked by {} (see example). **The order of {} is important** (do not worry, it will become clear later what do I mean by this statement). 

The key defines how to fill the {} and compute answers.There are two types of keys 
1) No computation keys. Where all the options and answer are hardcoded and the script does not have to compute the answer. These are the simpler of the two types.
2) Computation keys. They have the power to evaluate expressions. Expression have to be in Python lingo see https://en.wikibooks.org/wiki/Python_Programming/Basic_Mathhttps://en.wikibooks.org/wiki/Python_Programming/Basic_Math, https://docs.python.org/3/library/math.html


Lets look at some examples to illustrate keys and the question_text

**Sr #**|**Question\_text**|**Key**
:-----:|:-----:|:-----:
1|`On a clear day, a scientist noted that the atmospheric stability condition is {}. Nearby, from a stack {}m high (h) a contaminant plume was observed to be rising another 15m (∆h). In these conditions, how far on the ground directly downwind from the stack should the scientist place his air quality measurement equipment to get maximum pollutant reading? Pick the closest answer from the following.`|`{[["A",85,0.4], ["B",85,0.7], ["C",85,1], ["D",85,3], ["A",55,0.3], ["B",55,0.5], ["C",55,0.8], ["D",55,2]]} Km`
2|`If the environmental lapse rate is {} than dry adiabatic lapse rate, then the atmosphere is ______ `|`{[["less ( Γenv < Γad )","stable"],["greater ( Γenv > Γad )","unstable"]]}`
3|`Express {} ppmv of Nitric Oxide (NO) in mg/m³ at 25C.`|`{{"a":[10,30,40,50,60,70,80,90,100,200], "ANSWER":"30/22.414*273.15/298.15*{a}"}} mg/m³`
4|`Some waste has a 5 day BOD at 20C equal to {} mg/L and an ultimate BOD of {} mg/L. Find the 5 day BOD at 25C.`|`{{"a":[200,210,220], "b":[400,375,425],"ANSWER":"{b} *(1-math.e**(-k_t*5))","STATEMENT":"k_t = -1/5*math.log(({b}-{a})/{b})*1.047**5","ROUND":2}} mg/L`
5|`A factory continuously releases a carcinogen X with a potency factor of 0.30 (mg/kg-day)⁻¹ in a stream flowing at a rate of 1 mph. The in-stream concentration of X at point of release is {}. The carcinogen also decays with at a rate of 0.10/day. {} miles downstream a family uses this stream as water supply for drinking water. What is the risk to an adult member of the family due to this water supply? Assume that the only transformation for the carcinogen is the in-stream decay. `|`{{"a":[0.2,0.3,0.4,0.5],"b":[100,125,150],"ANSWER":"_cdi*0.30","STATEMENT_t={b}/24;_c={a}*math.e**(-0.10*_t);_cdi=_c*2*360*30/70/365/70","ROUND":6}} `

Examples 1 and 2 are 'No computation' type problems. Note the key format; it is akin to creating an *array or array* or a *list of list* enclosed in curly braces. Anything outside the curly braces (usually units) is reproduced directly on all answers. Each list in the *list of **list*** (enclosed lists) represents a set of options (numbers to fill and respective answer). The last element in the option set is always the answer. Other elements in the option set (**in order**) are used to fill the "{}" in the corresponding question. This is how the algorithm works:
1. Randomly pick the desired number of options(5) from the list of list (now called the *chosen list of list*). If there are not enough pick them all.
2. From the *chosen list of list*, pick one and crown it the correct answer.
3. Use the data in the correct answer list to fill {} in the question text. The first {} is filled by the first element, second {} by the second element and so on... The last element in the list is the answer.
4. Shuffled answers from the *chosen list of list* makeup the multiple choices to pick from. 

Examples 3,4,5 have 'Computation Keys'. These are more powerful and have more options. Lets look at the example 5 to understand this key. The question in example 5, like earlier, has {} to be filled. Unlike 'no computation keys' here the lists with possible values to fill are labeled with characters a and b (python speak--> we are creating a dict; map for Java guys). The values in 'a' will be used to fill the first {}, 'b' the second {} and so on... Besides characters we have reserved keywords "STATEMENT", "ANSWER", and "ROUND". Providing an ANSWER is required. In the ANSWER you can use pythonic math (see https://en.wikibooks.org/wiki/Python_Programming/Basic_Mathhttps://en.wikibooks.org/wiki/Python_Programming/Basic_Math, https://docs.python.org/3/library/math.html) to describe how to compute answers using chosen variables from list a,b and more if present. "STATEMENT" is not required, but it makes writing formula to compute ANSWER easier. STATEMENT is executed before ANSWER, so the variables created in the STATEMENT are available in ANSWER. In our example 5 \_cdi is created in STATEMENT and used in ANSWER (python way of saying raise to power is \*\* not ^); also note that \_cdi itself uses \_c created before \_cdi in the STATEMENT. "ROUND" decides how many decimals to display, it defaults to 2. Note that ROUND is also used for "close check" described later. 
This is how the algorithm works:
1. Make list of all possible combinations. In example 5 that will be 12 combinations. If we had a c number of combinations will further increase.
2. Compute answers for all combinations based on STATEMENT and ANSWER and create a list of list (not literally) as earlier.
3. Randomly pick the desired number of options(5) from the list of list (now called the *chosen list of list*). If there are not enough pick them all.
4. From the *chosen list of list*, pick one and crown it the correct answer.
5. Use the data in the correct answer list to fill {} in the question text. The first {} is filled by the first element, second {} by the second element and so on... The last element in the list is the answer.
6. Shuffled answers from the *chosen list of list* makeup the multiple choices to pick from. 

## Software requirements
1. Python 3x
2. Free, pandas and itertools python packages (pip may install these packages)


If you have any inclination to use python more that for this script or want to take the simple route just **install anaconda** (see https://www.continuum.io/downloads). Remember v3 installer for your system   
    
    
## Similar options test... the thing that fails!!
If several of your variables/options yield same or similar answers. There is a possibility in random picking (without replacement) that multiple options may be similar or same (e.g. A, B options have same answers). The script tries to address this problem by using two variables CLOSE_CHECK and CLOSE_CHECK_SKIP. This is used **only** for 'computation keys'; for 'no computation key' it is assumed you are smart not to create a pool with answers that are too close.

### Check method
The difference between all possible option pairs should be greater that the CLOSE_CHECK to be valid. Note that decimal are converted to the whole number by multiplying by $10^{ROUND}$. **If there are not enough viable options the script will enter an infinite loop**. To get out of this press ctrl+c to break script and turn DEBUG = True (if False... I always keep it True) and see which question is messing up and change accordingly.

If for some reason some question/questions cannot fit the CLOSE_CHECK algorithm (it is a quick and dirty algorithm) and you are happy with the options generated for those questions, put these question numbers in the CLOSE_CHECK_SKIP list, to avoid any infinite loops.


## TIPS and Notes
* The script generates a text file (no tabs, bolds, formatting etc.), UTF8 so ensure that proper character set is in use. Subscripts and superscripts have to be UTF8 https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts. Maybe in a future version will implement MS Word or HTML formatting. Changing formatting will help to embed figures too.
* Before printing, make sure the text editor you are printing from has the **same font** that was used to generate questions in excel. 
* Some page formatting in needed in the generated text file with exam questions. I found it useful to open them in MS Word and then apply page breaks as necessary.

## Coming in version 2
* MS Word/Excel formatting handling with output in EXCEL. Will get rid of the UTF8 character encoding issues.
* Formatted and properly paged outputs.
* HTML renderer with a built in server to automate grading.
