'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2013  Moritz Kassner & William Patera

 Distributed under the terms of the CC BY-NC-SA License. 
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
'''
import os, sys, argparse, time

from ctypes import *

import cv2
import numpy as np
from glob import glob

from multiprocessing import Process, Pipe, Value
from browser_2d import browser
# from audio import play_audio

class Browser(object):
	"""Command Line manager for 2D Browser"""
	def __init__(self):
		self.parseCommandLineFlags()
		self.exceptions()
		self.load_data()

	def parseCommandLineFlags(self):
		parser = argparse.ArgumentParser(description="2D Browser for PUPIL data.  \
					Recorded eye movements are superimposed onto the recorded video stream for purposes of analysis.")
		parser.add_argument('-d', '--data_path', type=str,
			help='The data directory from the capture routine (only required input).',
			required=True)

		try:
			args = parser.parse_args(namespace=self)
		except:
			parser.print_help()
			sys.exit()

	def exceptions(self):
		if not os.path.isdir(self.data_path):
			raise Exception, "'%s' is not a directory.  Please specify a data_path directory." %(self.data_path)

	def load_data(self):
		os.chdir(self.data_path)
		try:
			self.video_path = [os.path.join(self.data_path, "world.avi")]
		except:
			print "Could not load video 'world.avi' please check the file name and data directory given."
			self.video_path = None

		try:
			all_videos = glob(self.data_path+'/*.mov')+glob(self.data_path+'/*.avi')
			src_video_name = [video for video in all_videos if 'world.avi' not in video]
			self.video_path = [self.video_path[0], src_video_name[0]]
			print "Found %s.  Using homography mapping to find correspondence between source and %s" %(self.video_path[0], self.video_path[1])
		except:
			self.source_video_path = None
			print "Could not find source video.  Proceed with single video."

		try:
			self.audio_path = os.path.join(self.data_path, "world.wav")
		except:
			print "Could not load audio 'world.wav' please check the file name and data directory given."
			self.audio_path = None

		try:
			self.pts_path = os.path.join(self.data_path, "gaze_positions.npy")
		except:
			print "Could not load pupil positions 'pupil_positions.npy' please check the file name and data directory given."
			self.pts_path = None

		try:
			self.cam_intrinsics_path = [os.path.join(self.data_path, 'camera_matrix.npy')]
			self.cam_intrinsics_path.append(os.path.join(self.data_path, 'dist_coefs.npy'))
			np.load(self.cam_intrinsics_path[0])
		except:
			print "Could not find camera intrinsics .npy files."
			self.cam_intrinsics_path = None




def main(data_path, video_path, audio_path, pts_path, cam_intrinsics_path):
	browser(data_path, video_path, pts_path, cam_intrinsics_path)


if __name__ == '__main__':
	#	data_path = "/Volumes/HD_Two/Users/Will/Documents/2012/MIT/Thesis/Thesis_Data/Capture/05052012/mpk_stata_05052012/003"
	b = Browser()
	main(b.data_path, b.video_path, b.audio_path, b.pts_path, b.cam_intrinsics_path)


