import random
import pickle

from utils.policy import InstantReward, FutureReward
from utils.tools import XplorationOrXplotation, GetState
from utils.logs import PrintLog


class Agent():
    def __init__(self, arguments=None, config=None):
        self.q_table = Qtable(actions=arguments.actions)
        self.learning_rate = arguments.alpha
        self.discount = arguments.discount
        self.epsilon = arguments.epsi_max
        self.epsi_max = arguments.epsi_max
        self.epsi_min = arguments.epsi_min
        self.decay_strat = arguments.epsi_decay


    def NextMove(self, game_engin, train):
        last_move = game_engin.last_move
        state = GetState(game_engin.map, game_engin.snake_head, game_engin.n_cells)

        if state not in self.q_table.table:
            self.q_table.NewState(state)

        x_type = XplorationOrXplotation(self.epsilon)
        nxt_move = self.GetMove(game_engin, x_type, game_engin.last_move, state, train)
        return nxt_move
        
    def GetMove(self, game_engin, x_type, last_move, state, train):
        state_scores = self.q_table.table[state]
        possible_moves = ['up', 'down', 'left', 'right']
        if last_move == 'right':
            possible_moves.remove('left')
        elif last_move == 'left':
            possible_moves.remove('right')
        elif last_move == 'up':
            possible_moves.remove('down')
        elif last_move == 'down':
            possible_moves.remove('up')

#        for m in possible_moves:
#            PrintLog(f'reward {m} => {self.CalcScore(game_engin, m, state)}')
        if train == True:
            self.q_table.table[state][possible_moves[0]] = self.q_table.table[state][possible_moves[0]] + self.learning_rate * (self.CalcScore(game_engin, possible_moves[0], state) - self.q_table.table[state][possible_moves[0]])    
            self.q_table.table[state][possible_moves[1]] = self.q_table.table[state][possible_moves[1]] + self.learning_rate * (self.CalcScore(game_engin, possible_moves[1], state) - self.q_table.table[state][possible_moves[1]])    
            self.q_table.table[state][possible_moves[2]] = self.q_table.table[state][possible_moves[2]] + self.learning_rate * (self.CalcScore(game_engin, possible_moves[2], state) - self.q_table.table[state][possible_moves[2]])    

        if x_type == 'Xploration':
            move = possible_moves[random.randint(0, 2)]

        elif x_type == 'Xplotation':
            max_score = state_scores[possible_moves[0]]
            move = possible_moves[0]
#            if train == True:
#                self.q_table.table[state][move] = self.q_table.table[state][move] + self.learning_rate * (self.CalcScore(game_engin, move, state) - self.q_table.table[state][move])
            for m in possible_moves:
                total_score = self.CalcScore(game_engin, m, state)
                if state_scores[m] > max_score:
                    move = m
                    max_score = state_scores[m]
        return move

    def CalcScore(self, game_engin, move, state):#Nouvelle valeur = Ancienne valeur + learning_rate * ((Récompense immédiate + Valeur future estimée * facteur d'actualisation) - Ancienne valeur)
        instant_reward = InstantReward(game_engin, move)
        future_reward = FutureReward(game_engin, move, self.q_table)
        return instant_reward + future_reward * self.discount

    def Update(self, session, max_sessions):
        self.epsilon = self.epsi_max - (self.epsi_max - self.epsi_min) * (session / max_sessions)

#        if session % 100 == 0 and self.epsilon > 0.1: 
#            self.epsilon = round(self.epsilon - 0.1, 1)

    @staticmethod
    def LoadConfig(config_file): #to do
        with open(config_file, "rb") as file:
            agent = pickle.load(file)
            agent.epsilon = 0
        return agent


    def SaveConfig(self, config_file):
        with open(config_file, "wb") as file:
            pickle.dump(self, file)


class Qtable():
    def __init__(self, actions=None, file=None):
        if file == None:
            self.n_state = 0
            self.actions = actions
            self.n_action = len(self.actions)
            self.table = {}

#        else:
#            self.table, self.actions, self.n_state = self.LoadTable(file)

    def NewState(self, state):
        self.table[state] = {'up': 0, 'down': 0, 'right': 0, 'left': 0}

    def LoadTable(self, file): #to do
        pass

    def SaveTable(self, file): #to do
        pass