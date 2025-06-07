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
    # Wave pose 1: Arm raised moderately, shoulder neutral
    wave_pose_1 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (looking forward, slightly up)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (relaxed, unchanged from your original)
        -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm: Shoulder raised moderately, neutral roll, elbow bent, wrist neutral
        0.0, 1.0,                         # LHand closed, RHand open
        0.0, 0.0, 0.0                    # HipRoll, HipPitch, KneePitch (neutral)
    ]

    # Wave pose 2: Arm raised higher, shoulder rolled outward (arm swings to the right)
    wave_pose_2 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -1.2, -1.0, 1.2, 0.6, 0.0,       # Right arm: Shoulder raised higher, rolled outward, elbow bent, wrist neutral
        0.0, 1.0,                         # LHand closed, RHand open
        0.0, 0.0, 0.0                    # HipRoll, HipPitch, KneePitch (neutral)
    ]

    # Wave pose 3: Arm lowered slightly, shoulder rolled inward (arm swings to the left)
    wave_pose_3 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -0.4, 0.0, 1.2, 0.6, 0.0,        # Right arm: Shoulder lowered slightly, rolled inward, elbow bent, wrist neutral
        0.0, 1.0,                         # LHand closed, RHand open
        0.0, 0.0, 0.0                    # HipRoll, HipPitch, KneePitch (neutral)
    ]

    turn_pose_1 = [
    0.00, -0.21,  # HeadYaw, HeadPitch (looking forward, slightly up)
    1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (relaxed, unchanged from your wave poses)
    -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm (neutral, from wave_pose_1)
    0.0, 1.0,                         # LHand closed, RHand open
    0.0, 0.0, 0.0                    # HipRoll, HipPitch, KneePitch (neutral)
    ]

    # Pose 2: Shift weight to left leg, slightly bend right knee
    turn_pose_2 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm (unchanged)
        0.0, 1.0,                         # LHand closed, RHand open
        0.2, 0.0, 0.1                    # HipRoll (lean left), HipPitch (neutral), KneePitch (right knee slightly bent)
    ]

    # Pose 3: Pivot right leg outward (start turn)
    turn_pose_3 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm (unchanged)
        0.0, 1.0,                         # LHand closed, RHand open
        0.2, -0.3, 0.1                   # HipRoll (lean left), HipPitch (pivot right leg), KneePitch (maintain)
    ]

    # Pose 4: Shift weight to right leg, continue turn
    turn_pose_4 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm (unchanged)
        0.0, 1.0,                         # LHand closed, RHand open
        -0.2, 0.3, 0.1                   # HipRoll (lean right), HipPitch (pivot left leg), KneePitch (maintain)
    ]

    # Pose 5: Complete turn, return to neutral stance
    turn_pose_5 = [
        0.00, -0.21,  # HeadYaw, HeadPitch (same)
        1.55, 0.13, -1.24, -0.52, 0.01,  # Left arm (unchanged)
        -0.8, -0.3, 1.2, 0.6, 0.0,       # Right arm (unchanged)
        0.0, 1.0,                         # LHand closed, RHand open
        0.0, 0.0, 0.0                    # HipRoll, HipPitch, KneePitch (neutral, facing 90 degrees)
    ]

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

        # im.robot.raiseArm() 
    
        im.robot.setPosture(wave_pose_1)
        time.sleep(0.3)
        im.robot.setPosture(wave_pose_2)
        time.sleep(0.3)
        im.robot.setPosture(wave_pose_3)
        
        im.robot.normalPosture()

        lang_ques = im.ask('lang', timeout=20)
        if lang_ques == 'en':
            im.robot.setLanguage('en')
        else:
            im.robot.setLanguage('it')

        while True:
            ask = im.ask('navigation_welcome', timeout=20)
            if ask == 'restroom':
                im.robot.setPosture([0.00, -0.21,1.55, 0.13, -1.24, -0.52, 0.01,0.3, -1.5, 1.0, 0.05, 0.0,0, 0, 0, 0, 0])
                im.execute('restroom')
            elif ask == 'din_ex':
                im.robot.setPosture([0.00, -0.21,1.55, 0.13, -1.24, -0.52, 0.01,0.3, -1.5, 1.0, 0.05, 0.0,0, 0, 0, 0, 0])
                im.execute('din_ex')
            elif ask == 'imp_paint':
                im.robot.setPosture([0.00, -0.21,1.55, 0.13, -1.24, -0.52, 0.01,0.3, -1.5, 1.0, 0.05, 0.0,0, 0, 0, 0, 0])
                im.execute('imp_paint')
            elif ask == 'crying_baby':
                im.execute('navigation_crying_baby')
                time.sleep(0.2)
                icecream =  im.ask('crying_baby_2', timeout=20)
                if icecream == 'yes':
                    im.robot.setPosture(turn_pose_1)
                    time.sleep(0.3)
                    im.robot.setPosture(turn_pose_2)
                    time.sleep(0.3)
                    im.robot.setPosture(turn_pose_3)
                    time.sleep(0.3)
                    im.robot.setPosture(turn_pose_4)
                    time.sleep(0.3)
                    im.robot.setPosture(turn_pose_5)
                    time.sleep(0.3)
                    im.execute('icecream')

            time.sleep(3)
            im.robot.normalPosture()
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
