import sys

helpstr='''
	This BrainF interpeter has BF a little BF III and normal BF.
	
	Usage: [args] or [args]=[arg]
	
	-c		List included characters. 
	-n		Change new line(10) to null(0). 
	-i		Show the compiled code. 
	-s		Save the compiled code to file set. [Filename]
	-f		Open and run code from file. [Filename]
	-w		No allowing numbers below 0 or above 255. 
	-h		This help text. 
'''
commandsstr='''
	Avalible characters and a breif description of them are listed below. 
	
	>		Progresses forward one cell. 
	<		Goes to the previous cell. 
	+		Adds one to the current cell. 
	-		Subtracts one from the current cell. 
	,		Gets input of character from user. 
	.		Prints current cells character
				(ie. '+++++++++.' prints '	' or \t).
	[		Skips to the matching ']' if current cell's value is 0 
				otherwise continue. 
	]		Goes back to the matching '[' if current cell's value 
				is not 0 otherwise continue. 
	0-F		Current cell gets asigned the hex value of character 
				multiplide by 16(ie. '5' is 80, 'f' is 240). 
	@		End program or python equivilant of 'quit(0)'.
'''

newlinetranc = False
showcode = False
savecode = ""
filecode = ""
numdensify = False

for x in sys.argv:
	if x == '-n':
		newlinetranc = True
	if x == '-i':
		showcode = True
	if x == '-w':
		numdensify = True
	if x.strip('-').startswith('h') == True:
		print(helpstr)
		quit(0)
	if x == '-c':
		print(commandsstr)
		quit(0)
	if x.split('=')[0]=='-s':
		savecode = x.split('=')[1]
	if x.split('=')[0]=='-f':
		filecode = x.split('=')[1]

def u_input(msg):
	i = input(msg)
	if i == '' and newlinetranc:
		i = '\x00'
	if i == '' and newlinetranc == False:
		i = ' '
	return i

class BF:
	def __init__(self):
		self.commands = {'>': 'curcell += 1;',
						 '<': 'curcell -= 1;',
						 '+': 'arrayed[curcell] += 1;',
						 '-': 'arrayed[curcell] -= 1;',
						 '.': 'sys.stderr.write(chr(arrayed[curcell]));',
						 ',': 'arrayed[curcell] = ord(u_input("> ")[0]);',
						 '[': 'while arrayed[curcell] != 0:',
						 ']': '',
						 'a': 'arrayed[curcell] = 160;',
						 'b': 'arrayed[curcell] = 176;',
						 'c': 'arrayed[curcell] = 192;',
						 'd': 'arrayed[curcell] = 208;',
						 'e': 'arrayed[curcell] = 224;',
						 'f': 'arrayed[curcell] = 240;',
						 '@': 'quit(0);'
		}
		for x in range(9):
			self.commands[str(x)] = 'arrayed[curcell] = '+str(x*16)
		
	def compileCode(self, code):
		compiledCode = "curcell = 0;\narrayed = [0 for x in range(30000)];\n"
		tabAmount = 0
		for char in code:
			if char in self.commands:
				compiledCode += ("\t"*tabAmount) + self.commands[char] + "\n"
				if char == '[':
					tabAmount += 1
				if char == ']':
					tabAmount -= 1
			else:
				print("Error!\n\tThe character, '"+char+"' is not a BF command!")
				quit(0)
		return compiledCode
		
	def run(self, code):
		print("Compiling...")
		compiled = self.compileCode(code)
		print("Compiled! Now running.")
		if showcode == True:
			print("Compiled Code:\n"+compiled+"\n")
		if savecode != "":
			print("Saving code to file: '"+savecode+"'.")
			open(savecode,'w').write(compiled)
			print("Done. Now continuing.")
		exec(compiled)


if __name__ == '__main__':
	try:
		bf = BF()
		if filecode != "":
			bf.run(open(filecode,'r').read())
		else:
			bf.run(input('Enter your code: '))
		sys.stderr.write('\n')
	except KeyError:
		print('Code works! Until...character '+str(bf.codechar+1))
		quit(0)