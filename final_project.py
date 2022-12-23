#Daria Gogonea
#final_project.py

#This experiment is testing the participant's verbal and problem-solving skills by testing how fast the participant can recognize what words are and what words are not anagrams of the word LISTEN. Participants go through 2 blocks and in each block there are two trials where they are presented a list of 10 words and they have to press either "y" (word is an anagram) 
#or "n" (word is not an anagram). The list of the 10 words is randomized at the start of each trial, so the words are not shown in the same order and the words are also not repeated during a trial. This might also be testing short term memory or the ability to remember/recognize patterns. Becuase the participants see the same 10 words all 4 trials, they might remember which words are anagrams and 
#which words are not, which might affect their reaction times as the trials proceed.

#In the list, 5 words are anagrams of the word LISTEN and 5 words are not anagrams. These words that are not anagrams are either missing letters that belong in the word LISTEN or the words contain letters that do not belong in the word. The reaction time and the accuracy of the participant is recorded. The words stay up on the screen until a keypress is performed by the participant and then a new word is shown instantly.
#Between the trials, there is a short moment where a fixation cross is shown and the cross then is replaced by a word when the trial starts. 

#I want to note here that the reason I only have 2 trials is because when the program goes through the list and displayed all the values, that is only counted as one trial. If I were to do 10 trials, that would mean that the participant would have to go through the list of words 20 times. This would be highly redundant and unnecessary, so I decided that 2 trials in each block is enough to gather a significant amount of data. 

#NOTE: I'm not sure why, only a folder "dataFiles" is being created but no data is being stored in the folder in .csv form. I can't upload an example document becuase I keep getting a "FileNotFoundError: [Errno 2] No such file or directory:" error but I'm not sure why my code isn't working for the data storing part.

#=====================
#IMPORT MODULES
#=====================
#importing several functions that will be necessary to use in the coding and will also be helpful. These functions help with saving files, creating dialogue boxes, randomizing, etc.
import numpy as np
import random
from psychopy import core, gui, visual, event, monitors, logging
import csv
import json
import pandas as pd
import os
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
main_dir = os.getcwd() #defining the main dictionary
print(main_dir) #print the main dictionary
path = os.path.join(main_dir, 'dataFiles') #defining dictionary where the data will be stored/saved
if not os.path.exists(path): #creating the path if it does not exist
   os.makedirs(path, exist_ok=True)
   
#=====================
#COLLECT PARTICIPANT INFO
#=====================
#creating a dialogue box that collects information from the participant; it will collect data on whether or not consent was given, age, number, gender, and handedness
exp_info = {'subject number': '',
            'consent given': ('yes','no'), #creates drop-down menu
            'age': '',
            'gender': ('female','male','prefer not to say'), #creates drop-down menu
            'handedness': ('right', 'left', 'ambi') #creates drop-down menu
            }
print(exp_info)

my_dlg = gui.DlgFromDict(dictionary=exp_info, 
                    title ="subject info",
                    order =['consent given', 'subject number', 'age', 'gender', 'handedness'])

#collect the data and the time of when the participant does the experiment
date = datetime.now()
exp_info['date']=str(date.day) + '/' + str(date.month) + '/' + str(date.year)
print(exp_info['date'])

#create a unique name for the file where the data will be saved
filename = str(exp_info['subject number']) + '_' + exp_info['date'] + '.csv'
print(filename)
main_dir = os.getcwd()

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
#set up the number of trials and blocks in the experiment
nTrials = 2
nBlocks = 2
totalTrials = nTrials*nBlocks #accounts for how many trials there will be in total (4)
#nEach = int(totalTrials/2) #division of the 4 trials by the blocks, which will give 2 trials

#creation of the two lists; the first one contains 5 words that are anagrams and the second one contains 5 words that are not anagrams
anagrams = ['elints', 'enlist', 'inlets', 'silent', 'tinsel']
non_anagrams = ['lister', 'linear', 'instal', 'nitres', 'entoil']

#combining the above two lists to make one list of 10 words that will be the stimuli in this experiment 
stimuli = anagrams + non_anagrams
np.random.shuffle(stimuli) #randomizing the order of the 10 words
print(stimuli)

text_coords = [0,0] #the words will be displayed in the center of the screen 

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
#creating empty lists that will be used for data collection once the experiment starts; there are 4 trials where 10 words are displayed so 40 items will be added in total to these lists
accuracy = [0]*totalTrials
responseTimes = [0]*totalTrials
trialNumbers = [0]*totalTrials
blockNumbers = [0]*totalTrials

#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
#using psychopy function (monitors) that defines the monitor settings
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1600,900]) #set resolution of monitor 

win = visual.Window(monitor=mon, size = (600,600), color = 'grey', units = 'pix') #define window settings

