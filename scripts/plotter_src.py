#!/usr/bin/env python
import rospy
#from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt 
from matplotlib.animation import FuncAnimation
	
class pose_visualizer(object):
	#def __init__(topic_name, message_name, cb_function):
	def __init__(self):
		plt.ion()
		self.fig, self.ax = plt.subplots()
		self.ln, = plt.plot([], [])#, 'ro')
		self.x_data, self.y_data = [] , []
		#self.x = None
		#self.y=None		
	
	def plot_init(self):
		self.ax.set_xlim(-5,5)
		self.ax.set_ylim(-5,5)
		return self.ln
				
	def update_plot(self,frame):
		#self.ax.scatter(self.x,self.y)
		self.ln.set_data(self.x_data,self.y_data)
		return self.ln

	def pose_callback(self,data):
		rospy.loginfo(data.pose[2].position.x)
		self.x_data.append(data.pose[2].position.x)
		self.y_data.append(data.pose[2].position.y) 
		#self.update_plot()
		

if __name__ == '__main__':
	rospy.init_node('plotter', anonymous=True)
	#plt.ion()
	vis = pose_visualizer();
	
	sub = rospy.Subscriber("gazebo/model_states",ModelStates, vis.pose_callback)
	ani = FuncAnimation(vis.fig, vis.update_plot, init_func=vis.plot_init)
	plt.show(block=True)
	
	#rospy.spin()	
	
