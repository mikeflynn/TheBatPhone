import sched
from gpiozero import LED, Button
from time import sleep, time
from pygame import mixer
from signal import pause

ringInterval = 20
led = LED(17)
button = Button(2)

onTheHook = False
isRinging = False

cron = sched.scheduler(time, sleep)
mixer.init()

def hungUp():
    global onTheHook
    #print("Hung Up")
    onTheHook = True

def pickedUp():
    #print("Picked Up")
    global onTheHook
    onTheHook = False
    if isRinging == True:
        sleep(1)
        play()

def shouldRing():
    """Checks if the phone should ring or not."""
    if onTheHook == True:
        return True

def ring(job): 
    """Rings the phone by flashing the light."""
    global isRinging
    #print("Possibly ringining..")
    cron.enter(ringInterval, 1, ring, (job,))
    if shouldRing():
        #print("Ringing!")
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

def play():
    """Batman picks up; Play the audio."""
    #print("Playing audio...")
    sound = mixer.Sound('/home/pi/batphone/wavs/batman_theme.wav')
    sound.play()

button.when_pressed = hungUp 
button.when_released = pickedUp

cron.enter(ringInterval, 1, ring, (cron,))
cron.run()

pause()

