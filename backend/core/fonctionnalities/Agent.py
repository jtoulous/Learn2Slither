import numpy as np

import random
import pickle
import torch



# ['up', 'down', 'left', 'right'] == [0, 1, 2, 3]
# ['green', 'red', 'wall'] == [10, 11, 12]

class Agent:
    def __init__(self, name):
        self.name = name
        self.default_epsilon = 0.05
        self.model = QModel()

        self.prev_move = None
    

    def choose_move(self, moves_scores, epsilon=None):
        if epsilon == None:
            epsilon = self.default_epsilon

        random_number = random.random()

        if random_number < epsilon:
            random_move = random.randint(0, 3)
            return random_move, moves_scores[random_move]
        else:
            move = max(moves_scores, key=moves_scores.get)
            return move, moves_scores[move]



    def save(self, save_path):
        with open(save_path, "wb") as save_file:
            pickle.dump(self, save_file)


    @staticmethod
    def load(load_path):
        with open(load_path, "rb") as load_file:
            agent = pickle.load(load_file)
        return agent


    



class QModel:
    def __init__(self, input_size=17, output_size=4, learning_rate=0.01, gamma=0.99):
        self.learning_rate = learning_rate

        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_size, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, output_size)
        )

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = torch.nn.MSELoss()


    def predict(model_state):
        with torch.no_grad():
            q_values = self.model(model_state)
        return q_values


    def train(self, model_state, move, reward, next_state, done=False):
        q_pred = self.model(model_state)[move]

        with torch.no_grad():
            if done:
                q_target = torch.tensor(reward)
            else:
                max_next_q = torch.max(self.model(next_state))
                q_target = reward + self.gamma * max_next_q

        loss = self.loss_fn(q_pred, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()








class TrainingCycle:
#    def __init__(self, db_manager, agent, game_engin, training_params):
    def __init__(self, agent, game_engin, training_params):
        self.status = 'running'

#        self.cycle_group = f'cycle_{self.db_manager.get_nb_cycles(agent_name) + 1}'
        self.cycle_group = f'cycle_test'

#        self.db_manager = db_manager
        self.agent = agent
        self.game_engin = game_engin

        self.nb_sessions = training_params["nb_sessions"]
        self.epsilon_decay_strat = training_params["epsilon_decay_strat"]
        self.epsilon_init = training_params["epsilon_init"]
        self.epsilon_min = training_params["epsilon_min"]
        self.epsilon_decay_rate = training_params["epsilon_decay_rate"]
        self.epsilon_decay_k = training_params["epsilon_decay_k"]
        self.epsilon_decay_power = training_params["epsilon_decay_power"]

        self.current_session = 0
        self.current_epsilon = self.epsilon_init
        self.cycles_stats = []

        self.game_engin.new_game()



    def training_state(self):
        state = {'status': self.status, 'current_session': self.game_engin.game_state(), 'training_cycle_stats': self.cycles_stats, 'epsilon': self.current_epsilon}
        return state


    
    def nxt_move(self):
        breakpoint()
        model_state = Interpreter.compute_model_state(self.game_engin.game_state())
        
        moves_scores = []
        for move in range(0, 4):
            moves_scores.append(Interpreter.compute_scores(self.game_engin, move))
        chosen_move, chosen_score = self.agent.choose_move(moves_scores, epsilon=self.current_epsilon)
    
        self.game_engin.execute_move(chosen_move)

        nxt_model_state = Interpreter.compute_model_state(self.game_engin.game_state())
        if self.game_engin.status == 'end':
            agent.model.train(model_state, chosen_move, chosen_score, nxt_model_state)
        else:
            agent.model.train(model_state, chosen_move, chosen_score, nxt_model_state, done=True)

        if self.game_engin.status == 'end':
            self.cycles_stats.append(self.game_engin.game_state())
#            self.db_manager.save_game_results(self.cycle_idx, self.agent.name, self.game_engin.game_state())

            if self.current_session < self.nb_sessions:
                self.current_session += 1
                self.current_epsilon = self.update_epsilon()
                self.game_engin.new_game()

            else: 
                self.status = 'done'


    def update_epsilon(self):
        total_sessions = self.nb_sessions
        current_session = self.current_session
        decay_strat = self.epsilon_decay_strat

        if decay_strat == 'linear':
            return max(self.epsilon_min, self.epsilon_init - (current_session / total_sessions) * (self.epsilon_init - self.epsilon_min))       

        elif decay_strat == 'exponential':
            return max(self.epsilon_min, self.epsilon_init * (self.epsilon_decay_rate ** current_session))

        elif decay_strat == 'polynomial':
            return max(self.epsilon_min, self.epsilon_init / ((1 + self.epsilon_decay_k * current_session) ** self.epsilon_decay_power))

        elif decay_strat == 'constant':
            return self.current_epsilon




class Interpreter:
#    model_state = [
#        "distance_first_obj_left",
#        "type_first_obj_left",
#        "distance_second_obj_left",
#        "type_second_obj_left",
#
#        "distance_first_obj_right",
#        "type_first_obj_right",
#        "distance_second_obj_right",
#        "type_second_obj_right",
#        
#        "distance_first_obj_up",
#        "type_first_obj_up",
#        "distance_second_obj_up",
#        "type_second_obj_up",
#        
#        "distance_first_obj_down",
#        "type_first_obj_down",
#        "distance_second_obj_down",
#        "type_second_obj_down",
#
#        "latest_global_direction",
#    ]

    @staticmethod
    def compute_model_state(game_state):
        model_state = np.zeros(17)

        y_head, x_head = game_state['snake_head']
        horizontal_view = game_state['horizontal_view']
        vertical_view = game_state['vertical_view']
        
        #Check left
        model_state[0], model_state[1] = Interpreter.distance_n_type__nxt_obj('left', horizontal_view, x_head) 
        model_state[2], model_state[3] = Interpreter.distance_n_type__nxt_obj('left', horizontal_view, x_head, skip_first=True)

        #Check right
        model_state[4], model_state[5] = Interpreter.distance_n_type__nxt_obj('right', horizontal_view, x_head) 
        model_state[6], model_state[7] = Interpreter.distance_n_type__nxt_obj('right', horizontal_view, x_head, skip_first=True)

        #Check top
        model_state[8], model_state[9] = Interpreter.distance_n_type__nxt_obj('up', vertical_view, y_head) 
        model_state[10], model_state[11] = Interpreter.distance_n_type__nxt_obj('up', vertical_view, y_head, skip_first=True)

        #Check bot
        model_state[12], model_state[13] = Interpreter.distance_n_type__nxt_obj('down', vertical_view, y_head) 
        model_state[14], model_state[15] = Interpreter.distance_n_type__nxt_obj('down', vertical_view, y_head, skip_first=True)

        model_state[16] = game_state['prev_global_direction']

        return model_state


    @staticmethod
    def distance_n_type__nxt_obj(iter_direction, view, start_idx, skip_first=False):
        nxt_object_type = -1
        nxt_object_normalised_dist = -1

        skipped_first = False

        cursor = start_idx - 1 if (iter_direction == 'left' or iter_direction == 'up') else start_idx + 1
        while cursor < len(view) - 1 and cursor > 0:

            if view[cursor] != '0':

                if skip_first is True and skipped_first is False:
                    skipped_first = True
                else:
                    break

            cursor = cursor - 1 if (iter_direction == 'left' or iter_direction == 'up') else cursor + 1



        nxt_object_type = Interpreter.cell_type(view[cursor])
        nxt_object_normalised_dist = abs(cursor - start_idx) / (len(view) - 1)

        return nxt_object_normalised_dist, nxt_object_type


    @staticmethod
    def cell_type(cell_content):
        cell_types = {
            '0': 10,
            'G': 11,
            'R': 12, 
            'S': 13,
            'W': 14,
            'H': 15,
        }
        return cell_types[cell_content]




    @staticmethod
    def compute_scores(game_engin, move):
        score = 0

        y_head, x_head = game_engin.map.snake_head
        nxt_y_head = y_head - 1 if move == 0 else y_head + 1 if move == 1 else y_head
        nxt_x_head = x_head - 1 if move == 2 else x_head + 1 if move == 3 else x_head 

        snake_head = game_engin.map.snake_head
        nxt_snake_head = (nxt_y_head, nxt_x_head)

        # Rewards + Penalties
        score += Interpreter.nxt_cell_type_score(game_engin, nxt_snake_head)
        score += Interpreter.closer_to_green_score(move, game_engin, nxt_snake_head, snake_head)

        return score


    @staticmethod
    def nxt_cell_type_score(game_engin, nxt_snake_head):
        grid = game_engin.map.grid
        
        nxt_cell = grid[nxt_snake_head]

        if nxt_cell == 'G':
            return 30 

        elif nxt_cell == 'R':
            return -15
        
        elif nxt_cell == 'W' or nxt_cell == 'S':
            return -200
        
        else:
            return -1


    @staticmethod
    def closer_to_green_score(move, game_engin, nxt_snake_head, snake_head):
        score = 0
        horizontal_view, vertical_view = game_engin.get_snake_view()
        
        target_view = horizontal_view if move == 2 or move == 3 else vertical_view
        cursor = nxt_snake_head[1] if move == 2 or move == 3 else nxt_snake_head[0]

        closer_to_green = False
        object_in_between = None

        while cursor > 0 and cursor < len(target_view) - 1:
            if target_view[cursor] == 'G':
                closer_to_green = True
                break                

            if move == 0 or move == 2:
                cursor -= 1
            else:
                cursor += 1

        if closer_to_green:
            score += 15
            if object_in_between:
                if object_in_between == 'S':
                    score -= 10
                elif object_in_between == 'R':
                    score -= 5

        return score
