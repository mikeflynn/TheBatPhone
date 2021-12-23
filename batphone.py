import sched, random
from gpiozero import LED, Button
from time import sleep, time
from pygame import mixer
from signal import pause
from os import listdir
from os.path import isfile, join

# Init

devMode = True

ringInterval = 60 * 5 # Five minutes

if devMode:
    ringInterval = 30

led = LED(17)
button = Button(2)

onTheHook = False
isRinging = False

wavPath = '/home/pi/batphone/wavs/'
wavFiles = [f for f in listdir(wavPath + 'answers/') if isfile(join(wavPath + 'answers/', f))]

cron = sched.scheduler(time, sleep)
mixer.init()

# Functions

def log(msg):
    if devMode:
        print(msg)

def hungUp():
    global onTheHook
    log("Hung Up")
    onTheHook = True

def pickedUp():
    log("Picked Up")
    global onTheHook
    global isRinging
    onTheHook = False
    if isRinging == True:
        isRinging = False
        sleep(1)
        play(None)
    else:
        play(wavPath + 'system/dialtone.wav')

def shouldRing():
    """Checks if the phone should ring or not."""
    if onTheHook == True:
        return True

def ring(job): 
    """Rings the phone by flashing the light."""
    global isRinging
    log("Possibly ringining..")
    cron.enter(ringInterval, 1, ring, (job,))
    if shouldRing():
        log("Ringing!")
        isRinging = True
        for x in range(0, 4):
            for x in range(0, 20):
                led.toggle()
                sleep(0.1)
            if onTheHook == False:
                break;
            sleep(3)
    else:
        isRinging = False

def play(file):
    """Batman picks up; Play the audio."""
    log("Playing audio...")
    if file is None:
        global wavFiles
        answer = wavPath + 'answers/' + random.choice(wavFiles)
        log(answer)
        sound = mixer.Sound(answer)
    else:
        sound = mixer.Sound(file)
    sound.play()

# Main

play(wavPath + 'system/batman_theme.wav')

button.when_pressed = hungUp 
button.when_released = pickedUp

cron.enter(ringInterval, 1, ring, (cron,))
cron.run()

pause()

