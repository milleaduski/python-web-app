## PYTON
# Define Class
# class Team():
# 	teamName = 'Arsenal'

# 	def getTeam(self, team):
# 		self.teamName = team
# 		return self.teamName

# ## Outside Class
# team = Team()
# print(team.getTeam('Liverpool'))

class Team():
	teamName = ''
	player = ''

	def __init__(self, team, player):
		self.teamName = team
		self.player = player

	def getTeam(self):
		return self.teamName

	def getPlayer(self):
		return self.player

team = Team('Liverpool', 'Roberto Firmino')
print(team.getPlayer() + ' is the player from ' + team.getTeam())