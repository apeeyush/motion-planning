def get_robot_data():
	with open('robot.dat') as f:
	    robot_data = f.readlines()
	numDOF = int(robot_data[0].strip())
	lengths = map(int, robot_data[1].strip().split(' '))
	numObst = int(robot_data[2].strip())
	obstacles = []
	for i in range(numObst):
		start_point = map(int, robot_data[3+2*i].strip().split(' '))
		start_point = (start_point[0], start_point[1])
		end_point = map(int, robot_data[3+2*i+1].strip().split(' '))
		end_point = (end_point[0], end_point[1])
		obstacles.append((start_point,end_point))
	return numDOF, lengths, numObst, obstacles

def get_goals_data():
	with open('goals.dat') as f:
		goals_data = f.readlines()
	goal_positions = []
	for datapoint in goals_data:
		datapoint = datapoint.strip()
		if datapoint:
			datapoint = tuple(map(int, datapoint.split(' ')))
			goal_positions.append(datapoint)
	return goal_positions
