################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

from arduinoCom import *
import Leap
import sys
import time


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        hand = frame.hands[0]

        #Add two hands
        #handType = "Left hand" if hand.is_left else "Right hand"

        if hand.palm_position.y == 0:
            sendToArduinoLeap("9;%s;" % (0))

        else:
            sendToArduinoLeap("9;%s;" % (280 - (int(hand.palm_position.y) / 2)))


        #Use two hands
        """if hand.is_left:
          sendToArduinoLeap("3;%s;" % (int(hand.palm_position.y) / 2))
        else:
            sendToArduinoLeap("9;%s;" % (int(hand.palm_position.y) / 2))"""

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Connect to Arduino
    setupSerial()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
