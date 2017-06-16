#!/usr/bin/env python
# Title : pepper_iot.py
# Author : Clarissa Cremona
# Date : 09/06/2017
# Version : 1.0

import rospy, qi, argparse, sys
#from std_msgs.msg import String
from diagnostic_msgs.msg import KeyValue # this is the message type /iot_updates uses

def dialog():
    #Get ALDialog service
    ALDialog = ALProxy("ALDialog", "pepper.local", 9559)
    ALDialog.resetAll()
    print(ALDialog.getAllLoadedTopics())
    topic_content = ('topic: ~cup_of_coffee()\n'
					'language: enu\n'
					'concept:(choice) [yes no "yes please" "no thank you"]\n'
                        'u: (What ["is the message" "is it"]) Your friend, Mawro, has put the kettle on for a cup of tea. Would you like to do the same, and talk to him over video chat? \n'
						'u1: (yes) Im sure he is looking forward to it\n'
						'u1: (no) are you sure?\n'
							'u2: (yes) okay\n'
							'u2: (no) Im sure he is looking forward to it\n')
    topic_name = ALDialog.loadTopicContent(topic_content)
    ALDialog.activateTopic(topic_name)
    ALDialog.subscribe('coffee_dialog')
    try:
        raw_input("\nSpeak to the robot. Press Enter when finished: ")
    finally:
        ALDialog.unsubscribe('coffee_dialog')
        ALDialog.deactivateTopic(topic_name)

def callback(data):
    print(data.key + " " + data.value)
    if(data.key == "WeMo_Motion" and data.value == "ON"): # Drawer opened
        print("wemo on")
        #med_drawer()
    elif(data.key == "Light_GF" and data.value == "ON"): # Light ground floor on
        #kettle_on()
        med_drawer()

def kettle_on():
    #basicProxy.setTrackingMode("Head") # track human with head
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    motionProxy.post.moveTo(0.2, 0.0, 0.0) # move forewards
    animatedProxy.say("^startTag(body language)I've got a message for you.")
    animatedProxy.say("\\pau=1000\\Your friend, Mauro, has put the kettle on for a cup of tea. Would you like to do the same and talk to him over video chat?^stopTag(body language)")
    #vocabulary = ["yes", "no", "please"]
    #recogProxy.setVocabulary(vocabulary, False)
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    #print("The light is on!")

def med_drawer():
    #tts.say("The light is off")
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    motionProxy.post.moveTo(-0.2, 0.0, 0.0) # move backwards
    print("start dialog")
    animatedProxy.say("^startTag(body language)I've got a message for you.")
    tabletProxy.showImage("http://198.18.0.1/apps/dragone-51a938/Dragone.jpg")
    dialog()
    tabletProxy.hideImage()
    #animatedProxy.say("^startTag(body language)If you are going to take your medication, Doxycycline must not be taken on an empty stomach. Would you like to have a meal first?^stopTag(body language)")
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s %s', data.key, data.value)

def listener():
    rospy.init_node('pepper_listener', anonymous=True) # create node to subscribe to topic
    rospy.Subscriber("iot_updates", KeyValue, callback) # subscribe to topic /iot_updates
    rospy.spin() # keeps python from exiting until node is stopped
    #print(data.value)

if __name__ == '__main__':
    from naoqi import ALProxy
    tts = ALProxy("ALTextToSpeech", "pepper.local", 9559) # initialise speech proxy
    tts.setParameter("speed", 100) # set speed of speech
    animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    motionProxy = ALProxy("ALMotion", "pepper.local", 9559) # initialise motion proxy
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559)
    #recogProxy = ALProxy("ALSpeechRecognition", "pepper.local", 9559) # initialise speech recognition proxy

    # THREE LINES TO BE UNCOMMENTED basicProxy = ALProxy("ALBasicAwareness", "pepper.local", 9559) # initialise basic awareness proxy
    #basicProxy.setEnabled(True) # enable basic awareness
    #basicProxy.setTrackingMode("MoveContextually") # set tracking mode to move

    #recogProxy.subscribe("Test_ASR")
    #memProxy = ALProxy("ALMemory","pepper.local",9559)
    listener()
