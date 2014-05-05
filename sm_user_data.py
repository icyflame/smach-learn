#!/usr/bin/env python

import roslib;
import rospy
import smach
import smach_ros

class State1(smach.State):

	def __init__(self):

		smach.State.__init__(self, 
			outcomes=['valid', 'invalid'],
			input_keys=['val1_in'],
			output_keys=['val1_out'])

	def execute(self, userdata):

		print 'Input to state 1: ', userdata.val1_in

		userdata.val1_out = userdata.val1_in + 1

		return 'valid'

class State2(smach.State):

	def __init__(self):

		smach.State.__init__(self,
			outcomes=['valid', 'invalid'],
			input_keys=['val2_in'],
			output_keys=['val2_out'])

	def execute(self, userdata):

		print 'Input to state 2: ', userdata.val2_in		

		userdata.val2_out = userdata.val2_in + 1;

		return 'valid'

def main():

	rospy.init_node('smach_example_state_machine')

	sm = smach.StateMachine(outcomes=['exit'])

	sm.userdata.data = 0

	with sm:

		# smach.StateMachine.add('State1', State1(), transitions={
		# 				'valid':'State2',
		# 				'invalid':'State1'
		# 				})

		# smach.StateMachine.add('State2', State2(), 
		# 	transitions={'valid':'exit',
		# 				'invalid':'State1'
		# 				})

		smach.StateMachine.add('STATE1', State1(), 
			transitions={'valid':'STATE2',
						'invalid':'STATE1'
						},
			remapping={
						'val1_in':'data',
						'val1_out':'data'
			})

		smach.StateMachine.add('STATE2', State2(), 
			transitions={'valid':'exit',
						'invalid':'STATE1'
						},
			remapping={
						'val2_in':'data',
						'val2_out':'data'
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