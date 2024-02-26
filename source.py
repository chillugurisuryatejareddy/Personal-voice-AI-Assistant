import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import wikipedia as wk
import requests
import datetime
import pyjokes
import wolframalpha
from ecapture import ecapture as ec
import sys
import time
import threading
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

engine=pyttsx3.init("sapi5")

voices=engine.getProperty('voices')

engine.setProperty('voice',voices[1].id)


def speak(data):
    engine.say(data)
    engine.runAndWait()


def animation(name):
    for i in name:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.01)

def animation1():
    for i in wiki_result:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.05)






def get_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        animation("listening...")
        r.pause_threshold=0.8
        r.operation_timeout=2
        audio = r.listen(source)
    
    
    try:
        animation("recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)

    except:
        animation("I havent understand it yet....take an other try!\n")
        return "None"
    

    return query.lower()

def wish():
    Time=datetime.datetime.now().hour

    if Time >0 and Time < 12:
        speak("Good morning!")
    elif Time > 18 and Time <= 24:
        speak("Good Evening!")
    else:
        speak("Good afternoon !")
    
    speak(f' i am your personal voice assistant {assistant_name1} ')  



def user():

    speak("what should I call you")
    uname=get_command()
    input_times=0
    while uname=="None":
        if(input_times>4):
            exit(0)
        speak("please register your name")
        new_uname=get_command()
        uname =new_uname
        input_times=input_times+1


    speak(f'Hello {uname} how can i help you today?')


# def mute_audio():
#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(
#         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#     volume = cast(interface, POINTER(IAudioEndpointVolume))
#     volume.SetMute(1, None)

# def unmute_audio():
#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(
#         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#     volume = cast(interface, POINTER(IAudioEndpointVolume))
#     volume.SetMute(0, None)









def get_data(query):
    city= query #city_name.get()
    response=requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=3c6679635a8c3691db92d978ca07fc15")
    data=response.json()
    
    
    climate_value=str(str.capitalize(str(data["weather"][0]["main"])))
    temperature_value=str(int(data ["main"]["temp"]-273.15))+" °Centigrade"
    temperature_max_value=str((int(data ["main"]["temp_max"]-273.15)))+" °Centigrade"
    temperature_min_value=str(int(data ["main"]["temp_min"]-273.15))+" °Centigrade"

    return climate_value,temperature_value,temperature_max_value,temperature_min_value
    







if __name__=="__main__":

    assistant_name1="STR"

    wish()
    user()

    

    while True:

        query = get_command().lower()

        if "weather in" in query:
            try:
                weather_details = get_data(query[10:])
                speak("The current weather condition of "+weather_details[0]+", the temperature is "+weather_details[1])
            except Exception as k:
                print(k)
                speak("sorry! city not found")



        elif "temperature in" in query:
            try:
                weather_details = get_data(query[14:])
                speak("The temperature is "+weather_details[1]+". Hope you will have a nice day")
            except Exception as k:
                print(k)
                speak("sorry i can't understand it")

        elif "tell me about" in query:
            try:
                wiki_result = wk.summary(query[13:], sentences=4)
                print("="*139)
                # animation(wiki_result)
                # # print("="*123)
                # speak(wiki_result)
                x=threading.Thread(target=animation1)
                x.start()
                speak(wiki_result)
                print("\n")
                print("="*139)
                # y=threading.Thread(target=animation1)
                # y.start()
                
            except Exception as e :
                print(e)
                speak("sorry i can't understand it")


        elif "open" in query:
            try:
                speak("opening" + query[6:])
                webbrowser.open_new_tab('https://www.'+query[5:])
            except Exception as e:
                print(e)
                print("Sorry! try again")
                speak("Sorry! try again")

        elif "tell me a joke" in query or "say me a joke" in query or "make me laugh" in query :
            jokes=pyjokes.get_joke()
            print("="*139)
            animation(jokes.replace(".",""))
            animation(" 😂🤣🤣\n")
            print("="*139)
            speak(jokes)
        
        elif "nice" in query or "good joke" in query:
            speak("thank you")
        
        elif "love you" in query:
            speak("give me some time to think")
        
        elif "calculate" in query:
            try:
                app_id="4A2UH2-TGHP2J58UY"
                client=wolframalpha.Client(app_id)
                index=query.lower().split().index('calculate')
                query = query.split()[index+1:]
                res=client.query(' '.join(query))
                answer=next(res.results).text
                print("="*139)
                print(f'{query}={answer}')
                print("="*139)
                speak(answer)

            except Exception as e:
                print(e)
        
        elif "change your name" in query:
            speak(" do you want to change my name?")
            if "yes" in get_command().lower():
                speak("give me a new name")
                assistant_name2=get_command()
                speak(f' name changed to {assistant_name1} to {assistant_name2}')
                assistant_name1=assistant_name2
            else:
                pass

        elif "how are you" in query:
            speak("I am good, how about you?")

            mood = get_command()
            if "fine" in mood or "good" in mood or "great" in mood:
                speak("great to hear that you are fine.")
            else:
                speak("hmm let's hope everything is going well for you too.")

        elif "hello" in query or "hey" in query or "hola" in query:
            speak("hello! how can I help you?")
        
        elif "what is your name" in query or "your name" in query:
            speak("my name is "+str(assistant_name1)+". How may I assist you today?")

        
        elif "who are you" in query or "tell me about you" in query:
            speak("My name is "+str(assistant_name1)+", and I am an AI developed by surya teja reddy")
        
        elif "change your voice" in query:
            voices=engine.getProperty('voices')
            
            speak("do you want male or female voice")
            tone=get_command()
            if (tone=='None' or tone != "male" and tone!="female"):
                speak("provide me with correct input")
                speak("There are two voice modulations")
                speak("that are male voice and female voice")
                speak("please provide me with the type of voice you want")
                tone=get_command()
                while tone!="male":
                    if tone=="female":
                        break
                    speak("choose either male voice or female voice")
                    tone=get_command()

            if tone=="male" or tone=="male voice":
                speak("changing to male voice")
                engine.setProperty('voice',voices[0].id)
            elif tone=="female"or tone=="female voice" or tone=="women voice":
                speak("changing to female voice")
                engine.setProperty('voice',voices[1].id)
            
        
        elif "where are you" in query:
            speak("i am running on cloud servers across the globe")
        
        elif "who is" in query or "what is" in query:
            try:
                app_id="4A2UH2-TGHP2J58UY"
                client=wolframalpha.Client(app_id)
                res=client.query(query)
                answer=next(res.results).text
                animation(answer+"\n")
                speak(answer)

            except:
                print("no results found \n")
        
        elif "silence mode" in query or "silence" in query:
            speak("muted")
            volume=engine.getProperty('volume')
            engine.setProperty('volume',0.0)
            

            
        
        elif "unmute" in query or "increase volume" in query:
            volume=engine.getProperty('volume')
            engine.setProperty('volume',1.0)
            speak("unmuted\n")


        elif "exit"in query or "stop" in query:
            speak(query+"ing")
            exit(0)
        
        elif "play music" in query or "play a song" in query:
            try:
                speak("playing music")
                webbrowser.open_new_tab("https://music.youtube.com/watch?v=9nRvqemGydw&list=PLqHG6DQFUMjTQQ-iEfryCtP-aTZb1UtCt")
            except:
                speak("can't play music sorry")
        
        elif "take a picture" in query or "take a photo" in query:
            speak("taking photo...")
            animation("😁😁😁\n")
            ec.capture(0, "Camera ", "img.jpg")
        
        elif "what is time" in query or "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)
        
        elif "good job" in query:
            speak("it's my duty to serve!,Thanks for the compliment")
        
        else:
            speak("Please say the command again.")





    


