import random

class agent():
	def __init__(self, Game):
		self.game = Game
			
	def minmax(self, maxdepth):
		def dfs(now_player, state, depth):
			
			if depth == maxdepth or self.game.if_game_over(state)!='No':
				#print(depth)
				return self.game.get_value(state)
			if now_player == 'Pacman':
				action_list = self.game.get_legal_action(state[0])
				v_list = []
				
				for i in action_list:
					v_list.append((dfs('Ghost', self.game.get_next_state(state, now_player, i), depth+1),i))
					
				if depth == 0:
					return max(v_list)[1]
				else:
					return max[v_list][0]
			else:
				action_list1 = self.game.get_legal_action(state[1])
				action_list2 = self.game.get_legal_action(state[2])
				v_list = []
				for i in action_list1:
					for j in action_list2:
						v_list.append(dfs('Ghost', self.game.get_next_state(state, now_player, i+j), depth+1))
				return sum(v_list)/len(v_list)
		return dfs('Pacman', self.game.get_now_state(), 0)
	
		
	def Ai_play(self):
		if self.game.pacman.if_can_control() == True:
			act = self.minmax(3)
			#print(act)
			self.game.pacman.move_to(act)