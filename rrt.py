# using shapely for collision detection
#using annoy for ann search

from shapely.geometry import Polygon, Point, LineString
from cs1lib import start_graphics, draw_rectangle, clear, set_fill_color, set_stroke_color, set_stroke_width, draw_polygon, draw_line
from planarsim import transform_from_config, config_from_transform
import math
from numpy import pi, cos, sin, sinc, array, sqrt, arctan, \
    round
from search_node import search_node

CANVAS_HEIGHT = 400
CANVAS_WIDTH = 400

ROBOT_CENTER_X = 200
ROBOT_CENTER_Y = 200
ROBOT_THETA = 0
ROBOT_WIDTH = 100 
ROBOT_HEIGHT = 200


class rrt():

	def __init__(self, obstacle_file_path, curr_config):
		self.obstacle_file_path = obstacle_file_path
		self.obstacle_list = []
		self.curr_config = curr_config 
		self.vertex_dict = {}
		self.sol_list = []
		self.gen_obstacles()


	def gen_obstacles(self):
		"""
		Generate the obstacles to put into obstacle list for collision checking
		"""
		file = open(self.obstacle_file_path, "r")
		for line in file:
			attr_list = line.strip().split(" ")

			#Center x, y = top left corner
			center_x = int(attr_list[0])
			center_y = int(attr_list[1])
			width = int(attr_list[2])
			height = int(attr_list[3])
			obstacle = Polygon([(center_x, center_y), (center_x, center_y + height), (center_x + width, center_y), (center_x + width, center_y + height)])
			self.obstacle_list.append(obstacle)

	def draw_obstacles(self):
		"""
		Draw the obstacles
		"""
		file = open(self.obstacle_file_path, "r")
		for line in file:
			attr_list = line.strip().split(" ")

			#Center x, y = top left corner
			center_x = int(attr_list[0])
			center_y = int(attr_list[1])
			width = int(attr_list[2])
			height = int(attr_list[3])
			draw_rectangle(center_x, center_y, width, height)

	def draw_car(self):
		upper_left = (self.curr_config[0] - ROBOT_WIDTH/2, self.curr_config[1] - ROBOT_HEIGHT/2)
		lower_left = (self.curr_config[0] - ROBOT_WIDTH/2, self.curr_config[1] + ROBOT_HEIGHT/2)
		upper_right = (self.curr_config[0] + ROBOT_WIDTH/2, self.curr_config[1] - ROBOT_HEIGHT/2)
		lower_right = (self.curr_config[0] + ROBOT_WIDTH/2, self.curr_config[1] + ROBOT_HEIGHT/2)
		theta = self.curr_config[2]

		rotated_up_left = self.rotate_coord(upper_left[0], upper_left[1], theta)
		rotated_low_left = self.rotate_coord(lower_left[0], lower_left[1], theta)
		rotated_up_right = self.rotate_coord(upper_right[0], upper_right[1], theta)
		rotated_low_right = self.rotate_coord(lower_right[0], lower_right[1], theta)

		draw_polygon([rotated_up_left, rotated_up_right,rotated_low_right, rotated_low_left])
		 

		draw_polygon([upper_left, upper_right, lower_right, lower_left])

	def detect_collision(self, vertex_a, vertex_b):
		vertex_a_state = vertex_a.get_state()
		vertex_b_state = vertex_b.get_state()
		new_line = LineString([Point(vertex_a_state[0], vertex_a_state[1]), Point(vertex_b_state[0], vertex_b_state[1])])
		for obstacle in self.obstacle_list:
			if new_line.intersects(obstacle):
				return True
		return False

	def rotate_coord(self, x, y, theta):
		temp_x = x
		temp_y = y

		rotated_x = temp_x * cos(theta) - temp_y * sin(theta)
		rotated_y = temp_x * sin(theta) + temp_y * cos(theta)

		return rotated_x, rotated_y

			

	def draw(self):
		clear()
		set_fill_color(0, 0, 1)
		set_stroke_color(0, 0, 1)
		set_stroke_width(1)
		self.draw_obstacles()
		# start_node =  search_node((150, 200))
		# start_state = start_node.get_state()
		# goal_node = search_node((300, 2000))
		# goal_state= goal_node.get_state()
		# draw_line(start_state[0], start_state[1], goal_state[0], goal_state[1])
		# print(self.detect_collision(start_node, goal_node))
		#self.draw_car()

test_rrt = rrt("mobile_robot_obstacle_1.txt", [300, 200, float("{0:.2f}".format(math.pi/4))])
# test_rrt.draw_car()
start_graphics(test_rrt.draw, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
