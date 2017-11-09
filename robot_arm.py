from cs1lib import set_fill_color, set_stroke_color, draw_line, draw_point, set_stroke_width, clear  
import math
from shapely.geometry import Point, LineString

class robot_arm():

	def __init__(self, center_x, center_y, arm_list, angle_list):
		self.center_x = center_x
		self.center_y = center_y
		self.angle_index = 0
		self.arm_list = arm_list
		self.angle_list = angle_list
		self.compeleted_animations = [False for i in range(len(arm_list))]
		print(self.compeleted_animations)
		self.polygon_list = []
		self.completed_animations = 0

	def create_polygon_list(self):
		self.polygon_list = []

		start_x = self.center_x
		start_y = self.center_y
		end_x = 0
		end_y = 0
		angle_sum = 0

		for i in range(len(self.angle_list)):
			angle_sum += self.angle_list[i]
			min_angle = self.min_angle(angle_sum)

			end_x = self.arm_list[i] * math.cos(min_angle) + start_x
			end_y = self.arm_list[i] * math.sin(min_angle) + start_y

			#Create a list of all arms as polygons from shapely
			line_string = LineString([Point(start_x, start_y), Point(end_x, end_y)])
			self.polygon_list.append(line_string)
	
			start_x = end_x
			start_y = end_y
			

	def draw(self):
		#On each draw, empty polygon_list
		self.polygon_list = []

		start_x = self.center_x
		start_y = self.center_y
		end_x = 0
		end_y = 0
		angle_sum = 0


		for i in range(len(self.angle_list[self.angle_index])):
			# print("i: " + str(i))
			curr_vertex = self.angle_list[self.angle_index]
			set_fill_color(1, 0, 0)
			set_stroke_color(1, 0, 0)
			angle_sum += curr_vertex[i]
			min_angle = self.min_angle(angle_sum)


			end_x = self.arm_list[i] * math.cos(min_angle) + start_x
			end_y = self.arm_list[i] * math.sin(min_angle) + start_y

			draw_line(start_x, start_y, end_x, end_y) 

			set_fill_color(0, 1, 0)
			set_stroke_color(0, 1, 0)
			# set_stroke_width(5)
			draw_point(end_x, end_y)

			#Create a list of all arms as polygons from shapely
			line_string = LineString([Point(start_x, start_y), Point(end_x, end_y)])
			self.polygon_list.append(line_string)
	
			start_x = end_x
			start_y = end_y

		draw_point(self.center_x, self.center_y)

		# self.animate_path()

		if self.angle_index < len(self.angle_list) - 1:
			self.angle_index += 1

	def animate_path(self):
		if self.angle_index < len(self.angle_list) - 1:
			curr_index = self.angle_index
			next_index = self.angle_index + 1
			for i in range(len(self.angle_list[curr_index])):

				curr_angle = self.angle_list[curr_index][i]
				goal_angle = self.angle_list[next_index][i]
				#Check if current angle is greater than or less than goal angle
				counter_clock_angle_diff = math.fabs(curr_angle - goal_angle)
				clockwise_angle_diff = (2 * math.pi) - math.fabs(curr_angle - goal_angle)

				if clockwise_angle_diff < counter_clock_angle_diff:
					self.angle_list[curr_index][i] -= 0.1
					if self.angle_list[curr_index][i] >= self.angle_list[next_index][i]:
						self.completed_animations += 1

				else:
					self.angle_list[curr_index][i] += 0.1
					if self.angle_list[curr_index][i] >= self.angle_list[next_index][i]:
						self.completed_animations += 1

			if self.completed_animations == len(self.angle_list[curr_index]):
				self.completed_animations = 0
				print("YO WHAT THE")
				# self.angle_index += 1


	def min_angle(self, theta):
		theta = theta % (2 * math.pi)
		# print("THETA: " + str(theta))
		return min(-1 * theta, 2 * math.pi - (theta))



