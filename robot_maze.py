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
		self.sol_list = []
		#Map holding vertices in free space 
		self.valid_robot_map = {}

	def PRM(self, num_vertices, k_neighbors):
		self.build_roadmap(num_vertices)

		# print("robot map: " + str(self.valid_robot_map))

		while(True):
			init_state = int(input("What is the initial state? Choose a number from 0 to " + str(num_vertices - 1) + ":"))
			goal_state = int(input("What is the goal state? Choose a number from 0 to " + str(num_vertices - 1) + ":"))

			key_list = list(self.valid_robot_map)
			self.sol_list = self.ids_search(key_list[init_state], key_list[goal_state], 100)

			print(self.sol_list)
			angle_list = self.sol_list
			self.robot_arm.angle_list = angle_list

			start_graphics(test.draw, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

			

	def ids_search(self, init_node, goal_node, depth_limit=100):
		for depth in range(depth_limit):
			sol = self.depth_limited_dfs(init_node, goal_node, 0, depth)
			if sol:
				return sol

	def depth_limited_dfs(self, init_node, goal_node, current_depth, depth_limit=100):

		if current_depth <= depth_limit:
			if init_node.get_state() == goal_node.get_state():
				return self.backchain(goal_node)
			else: 
				init_node.color = "g"
				for neighbor in sorted(self.valid_robot_map[init_node], key=lambda cost: cost[1]):
					if neighbor[0].color == "w":
						neighbor[0].set_parent(init_node)
						sol = self.depth_limited_dfs(neighbor[0], goal_node, current_depth + 1)
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
			rand_vertex = search_node(tuple(vertex))
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

	def find_k_neighbors(self, k, vertex):
		"""
		Find the K nearest neighbors of a vertex
		@param: k: number of nearest neighbors to find
		@param: vertex: vertex to find neighbors of
		"""

		#First loop to generate distances and neighbors
		dist_neighbor_list = []
		neighbor_list = []
		for node in self.valid_robot_map:
			if node.get_state() != vertex.get_state():
				coord_distance = self.calculate_distance(node.get_state(), vertex.get_state())
				dist_neighbor_list.append((coord_distance, node))
		dist_neighbor_list = sorted(dist_neighbor_list, key=lambda entry: entry[0])
		# print("dist neighbor list: " + str(dist_neighbor_list))

		#Second loop to append just the vertices in correct order
		for i in range(len(dist_neighbor_list)):
			if i < 15:
				neighbor_list.append(dist_neighbor_list[i][1])
			else:
					break
		return neighbor_list

	def detect_collissions(self):
		for polygon in self.obstacle_polygons:
			for line in self.robot_arm.polygon_list:
					if line.intersects(polygon):
						# print("COLLISSION DETECTED")
						return True
		return False

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
				# print("neighbor list length: " + str(len(neighbor_list)))
				for neighbor in neighbor_list:
					self.robot_arm.angle_list = neighbor.get_state()
					self.robot_arm.create_polygon_list()
					if not self.detect_collissions():
						angle_distance = self.calculate_distance(current_vertex.get_state(), neighbor.get_state())
						self.valid_robot_map[current_vertex].append((neighbor, angle_distance))
						self.valid_robot_map[neighbor].append((current_vertex, angle_distance))

	def draw(self):
		clear()
		self.draw_obstacles()
		self.robot_arm.draw()
		# self.detect_collissions()



# arm_list = [60, 60]
# angle_list = [[math.pi * 3/2, 3 * math.pi/2], [11 * math.pi, math.pi/2], [10 * math.pi, 0]]
# test_robot_arm = robot_arm(ROBOT_CENTER_X, ROBOT_CENTER_Y, arm_list, angle_list)
# start_graphics(test_robot_arm.draw, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

test = robot_maze("obstacle2.txt", 3)
test.PRM(30, 15)



