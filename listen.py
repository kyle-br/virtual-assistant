import speech_recognition as sr
from datetime import date, datetime
import pyttsx3   #Convert text to speech (need to install pyttsx3 and pywind32 )
import pywhatkit #Playing YouTube Videos 
import requests #weather report for city
import webbrowser
import time
import random
from word2number import w2n # convert word to number (use to convert any number in word to real number: use in calc function)
# Robot mouth part
robot_mouth = pyttsx3.init()
voices=robot_mouth.getProperty('voices')
robot_mouth.setProperty('voice',voices[1].id)
robot_mouth.setProperty('rate', 140) # Decrease the Speed Rate x2

def talk(text): #talk function (only accept string as parameter)
    robot_mouth.say(text)
    robot_mouth.runAndWait()

# Robot ear part
robot_ear= sr.Recognizer() 
def take_command():
    try:
        with sr.Microphone() as mic: 
            print("""
                Hello, my name is ivy, your virtual assistant
                Make sure to say 'ivy' first before giving a command.
                -To do math problems, say "ivy calculate (problem)"
                -To open a website, say "ivy open (name of website)"
                 """)
            # talk("""Hello, my name is ivy, your virtual assistant. Make sure to say 'ivy' first before giving a command.
            #      """)
            
            print('listening...')
            robot_ear.adjust_for_ambient_noise(mic) #remove noise in background, result in faster respond from machine
            audio= robot_ear.listen(mic)
            command=robot_ear.recognize_google(audio) #using google word-listening service
            command= command.lower() 
            if'ivy' in command: 
                command=command.replace('ivy ',"")
            else:
                talk('please make sure say "ivy" first')
                print('please make sure say "ivy" first')
                return ""
    except:
        you=""
    return command

def run_alexa(): #this function pass all command to the coresponding methods
    ans=take_command()
    print(ans)
    if ans[0:4]=='play':
        play(ans)
    if ans[0:9]=='calculate':
        ans= ans.split(" ")
        ans.pop(0)
        calc(ans)
    elif 'what' in ans:
        if "today" in ans:
            today_date()
        if "time" in ans:
            time_now()
        if "weather" in ans :
            weather()
    elif "open" in ans:
        open_websites(ans)
    elif "how are you" in ans:
        print("I feel good. Thanks for asking")
        talk("I feel good. Thanks for asking")
    elif "how old are you" in ans:
        print("They say that age is nothing but a number. But technically, it's also a word")
        talk("They say that age is nothing but a number. But technically, it's also a word")
    elif "tell me a joke" in ans:
        jokes()
    else:
        print("Sorry, try another command")


def play(a): # This function will assign the command and pop up youtube
    song = a.replace('play','')
    talk('playing'+ song)
    print('Now playing:' + song)
    pywhatkit.playonyt(song) #play on YTube
    exit()

def today_date(): 
    today= date.today()
    talk('Okay, today is: '+ today.strftime("%B %d, %Y"))
    print('Today is:' + today.strftime("%B %d, %Y"))

def time_now():
    time= datetime.now()
    talk('It is '+ time.strftime("%H:%M"))
    print('Current time: '+ time.strftime("%H:%M:%S"))
    
def weather():
    talk("here's there weather report for today")
    url= 'https://wttr.in/{}'.format('baton rouge')
    res= requests.get(url)
    print(res.text)
       
def calc(agrs): # calculate basic math (only do simple math with 2 numbers)
    if '+' in agrs:
        try: 
            for i in agrs:
                if i == '+':
                    agrs.remove('+')
            total=[int(item) for item in agrs] #convert string-value in list to int
        except:
            print("sorry, that exceed my ability")# this occur when multiples different operators in statement
            talk("sorry, that exceed my ability")
        total=sum(total)
        total=str(total)
        print("Answer: ",total)
        talk("Answer is: "+ total)
        
    if '-' in agrs[1]:
        agrs=w_to_n(agrs[0]) - w_to_n(agrs[2])
        agrs= str(agrs)
        print("Answer: ",agrs)
        talk("Answer is: "+ agrs)
    
    if '*' in agrs[1]:     
        agrs=w_to_n(agrs[0]) * w_to_n(agrs[2])
        agrs= str(agrs)
        print("Answer: ",agrs)
        talk("Answer is: "+ agrs)
   
    if '/' in agrs[1]:  
        try:
            agrs=w_to_n(agrs[0]) / w_to_n(agrs[2])
            agrs= str(agrs)
            print("Answer: ",agrs)
            talk("Answer is: "+ agrs)
        except ZeroDivisionError:
            print("Zero, Division Error")
            talk("Zero, Division Error")

def w_to_n(x):
    x= w2n.word_to_num(x)
    return x
def open_websites(ans):
    if 'open youtube' in ans:
        webbrowser.open_new_tab("https://www.youtube.com")
        talk("youtube is open now")
        

    elif 'open google' in ans:
        webbrowser.open_new_tab("https://www.google.com")
        talk("Google chrome is open now")
        

    elif 'open gmail' in ans:
        webbrowser.open_new_tab("https://www.gmail.com")
        talk("Google Mail open now")
        
    elif 'open facebook' in ans:
        webbrowser.open_new_tab("https://www.facebook.com")
        talk("Facebook is open now")
        
    elif 'open amazon' in ans:
        webbrowser.open_new_tab("https://www.amazon.com")
        talk("Amazon is open now")
        
    elif 'open yahoo' in ans:
        webbrowser.open_new_tab("https://www.yahoo.com")
        talk("Yahoo is open now")
    
    else: 
        print("That's exceed my ability at this moment")
        talk("That's exceed my ability at this moment")
    
def jokes():
    jlist = ["What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Hear about the new restaurant called Karma? There's no menu: You get what you deserve.",
            "Did you hear about the actor who fell through the floorboards? He was just going through a stage.",
            "Where are average things manufactured? The satisfactory.",
            "How do you drown a hipster? Throw him in the mainstream.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem",
            "Whats the object-oriented way to become wealthy?..Inheritance"
            "Why did the programmer quit his job? Because he didn't get arrays."]
    joke=random.choice(jlist)
    print(joke)
    talk(joke)