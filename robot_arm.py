from cs1lib import *
import math

class robot_arm():

	def __init__(self, center_x, center_y, arm_list, angle_list):
		self.center_x = center_x
		self.center_y = center_y
		self.arm_list = arm_list
		self.angle_list = angle_list

	def draw(self):
		set_fill_color(1, 0, 0)
		set_stroke_width(20)

		start_x = self.center_x
		start_y = self.center_y
		end_x = 0
		end_y = 0
		angle_sum = 0

		# curr_rad = self.angle_list[0]
		# curr_arm = self.arm_list[0]
		# prev_

		# for i in range(len(angle_list)):

		# 	if curr_rad != self.angle_list[0]:
		# 		curr_rad += angle_list[i]
		# 	if curr_arm != self.arm_list[0]:
		# 		curr_arm = curr_arm[i]

		set_stroke_color(0, 1, 0)
		for i in range(len(self.angle_list)):
			angle_sum += self.angle_list[i]
			print("angle sum: " + str(angle_sum))
			min_angle = self.min_angle(angle_sum)
			print("min angle: " + str(min_angle))
			print("start x: " + str(start_x))
			print("start y: " + str(start_y))
			print("cos: " + str(math.cos(min_angle)))
			print("sin: " + str(math.sin(min_angle)))

			end_x = self.arm_list[i] * math.cos(min_angle) + start_x
			end_y = self.arm_list[i] * math.sin(min_angle) + start_y
			print("end x: " + str(end_x))
			print("end y: " + str(end_y))

			draw_line(start_x, start_y, end_x, end_y) 

			start_x = end_x
			start_y = end_y

		set_stroke_color(1, 0, 0)

		draw_point(self.center_x, self.center_y)

	def min_angle(self, theta):
		return min(-1 * theta, 2 * math.pi - (theta))

# arm_list = [100, 80, 150]
# angle_list = [math.pi/2, math.pi/2, 7 * math.pi/4]
arm_list = [100]
angle_list = [0]

test_arm = robot_arm(500, 500, arm_list, angle_list)

start_graphics(test_arm.draw, width = 1000, height = 1000)



