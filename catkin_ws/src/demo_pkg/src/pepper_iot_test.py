#!/usr/bin/env python
# Title : pepper_iot.py
# Author : Clarissa Cremona
# Date : 09/06/2017
# Version : 1.0

import rospy, qi, argparse
import os
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # this is the message type /iot_updates uses

#class myModule(ALModule):
def dialog1():
    ALDialog = ALProxy("ALDialog", "pepper.local", 9559)
    topic_content = ('topic: ~medication()\n'
					'language: enu\n'
					'concept:(choice) [yes no "yes please" "no thank you"]\n'
                    'u: (yes [please]) Great!^stopTag(body language)\n'
                    'u: (no ["thank you"]) Okay.')
    topic_name = ALDialog.loadTopicContent(topic_content)
    ALDialog.activateTopic(topic_name)
    ALDialog.subscribe('med_dialog')
    time.sleep(5)
    ALDialog.unsubscribe('med_dialog')
    ALDialog.deactivateTopic(topic_name)
    ALDialog.unloadTopic(topic_name)
    return

def dialog2():
    #Get ALDialog service
    ALDialog = ALProxy("ALDialog", "pepper.local", 9559)
    ALDialog.resetAll()
    print(ALDialog.getAllLoadedTopics())
    topic_content = ('topic: ~cup_of_tea()\n'
					'language: enu\n'
					'concept:(choice) [yes no "yes please" "no thank you"]\n'
                    'u: (What ["is the message" "is it"]) Your friend, Mauro, has put the kettle on for a cup of tea. Would you like to do the same, and have a chat with him? \n'
						'u1: (yes [please]) Im sure he is looking forward to it\n'
						'u1: (no ["thank you"]) are you sure?\n'
							'u2: (yes) okay\n'
							'u2: (no) Im sure he is looking forward to it\n')
    topic_name = ALDialog.loadTopicContent(topic_content)
    ALDialog.activateTopic(topic_name)
    ALDialog.subscribe('tea_dialog')
    time.sleep(16)
    ALDialog.unsubscribe('tea_dialog')
    ALDialog.deactivateTopic(topic_name)
    ALDialog.unloadTopic(topic_name)
    basicProxy.setEnabled(False)

def callback(data):
    print(data.key + " " + data.value)
    if(data.key == "WeMo_Motion" and data.value == "ON"): # Drawer opened
        print("wemo on")
        med_drawer()
    elif(data.key == "WeMo_Switch" and data.value == "ON"): # Light ground floor on
        kettle_on()
        #med_drawer()

def med_drawer():
    #basicProxy.setTrackingMode("MoveContextually")
    basicProxy.setTrackingMode("Head") # track human with head
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    motionProxy.moveTo(1.0, 0.0, 0.0) # move forewards
    animatedProxy.say("^startTag(body language)What medication are you taking Clarissa?")
    time.sleep(2)
    tabletProxy.showImage("http://198.18.0.1/apps/ibup-b76bd1/Ibuprofen.jpeg")
    animatedProxy.say("Ibuprofen should not be taken on an empty stomach. Would you like to have a meal first?")
    #memoryProxy.subscribeToEvent("PictureDetected", "newModule", "dialog1")
    dialog1()
    tabletProxy.hideImage()
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

def kettle_on():
    #tts.say("The light is off")
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    print("start dialog")
    animatedProxy.say("^startTag(body language)I've got a message for you.")
    tabletProxy.showImage("http://198.18.0.1/apps/dragone-51a938/Dragone.jpg")
    dialog2()
    tabletProxy.hideImage()
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

def listener():
    rospy.init_node('pepper_listener', anonymous=True) # create node to subscribe to topic
    rospy.Subscriber("iot_updates", KeyValue, callback) # subscribe to topic /iot_updates
    rospy.spin() # keeps python from exiting until node is stopped
    #print(data.value)

if __name__ == '__main__':
    from naoqi import ALProxy
    # Create a local broker, connected to the remote naoqi
    broker = ALBroker("pythonBroker", "192.168.1.62", 9999, "pepper.local", 9559)
    #global newModule
    #newModule = myModule("newModule")
    tts = ALProxy("ALTextToSpeech", "pepper.local", 9559) # initialise speech proxy
    tts.setParameter("speed", 100) # set speed of speech
    animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    motionProxy = ALProxy("ALMotion", "pepper.local", 9559) # initialise motion proxy
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559)
    #recogProxy = ALProxy("ALSpeechRecognition", "pepper.local", 9559) # initialise speech recognition proxy

    basicProxy = ALProxy("ALBasicAwareness", "pepper.local", 9559) # initialise basic awareness proxy
    basicProxy.setEnabled(True) # enable basic awareness # set tracking mode to move
    basicProxy.setEngagementMode("FullyEngaged")

    #recogProxy.subscribe("Test_ASR")
    memProxy = ALProxy("ALMemory","pepper.local",9559)
    #memoryProxy.subscribeToEvent(event_name, "newModule", "Dialog/Answered")
    listener()
