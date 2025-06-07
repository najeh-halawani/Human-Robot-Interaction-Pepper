# nimations/Stand/BodyTalk/BodyTalk_10
import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME') + '/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

import ws_client
from ws_client import *

def intStart():
    # im.robot.setVolume(100)
    while True:
        im.init()
        im.robot.setAlive(True)
        flagP = False
        detected = False

        im.executeModality('TEXT_default', 'Waiting for a human')

        # Checking if human stays in front of Pepper more than 2 seconds
        im.robot.startSensorMonitor()
        im.robot.normalPosture()
        im.robot.headscan()
        while not flagP:
            while not detected:
                p = im.robot.sensorvalue()  # p is the array with data of all the sensors
                detected = p[1] > 0.0 and p[1] <= 1.0  # p[1] is the Front sonar
            if detected:
                print('*Person Detected*')
                time.sleep(2)
                p = im.robot.sensorvalue()
                detected = p[1] > 0.0 and p[1] <= 1.0
                if detected:
                    print('*Person still there*')
                    flagP = True
                else:
                    print('*Person gone*')

        im.executeModality('TEXT_default', 'Detection: Person Still Here')
        im.robot.stopSensorMonitor()
        im.robot.normalPosture()

        im.robot.raiseArm()
        time.sleep(0.5)
        im.robot.normalPosture()
        lang_ques = im.ask('lang', timeout=20)
        if lang_ques == 'en':
            im.robot.setLanguage('en')
        else:
            im.robot.setLanguage('it')
        while True:
            ask = im.ask('navigation_welcome', timeout=20)

            if ask == 'restroom':
                im.execute('restroom')
            elif ask == 'din_ex':
                im.execute('din_ex')
            elif ask == 'imp_paint':
                im.execute('imp_paint')
            elif ask == 'crying_baby':
                im.execute('navigation_crying_baby')

            time.sleep(3)
            q = im.ask('menuexist', timeout=4)
            if q == 'timeout':
                im.execute('repeat')
                time.sleep(3)
                q = im.ask('menuexist', timeout=10)

            if q == 'main_menu':
                pass
            elif q == 'exit':
                feedback = im.ask('feedback', timeout=10)
                im.execute('goodbye')
                time.sleep(1)

if __name__ == "__main__":
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)
    mws.run_interaction(intStart)
