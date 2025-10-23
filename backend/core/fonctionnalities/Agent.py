import random
import pickle

import torch



# ['up', 'down', 'left', 'right'] == [0, 1, 2, 3]

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
            return move, moves_scores[move]
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
    def __init__(self, db_manager, agent, game_engin, training_params):
        self.status = 'running'

        self.cycle_group = f'cycle_{self.db_manager.get_nb_cycles(agent_name) + 1}'

        self.db_manager = db_manager
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
        self.current_epsilon = epsilon_init
        self.cycles_stats = []

        self.game_engin.new_game()



    def training_state(self):
        state = {'status': self.status, 'current_session': self.game_engin.game_state(), 'training_cycle_stats': self.cycles_stats, 'epsilon': self.current_epsilon}
        return state


    
    def nxt_move(self):
        model_state = Interpreter.compute_model_state(self.game_engin.game_state())
        
        for move in range(0, 4):
            moves_scores = Interpreter.compute_scores(model_state, move)

        chosen_move, chosen_score, nxt_state = self.agent.choose_move(moves_scores, epsilon=self.current_epsilon)
        self.game_engin.execute_move(chosen_move)

        nxt_model_state = Interpreter.compute_model_state(nxt_state)

        if self.game_engin.status == 'end':
            agent.model.train(model_state, chosen_move, chosen_score, nxt_model_state)
        else:
            agent.model.train(model_state, chosen_move, chosen_score, nxt_model_state, done=True)

    
        
        if self.game_engin.status == 'end':
            self.cycles_stats.append(self.game_engin.game_state())
            self.db_manager.save_game_results(self.cycle_idx, self.agent.name, self.game_engin.game_state())

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



    model_state = [
        "distance_first_obj_left",
        "distance_second_obj_left",
        "type_first_obj_left",
        "type_second_obj_left",

        "distance_first_obj_right",
        "distance_second_obj_right",
        "type_first_obj_right",
        "type_second_obj_right",
        
        "distance_first_obj_up",
        "distance_second_obj_up",
        "type_first_obj_up",
        "type_second_obj_up",
        
        "distance_first_obj_down",
        "distance_second_obj_down",
        "type_first_obj_down",
        "type_second_obj_down",

        "latest_global_direction",
    ]



    @staticmethod
    def compute_model_state(game_state):
        model_state = None


        return state


    @staticmethod
    def compute_scores(game_engin, move):
        score = 0
        prev_move = game_engin.prev_move

        x_head, y_head = game_engin.map.snake_head
        nxt_x_head = x_head - 1 if move == 0 else x_head + 1 if move == 1 else x_head 
        nxt_y_head = y_head - 1 if move == 2 else y_head + 1 if move == 3 else y_head
        
        
        
        return score