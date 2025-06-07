# nimations/Stand/BodyTalk/BodyTalk_10
import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
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

		im.executeModality('TEXT_default','Waiting for a human')

		#Checking if human stay in front of Pepper more than 2 seconds
		im.robot.startSensorMonitor()
		im.robot.normalPosture()
		im.robot.headscan()
		while not flagP:
			while not detected:
				p = im.robot.sensorvalue() #p is the array with data of all the sensors
				detected = p[1] > 0.0 and p[1] <= 1.0 #p[1] is the Front sonar
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
		im.executeModality('TEXT_default','Detection: Person Still Here')
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
		im.execute('start')
		time.sleep(1.2)
		intro_ques = im.ask('intro', timeout=20)
		print('* ', intro_ques)
		if intro_ques == 'yes':
			age = im.ask('age', timeout=20)
			if age != 'timeout':
				interest = im.ask('interest', timeout=20)
				if age == 'child':
					if interest == 'art':
						im.execute('art_leo_child')
						time.sleep(3)
						a0 = im.ask('art_leo_child_ques', timeout=20)
						if a0 == "yes":
							im.execute('art_leo_child_incorrect')
						elif a0 == "no":
							im.execute('art_leo_child_correct')
						else:
							pass
					elif interest == 'robots':
						pass
					elif interest == 'history':
						pass
				else: # teens - adults 
					level = im.ask('level', timeout=20)
					if interest == 'art':
						if level == 'fun_facts':
							im.execute('art_leo_fun_facts')
							print('* fun_facts page')
							time.sleep(3)
							im.execute('art_leo_fun_facts_random')
					
						elif level == 'deep_details':
							im.execute('art_leo_deep_details')
							print('* deep_details page')		
							a0 = im.ask('art_leo_deep_details_ques', timeout=20)
							if a0 == "bird_wings":
								im.execute('art_leo_deep_details_correct')
							else:
								im.execute('art_leo_deep_details_incorrect')
							
					elif interest == 'robots':
						pass
					elif interest == 'history':
						pass
				time.sleep(1)
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