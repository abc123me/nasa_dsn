from cli import colors

class StatusError(OSError):
	def __init__(self, source, problem, isSevere = False):
		self.source = source
		self.problem = problem
		self.isSevere = isSevere
	def __str__(self, ansi = False):
		if(ansi):
			return colors.red + self.source + ": " + self.problem + colors.reset
		else:
			return self.source + ": " + self.problem
