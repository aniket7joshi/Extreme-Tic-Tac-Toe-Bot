import random
import datetime
import copy

class Team10:

	def __init__(self):
		
		self.diamond_state = [
			[
				[0,1],[1,0],[1,2],[2,1] ],
			[ 
				[0,2],[1,1],[1,3],[2,2] ],
			[
				[1,1],[2,1],[2,2],[3,1] ],
			[
				[1,2],[2,1],[2,3],[3,2] ]
		]

		self.centrePos = [(1,1),(1,2),(2,1),(2,2)]
		self.edgePos = [(0,1),(0,2),(1,0),(2,0),(3,1),(3,2),(2,3),(1,3)]
		self.cornerPos = [(0,0),(3,0),(3,3),(0,3)]

		
		self.ALPHA = -100000000
		self.BETA = 100000000
		
		self.timeLimit = datetime.timedelta(seconds = 14.9)
		self.begin = 0
		
		self.two_value = 10
		self.three_value = 100
		self.four_value = 1000
		
		self.dict = {}
		self.hash_board = dict()
		self.length = 0
		self.zobrist = []
		for i in xrange(16):
			self.zobrist.append([])
			for j in xrange(16):
				self.zobrist[i].append([])
				for k in xrange(2):
					self.zobrist[i][j].append(random.randint(0, 0x10000000000000000L))

		self.WIN_UTILITY = 1000000
		self.LOST_UTILTIY = -1000000
		self.cell_win = 1000


	def stateback(self, p_board, i, j):
		p_board.board_status[i][j] = '-'
		p_board.block_status[i/4][j/4] = '-'

	def isValidTime(self):
		if datetime.datetime.utcnow() - self.begin > self.timeLimit:
			return 1
		return 0

	def minimax(self,old_move, depth, max_depth, alpha, beta, isMax, p_board, p_block, player_flag, flag2, best_node):
		if self.isValidTime():
			return (-111,(-1,-1))
		terminal_state = p_board.find_terminal_state()
		if terminal_state[1][0] == 'W' :
			if terminal_state[0] == player_flag :
				return (self.WIN_UTILITY,old_move)
			elif terminal_state[0] == flag2 :
				return (self.LOST_UTILTIY,old_move)
		if depth == max_depth:
			# print "Inside Max Depth"
			hash_value = 0
			for i in xrange(16):
				for j in xrange(16):
					if p_board.board_status[i][j] != '-':
						if p_board.board_status[i][j] == player_flag:
							hash_value = hash_value ^ self.zobrist[i][j][0]
						else:
							hash_value = hash_value ^ self.zobrist[i][j][1]

			if hash_value in self.hash_board:
				# print "in Hash function"
				# print(self.hash_board[hash_value])
				# print(best_node)
				if player_flag == 'x':
					return (self.hash_board[hash_value],best_node)
				return (-self.hash_board[hash_value],best_node)


			self.hash_board[hash_value] = self.checkBoardUtility(p_block,p_board) + self.checkBlockUtility(p_block,p_board)
			if player_flag == 'x':
				# print(self.hash_board[hash_value])
				return (self.hash_board[hash_value],best_node)
			return (-self.hash_board[hash_value],best_node)

		
		
		else:
			validMoves = p_board.find_valid_move_cells(old_move)
			random.shuffle(validMoves)
			if len(validMoves) == 0:
				utility = self.checkOverallUtility(p_block,p_board)
				negUtility = -utility
				if player_flag == 'o':
					return (negUtility,old_move)
				return (utility,old_move)
			for move in validMoves:
				if isMax is True:
					p_board.update(old_move,move,player_flag)
				else:
					p_board.update(old_move,move,flag2)
				if isMax is True:
					score = self.minimax (move,depth+1,max_depth,alpha,beta,False,p_board,p_block,player_flag,flag2,best_node)
					if self.isValidTime():
						i,j = move[0],move[1]
						self.stateback(p_board, i, j)
						return (-111,(-1,-1))
					if (score[0] > alpha):
						best_node = move
						alpha = max(alpha,score[0])
				else:
					score = self.minimax (move,depth+1,max_depth,alpha,beta,True,p_board,p_block,player_flag,flag2,best_node)
					if self.isValidTime():
						i,j = move[0],move[1]
						self.stateback(p_board, i, j)
						return (-111,(-1,-1))
					if (score[0] < beta):
						beta = score[0]
						best_node = move
				i,j = move[0],move[1]
				self.stateback(p_board, i, j)
				if (alpha >= beta):
					break
			if isMax is True:
				return (alpha, best_node)
			else:
				return(beta, best_node)

	def checkBlockUtility(self,block,board) :
		ans = 0
		utilityX = 100*self.block_utility(board.block_status,'x',0)
		utilityO = 100*self.block_utility(board.block_status,'o',0)
		ans = ans + utilityX - utilityO 
		return ans	

	def checkOverallUtility(self,block,board):
		return self.checkBlockUtility(block,board) + self.checkBoardUtility(block,board)

	def checkBoardUtility(self,block,board):
		ans = 0
		temp_block = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in xrange(0,4,1):
			for j in xrange(0,4,1):
				if(board.block_status[i][j] == '-'):
					for l in range(4):
						for k in range(4):
							temp_block[l][k] = board.board_status[4*i+k][4*j+l]
					utilityX = self.block_utility(temp_block,'x',1)
					utilityO = self.block_utility(temp_block,'o',1)
					ans = ans + utilityX - utilityO 
				elif(board.block_status[i][j] == 'x'):
					ans = ans + 1000
				elif(board.block_status[i][j] == 'o'):
					ans = ans - 1000
		return ans

	def move(self,board,old_move,player_flag) :
		self.timeLimit = datetime.timedelta(seconds = 14.9)
		
		maxDepth = 3
		self.begin = datetime.datetime.utcnow()
		flag2 = 'x'
		temp_board = copy.deepcopy(board)
		if player_flag == 'x' :
			flag2 = 'o'
		while self.isValidTime()==0:
			ret = self.minimax(old_move,0,maxDepth,self.ALPHA,self.BETA,True,temp_board, (1,1), player_flag, flag2, (7,7))
			if ret[0] != -111 :
				best_node = ret[1]
			maxDepth = maxDepth + 1
		return best_node

	def block_utility(self,block,flag,param):
		
		ans = 0
		countVeryHigh = 0
		countHigh = 0
		countLow = 0
		block_1 = tuple([tuple(block[i]) for i in range(4)])
		if (block_1, flag) in self.dict:
			ret = self.dict[(block_1, flag)]
			return ret
		
				
		
		for cord in self.centrePos:
			if block[cord[0]][cord[1]]==flag:
				countVeryHigh =countVeryHigh+1

		for cord in self.edgePos:
				if block[cord[0]][cord[1]]==flag:
					countHigh=countHigh+1
		for cord in self.cornerPos:
			if block[cord[0]][cord[1]]==flag:
				countLow=countLow+1


		if param == 0:
			value = 5
			ans = ans + value*((countVeryHigh*3) + (countHigh*2) + (countLow))
		if param == 1:
			value = 1
			ans = ans + value*((countVeryHigh*3) + (countHigh*2) + (countLow))

		if flag == 'x':
			flag2 = 'o'
		else:
			flag2 = 'x'
		
		playerFlag = 0
		oppFlag = 0			
		for row in range(4):
			for col in range(4):
				if(block[row][col] is flag):
					playerFlag = playerFlag+ 1
				elif((block[row][col] == flag2) or (block[row][col] == 'd')):
					oppFlag += 1
			if not oppFlag:
				if playerFlag == 4 :
					ans = self.four_value
				elif playerFlag == 3 :
					ans += self.three_value
				elif playerFlag == 2 :
					ans += self.two_value
			playerFlag = 0
			oppFlag = 0
		for col in range(4):
			for row in range(4):
				if(block[row][col] is flag):
					playerFlag += 1
				elif((block[row][col] is flag2) or (block[row][col] is 'd')):
					oppFlag += 1
			if not oppFlag:
				if playerFlag == 4:
					ans = self.four_value
				elif playerFlag == 3:
					ans += self.three_value
				elif playerFlag == 2:
					ans += self.two_value
			playerFlag = 0
			oppFlag = 0
		for di in self.diamond_state:
			for cell in di:
				i = cell[0]
				j = cell[1]
				if block[i][j] is flag:
					playerFlag+=1
				elif (block[i][j] is flag2) or (block[i][j] is 'd'):
					oppFlag+=1
					continue
			if not oppFlag:
				if playerFlag == 2:
					ans += self.two_value
				elif playerFlag == 3:
					ans += self.three_value
				elif playerFlag == 4:
					ans = self.four_value
			playerFlag = 0
			oppFlag = 0
			   
		self.dict[(block_1, flag)] = ans
		return self.dict[(block_1, flag)]			
