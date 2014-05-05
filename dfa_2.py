# Strings starting with 00 and ending with 11

#!/usr/bin/env python

import roslib;
import rospy
import smach
import smach_ros

class State1(smach.State):

	def __init__(self):

		smach.State.__init__(self, 
			outcomes=['proceed', 'dead'],
			input_keys=['val1_in'],
			output_keys=['val1_out'])

	def execute(self, userdata):

		print 'Input to state 1: ', userdata.val1_in

		x = raw_input("input: ")

		userdata.val1_out = x

		y = userdata.val1_in

		if y == '0':

			return 'proceed'

		else:

			return 'dead'

class State2(smach.State):

	def __init__(self):

		smach.State.__init__(self,
			outcomes=['proceed', 'dead'],
			input_keys=['val2_in'],
			output_keys=['val2_out'])

	def execute(self, userdata):

		print 'Input to state 2: ', userdata.val2_in		

		x = raw_input('input: ')

		userdata.val2_out = x

		y = userdata.val2_in

		if y == '0':

			return 'proceed'

		else:

			return 'dead'

class State3(smach.State):

	def __init__(self):

		smach.State.__init__(self,
			outcomes=['stay', 'proceed'],
			input_keys=['val3_in'],
			output_keys=['val3_out']
			)

	def execute(self, userdata):

		x=raw_input("input: ")
		userdata.val3_out = x
		y = userdata.val3_in

		if y == '0':

			return 'stay'

		elif y == '1':

			return 'proceed'

class State4(smach.State):

	def __init__(self):

		smach.State.__init__(self,
			outcomes=['accept', 'regress'],
			input_keys=['val4_in'],
			output_keys=['val4_out'])

	def execute(self, userdata):

		x=raw_input("input: ")
		userdata.val4_out = x

		y = userdata.val4_in

		if y == '0':

			return 'regress'

		elif y == '1':

			return 'accept'


def main():

	rospy.init_node('smach_dfa_1')

	sm = smach.StateMachine(outcomes=['accept', 'exit'])

	sm.userdata.data = 0

	with sm:

		smach.StateMachine.add('STATE1', State1(), 
			transitions={'proceed':'STATE2',
						'dead':'exit'
						},
			remapping={
						'val1_in':'data',
						'val1_out':'data'
			})

		smach.StateMachine.add('STATE2', State2(), 
			transitions={'proceed':'STATE3',
						'dead':'exit'
						},
			remapping={
						'val2_in':'data',
						'val2_out':'data'
			})

		smach.StateMachine.add('STATE3', State3(), 
			transitions={'proceed':'STATE4',
						'stay':'STATE3'
						},
			remapping={
						'val3_in':'data',
						'val3_out':'data'
			})

		smach.StateMachine.add('STATE4', State4(), 
			transitions={'accept':'accept',
						'regress':'STATE3'
						},
			remapping={
						'val4_in':'data',
						'val4_out':'data'
			})

	# Create and start the introspection server
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()

	# Execute the state machine
	outcome = sm.execute()

	# Wait for ctrl-c to stop the application
	rospy.spin()
	sis.stop()

if __name__ == '__main__':

	main()