start_msg = "Welcome to the experiment. Please press any key to continue." #first message displayed that welcomes participant 
#The message below contains all the information/instructions that the participant needs to perform the experiment 
instruct_msg = "Please read the following instructions. \n \n An anagram is a word that can be formed by rearranging the letters of another word. In this experiment, you will be presented with a series of words. Your task is to decide as quickly and accurately as possible whether each word on the screen is an anagram of the word 'LISTEN'. \n \n Press the 'y' key if the string is an anagram, and the 'n' key if it is not. \n \n Press any key to begin."
block_start = "Press any key to begin Block " #the block start message

#psychopy function (visual) to define the messages that were mentioned in the code above
start_text = visual.TextStim(win, text= start_msg)
instruct_text = visual.TextStim(win, text= instruct_msg)
fixation = visual.TextStim(win, text='+', color='black') #fixation cross that is shown between blocks and trials 

#timer for reaction times
trial_timer = core.Clock()

#=====================
#START EXPERIMENT
#=====================
start_text.draw() #start message is drawn into the back buffer
win.flip() #window is flipped, showing the start message

event.waitKeys() #waiting for keypress from participant to proceed

instruct_text.draw() #instruction text is drawn into the back buffer
win.flip() #window is flipped, showing stimuli
event.waitKeys() #waiting for key press

#=====================
#BLOCK SEQUENCE
#=====================
for iblock in range(nBlocks): #for loop that will run through the 2 blocks 
    block_start = 'Press any key to begin Block ' + str(iblock+1)
    block_text = visual.TextStim(win, text= block_start) #block start message defined
    block_text.draw()
    win.flip() #window flipped showing block start message
    event.waitKeys() 
    
    #=====================
    #TRIAL SEQUENCE
    #=====================    
    for itrial in range(nTrials): #for loop that runs through the 2 trials that are present in each block
        fixation.draw()
        win.flip()
        core.wait(1.0) #waiting before trial starts, only fixation cross is present at this moment 
        np.random.shuffle(stimuli) #shuffling the 10 words that are in the list before the start of each trial so that the participant gets a new order each time
        event.clearEvents() #clear keypresses
        
        #data is collected and added to these lists are the experiment progresses
        totalTrials = iblock*nTrials+itrial
        blockNumbers[totalTrials] = iblock+1
        trialNumbers[totalTrials] = itrial+1
        
        #=====================
        #START TRIAL
        #=====================   
        for stimulus in stimuli: #for loop that runs through the lsit of 10 words
            message = visual.TextStim(win, text=stimulus) #defining the stimulus
            message.draw()
            win.flip() #window is flipped, only one word is shown at a time
            keys=event.waitKeys(keyList=['y', 'n']) #wait for keypress, stimulus stays up on the screen until a keypress is performed
            trial_timer.reset() #reset clock 
            
            if keys:
                responseTimes[totalTrials] = trial_timer.getTime() #add reaction times to the response time list
                if stimulus in anagrams: #is the stimulus presented is present in the list of anagrams (meaning that it is an anagram), the if condition is met
                    if keys[0] == 'y': 
                        accuracy[totalTrials] = 'Correct' #if the word was an anagram and the "y" key was pressed, this was the correct action to take
                    else:
                        accuracy[totalTrials] = 'Incorrect' #if the word was not an anagram and the "y" key was pressed, this was the incorrect action to take
                else:
                    if keys[0] == 'n':
                        accuracy[totalTrials] = 'Correct' #if the word was not an anagram and the "n" key was pressed, this was the correct action to take
                    else: 
                        accuracy[totalTrials] = 'Incorrect' ##if the word was an anagram and the "n" key was pressed, this was the incorrect action to take
            
            print( #print funtion that will prinnt the block number (1 or 2), the trial number (1 or 2), the accuracy (correct/incorrect), and the response time of the participant 
            'Block:',
            iblock+1,
            ', Trial:', 
            itrial+1, 
            ', Accuracy:', 
            accuracy[totalTrials], 
            ', RT:', 
            responseTimes[totalTrials]
            )


#======================
# END OF EXPERIMENT
#======================
#the data that was collected in the for loops above is defined as a variable (=df) and this data is then loaded as a "DataFrame" object. This allows you to 
#view all the collected responses in a tabular format. This table will include the block number (1 or 2), the trial number (1 or 2), the accuracy (correct/incorrect), 
#and the response time of the participants. The data was stored in the empty lists created at the start of the experiment code.
#The panda data is converted to a .csv file and this file is saved in the directory that was defined above.
df = pd.DataFrame(data={
 "Subject number": exp_info['subject number'],
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers, 
 "Accuracy": accuracy, 
 "Response Time": responseTimes
})
df.to_csv(os.path.join(path, filename), sep=',', index=False)

#the window will close, indicating that the experiment is finished 
win.close()