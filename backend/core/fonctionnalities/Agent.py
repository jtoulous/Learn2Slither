



class Agent:
    def __init__(self):
        self.epsilon = 0.01
        self.q_table = QTable()

        self.prev_move = None
    

    def new_training(self, sessions, epsilon_init, epsilon_decay):
        return





class QTable:
    def __init__(self):
        self.state = np.array(1)
        self.up_scores = np.array(1)
        self.down_scores = np.array(1)
        self.left_scores = np.array(1)
        self.right_scores = np.array(1)

    def update_q_table(self):
        