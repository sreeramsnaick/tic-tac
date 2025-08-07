import random
class State:
	def __init__(self, current_player, state):
		self.current_player = current_player
		self.state = state
class Game:
	def __init__(self):
		self.initial = [["","",""],
						["","",""],
						["","",""]]
		self.state = State("x", self.initial)
		while self.terminate(self.state) == False:
			for i in self.state.state:
				print(i)
			if self.state.current_player == "x":
				row, col = map(int, input("enter row and col:").split())
				new_state = self.result(self.state, (row,col))
				new_player = self.player(self.state)
				self.state = State(new_player, new_state)
			elif self.state.current_player == "o":
				actions = self.actions(self.state)
				results = []
				posse = []
				for row,col in actions:
					res = self.result(self.state, (row,col))
					player = self.player(self.state)
					state = State(player, res)
					results.append((state, (row,col)))
				steps = 0
				for i in results:		
					min_value = self.min_value(i[0], self.player(self.state), steps)
					posse.append((min_value[0], i[1], min_value[2], min_value[3]))
				
				sort = sorted(posse, key=lambda x: (x[0], x[2]))
				new_sort = [i for i in sort if i[1] is not None]
				
				best = [state for state in new_sort if state[0] == new_sort[0][0]]
				for i in best:
					print(i)
				weight = [i for i in range(1,len(best)+1)][::-1]
				chosen = random.choices(best, weights=weight)
				result = self.result(self.state, chosen[0][1])
				new_player = self.player(self.state)
				self.state = State(new_player,  result)
				
		for i in self.state.state:
			print(i)

	def player(self,state):
		if state.current_player == "x":
			return "o"
		else:
			return "x"

	def actions(self,state):
		return [(i, j) for i in range(3) for j in range(3) if state.state[i][j] == ""]

	def result(self, state, action):
		new_state = [row[:] for row in state.state]
		new_state[action[0]][action[1]] = str(state.current_player)
		return new_state

	def terminate(self, state):
		if self.utility(state, "x") or self.utility(state, "o"):
			return True
		for i in self.state.state:
			for j in i:
				if j == "":
					return False

		return True

	def utility(self, state, player):
		for row in state.state:
			if all(cell == player for cell in row):
				if player == "x":
					return 1
				elif player == "o":
					return -1
		for col in range(3):
			if all(state.state[row][col] == player for row in range(3)):			
				if player == "x":				
					return 1
				elif player == "o":				
					return -1	
		if all(state.state[i][i] == player for i in range(3)):
			if player == "x":		
				return 1
			elif player == "o":		
				return -1
		if all(state.state[i][2-i] == player for i in range(3)):
			if player == "x":		
				return 1
			elif player == "o":		
				return -1

		return 0

	def min_value(self,state, player, steps):
		v = float("inf")
		best_move = None
		new_state = state
		step = steps
		if self.terminate(state):
			last_player = "x" if player == "o" else "o"
			return (self.utility(state, last_player), best_move, step, state.state)
		actions = self.actions(state)
		
		for row, col in actions:	
			new_result = self.result(state, (row,col))
			new_player = "x" if player == "o" else "o"
			new_state = State(new_player, new_result)
			step+= 1
			max_val = self.max_value(new_state, new_player, step)
			if max_val[0] < v:
				v = min(v, max_val[0])
				best_move = max_val[1] if max_val[1] is not None else (row, col)

		return (v, best_move, step, new_state.state)

	def max_value(self,state, player, steps):
		v = float("-inf")
		best_move = None
		step = steps
		new_state = state
		if self.terminate(state):
			last_player = "x" if player == "o" else "o"
			return (self.utility(state, last_player), best_move, step, state.state)
		actions = self.actions(state)
		for row, col in actions:	
			new_result = self.result(state, (row,col))
			new_player = "x" if player == "o" else "o"
			new_state = State(new_player, new_result)
			step += 1
			min_val = self.min_value(new_state, new_player, step)
			if min_val[0] > v:
				v = max(v, min_val[0])
				best_move = min_val[1] if min_val[1] is None else (row, col)

		return (v, best_move, step, new_state.state)


Game()