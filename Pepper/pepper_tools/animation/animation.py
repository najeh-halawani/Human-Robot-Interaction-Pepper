import qi
import argparse
import sys
import time
import os



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Memory Read", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    animation_player_service = session.service("ALAnimationPlayer")
    # # animation_player_service.run('animations/Stand/Gestures/Hey_1')
    # animation_player_service.run("animations/Stand/Gestures/Hey_1", _async=True)

    # play an animation, this will return right away
    future = animation_player_service.run("animations/Stand/Gestures/Hey_2", _async=True)
    # stop the animation
    future.cancel()


    # animation_player_service.run("Hey_1")


if __name__ == "__main__":
    main()
