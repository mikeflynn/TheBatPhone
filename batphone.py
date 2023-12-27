import sched, random
from gpiozero import LED, Button
from time import sleep, time
from pygame import mixer
from signal import pause
from os import listdir
from os.path import isfile, join

# Init

devMode = False

reciever = Button(18)
led = LED(17)
statusLed = LED(22)

onTheHook = True
isRinging = False

wavPath = '/opt/batphone/wavs/'
wavFiles = [f for f in listdir(wavPath + 'answers/') if isfile(join(wavPath + 'answers/', f))]

cron = sched.scheduler(time, sleep)
mixer.init()

# Functions

def getRingInterval(devMode):
    if devMode:
        return 30
    else:
        return (60 * 5) + random.randint(-120, 120)

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
    return onTheHook

def ring(job):
    """Rings the phone by flashing the light."""
    global isRinging
    log("Possibly ringining..")
    cron.enter(getRingInterval(devMode), 1, ring, (job,))
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

statusLed.on()
play(wavPath + 'system/batman_theme.wav')

reciever.when_pressed = pickedUp # Weird flipped logic because of the switch I hacked out of the original phone.
reciever.when_released = hungUp

cron.enter(10, 1, ring, (cron,)) # After boot, ring right away for quick testing.
cron.run()

pause()

