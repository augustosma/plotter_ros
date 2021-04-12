#!/usr/bin/env python

import rospy
#from std_msgs.msg import String
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt 
from matplotlib.animation import FuncAnimation
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry

class pose_visualizer(object):
	#def __init__(topic_name, message_name, cb_function):
	def __init__(self):
		rospy.init_node('plotter', anonymous=True)
		sub = rospy.Subscriber("gazebo/model_states",ModelStates, self.gt_callback)
		sub = rospy.Subscriber("odom",Odometry, self.odom_callback)
		
		self.x_gt, self.y_gt = [], []
		self.x_odom, self.y_odom = [], []
		plt.ion()
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(1,1,1)
		self.ax.set_xlim(-10,10)
		self.ax.set_ylim(-10,10)
		self.line_gt, = self.ax.plot(self.x_gt,self.y_gt,'r')
		self.line_odom, = self.ax.plot(self.x_odom,self.y_odom)
				
	def plotter(self):
		while not rospy.is_shutdown():
			self.line_gt.set_data(self.x_gt,self.y_gt)
			self.line_odom.set_data(self.x_odom,self.y_odom)
			plt.draw()
			plt.pause(0.1)#update rate
	
		rospy.spin()
			
	def plot_init(self):
		self.ax.set_xlim(-10,10)
		self.ax.set_ylim(-10,10)
		return self.ln
				
	def update_plot(self):
		self.ax.plot(self.x,self.y)
		#plt.draw()
		#self.ln.set_data(self.x_data,self.y_data)
		#return self.ln

	def gt_callback(self,msg):
		self.x_gt.append(msg.pose[2].position.x)
		self.y_gt.append(msg.pose[2].position.y)
		
	def odom_callback(self,msg):
		#rospy.loginfo(msg.pose[2].position.x)
		self.x_odom.append(msg.pose.pose.position.x)
		self.y_odom.append(msg.pose.pose.position.y)



x, y = [], []
x_odom, y_odom = [],[]
x_,y_ = None, None

def callback(data):
	#rospy.loginfo(data.pose[2].position.x)
	x.append(data.pose[2].position.x)
	y.append(data.pose[2].position.y)

	#x_ = data.pose[2].position.x
	#y_ = data.pose[2].position.y

	#ax.plot(x,y)
	#fig.canvas.draw()
	#fig.show()

def plotter():

	rospy.init_node('plotter', anonymous=True)
	sub = rospy.Subscriber("gazebo/model_states",ModelStates, callback)
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_xlim(-10,10)
	ax.set_ylim(-10,10)
	line1, = ax.plot(x,y,animated=True)
	
	plt.show(block=False)
	
	#plt.pause(0.1)
	bg = fig.canvas.copy_from_bbox(fig.bbox)
	ax.draw_artist(line1)
	fig.canvas.blit(fig.bbox)

	while not rospy.is_shutdown():
		fig.canvas.restore_region(bg)
		line1.set_xdata(x)
		line1.set_ydata(y)
		ax.draw_artist(line1)
		fig.canvas.blit(fig.bbox)
		#fig.canvas.flush_events()
		
		#plt.pause(0.1)#graph update rate
	
	rospy.spin()
	
def plotter2():		
	rospy.init_node('plotter', anonymous=True)
	sub = rospy.Subscriber("gazebo/model_states",ModelStates, callback)
	sub = rospy.Subscriber("odom",ModelStates, callback)
	
	plt.ion()
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_xlim(-10,10)
	ax.set_ylim(-10,10)
	line1, = ax.plot(x,y)
	#plt.show(block=False)

	while not rospy.is_shutdown():
		line1.set_xdata(x)
		line1.set_ydata(y)
		plt.draw()
		plt.pause(0.1)#update rate
	
	rospy.spin()	

if __name__ == '__main__':
	#plotter()
	vis = pose_visualizer()
	vis.plotter()
	
