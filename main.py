import Game
import agent

pac_game = Game.Pacman_Game()
Agent = agent.agent(pac_game)

winnum = 0
total = 0
point = 0

while True:
	pac_game.update()
	if pac_game.Control_Mode == 'AI':
		Agent.Ai_play()
	pac_game.draw()
	
		

	