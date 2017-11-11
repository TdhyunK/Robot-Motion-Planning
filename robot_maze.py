from robot_arm import robot_arm
from shapely.geometry import Polygon
from random import randint, uniform
from search_node import search_node
import math
from cs1lib import set_fill_color, set_stroke_color, draw_rectangle, start_graphics, clear, set_stroke_width
# from cs1lib import *

CANVAS_HEIGHT = 400
CANVAS_WIDTH = 400

ROBOT_CENTER_X = 200
ROBOT_CENTER_Y = 200
ROBOT_LINK_LENGTH = 50

OBSTACLE_WIDTH = 5
OBSTACLE_HEIGHT = 5

class robot_maze():

	def __init__(self, obstacle_path, num_links):
		self.obstacle_path = obstacle_path
		self.num_links = num_links 
		self.robot_arm = robot_arm(ROBOT_CENTER_X, ROBOT_CENTER_Y, self.gen_arm_list(), None) 
		self.obstacle_polygons = []
		self.sol_list = None
		#Map holding vertices in free space 
		self.valid_robot_map = {}

	def PRM(self, num_vertices, k_neighbors):
		self.build_roadmap(num_vertices)

		# print("robot map: " + str(self.valid_robot_map))

		while(True):
			init_state = int(input("What is the initial state? Choose a number from 0 to " + str(num_vertices - 1) + ":"))
			depth = int(input("How deep do you want to search? "))

			key_list = list(self.valid_robot_map)
			self.sol_list = self.ids_search(key_list[init_state], depth)

			if not self.sol_list:
				print("Sorry, the initial state you chose does not have a state that deep. Please choose a different initial state or search a smaller depth.")
				continue 

			print(self.sol_list)
			angle_list = self.sol_list
			self.robot_arm.angle_list = angle_list

			start_graphics(test.draw, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

			

	def ids_search(self, init_node, depth_limit):
		for depth in range(depth_limit):
			sol = self.depth_limited_dfs(init_node, 0, depth_limit)
			if sol:
				return sol

	def depth_limited_dfs(self, init_node, current_depth, depth_limit):

		if current_depth <= depth_limit:
			if current_depth == depth_limit:
				return self.backchain(init_node)
			else: 
				init_node.color = "g"
				for neighbor in self.valid_robot_map[init_node]:
					if neighbor.color == "w" and self.is_valid_node(init_node, neighbor):
						neighbor.set_parent(init_node)
						sol = self.depth_limited_dfs(neighbor, current_depth + 1, depth_limit)
						if sol:
							return sol
				init_node.color = "b"

	def backchain(self, node):
		backchain_list = []
		while(node.parent != None):
			backchain_list.insert(0, node.get_state())
			node = node.parent
		return backchain_list

	def gen_arm_list(self):
		arm_list = []
		for i in range(self.num_links):
			arm_list.append(ROBOT_LINK_LENGTH)
		return arm_list

	def draw_obstacles(self):
		set_fill_color(0, 0, 1)
		set_stroke_color(0, 0, 1)
		set_stroke_width(1)
		file = open(self.obstacle_path, "r")
		for line in file:
			parsed_line = line.strip().split(" ")
			obstacle_x = int(parsed_line[0])
			obstacle_y = int(parsed_line[1])
			draw_rectangle(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

	def generate_obstacle_polygons(self):
		file = open(self.obstacle_path, "r")
		for line in file:
			parsed_line = line.strip().split(" ")
			obstacle_x = int(parsed_line[0])
			obstacle_y = int(parsed_line[1])
			obstacle_polygon = Polygon([(obstacle_x, obstacle_y), (obstacle_x + OBSTACLE_WIDTH, obstacle_y), (obstacle_x, obstacle_y + OBSTACLE_HEIGHT), (obstacle_x + OBSTACLE_WIDTH, obstacle_y + OBSTACLE_HEIGHT)])
			self.obstacle_polygons.append(obstacle_polygon)

	def gen_rand_vertex(self):
		"""
		Generate random vertex sample
		"""
		rand_vertex = None
		found_vertex = False
		while not found_vertex:
			vertex = []
			for j in range(self.num_links):
				rand_angle = uniform(0, 2*math.pi)
				vertex.append(rand_angle)
			rand_vertex = search_node(vertex)
			if rand_vertex not in self.valid_robot_map:
				found_vertex = True
		return rand_vertex

	def calculate_distance(self, angle_list_1, angle_list_2):
		"""
		Calculate distance between two vertices.
		Length of angle_list_1 and angle_list_2 must be the same
		@param: angle_list_1: 1st list of angle configurations
		@param: angle_list_2: 2nd list of angle configurations
		"""
		distance = 0
		if len(angle_list_1) == len(angle_list_2):
			for i in range(len(angle_list_1)):
				distance += math.fabs(angle_list_2[i] - angle_list_1[i])					
		return distance


	#Try to implement all vertices in a given raidus
	# def neighbors_in_radius(self):

	def find_k_neighbors(self, k, vertex):
		"""
		Find the K nearest neighbors of a vertex
		@param: k: number of nearest neighbors to find
		@param: vertex: vertex to find neighbors of
		"""

		#First loop to generate distances and neighbors
		dist_neighbor_list = []
		for node in self.valid_robot_map:
			if node.get_state() != vertex.get_state() and self.is_valid_node(vertex, node):
					coord_distance = self.calculate_distance(node.get_state(), vertex.get_state())
					dist_neighbor_list.append((coord_distance, node))
			dist_neighbor_list = sorted(dist_neighbor_list, key=lambda entry: entry[0])
		return dist_neighbor_list[:15]

	def detect_collissions(self):
		for polygon in self.obstacle_polygons:
			for line in self.robot_arm.polygon_list:
					if line.intersects(polygon):
						# print("COLLISSION DETECTED")
						return True
		return False

	def is_valid_node(self, curr_node, goal_node):
		"""
		Determine if we can make a valid transition from curr_node to goal_node
		@param: curr_node: starting node 
		@param: goal_node: goal node to make connection to
		"""
		curr_angle = curr_node.get_state()
		goal_angle = curr_node.get_state()
		num_steps = 10

		angle_difference_list = []

		for i in range(len(curr_angle)):
			angle_difference = curr_angle[i] - goal_angle[i]
			angle_difference_list.append(angle_difference/float(num_steps))

		for j in range(num_steps):
			for k in range(len(curr_angle)):
				curr_angle[k] += angle_difference_list[k]
			self.robot_arm.angle_list = curr_angle
			if self.detect_collissions():
				return False
		return True

	def build_roadmap(self, num_vertices):

		#Initialize the obstacle polygons to detect collisions
		self.generate_obstacle_polygons()
		
		i = 0

		#Build_roadmap algorithm
		while i < num_vertices:
			current_vertex = self.gen_rand_vertex()
			self.robot_arm.angle_list =	current_vertex.get_state()	
			self.robot_arm.create_polygon_list()
			if not self.detect_collissions():
				self.valid_robot_map[current_vertex] = []
				i += 1
				neighbor_list = self.find_k_neighbors(15, current_vertex)
				for neighbor in neighbor_list:
					self.robot_arm.angle_list = neighbor[1].get_state()
					self.robot_arm.create_polygon_list()
					if not self.detect_collissions():
						self.valid_robot_map[current_vertex].append(neighbor[1])
			# print("i: " + str(i))

	def draw(self):
		clear()
		self.draw_obstacles()
		self.robot_arm.draw()
		# self.detect_collissions()



# arm_list = [60, 60]
# angle_list = [[math.pi * 3/2, 3 * math.pi/2], [11 * math.pi, math.pi/2], [10 * math.pi, 0]]
# test_robot_arm = robot_arm(ROBOT_CENTER_X, ROBOT_CENTER_Y, arm_list, angle_list)
# start_graphics(test_robot_arm.draw, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

test = rpm("obstacle2.txt", 3)
test.PRM(100, 15)



