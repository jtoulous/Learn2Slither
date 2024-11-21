class Agent():
    def __init__(self, args=None, config=None):
        if args.load == None:
            self.q_table = Qtable(n_actions=args.n_actions)
            self.learning_rate = args.learning_rate
            self.discount_factor = args.discount_factor
            self.epsilon = args.epsi
            self.decay_strat = args.epsi_decay

        else:
            self.LoadConfig(args.load)

    def LoadConfig(config_file): #to do
        pass  

    def NextMove(self, game_data): #to do
        pass


class Qtable():
    def __init__(self, n_action=None, file=None):
        if file == None:
            self.n_state = 0
            self.n_action = n_action
            self.table = self.NewTable(n_action)

        else:
            self.table, self.n_action, self.n_state = self.LoadTable(file)

    def LoadTable(self, file): #to do
        pass

    def NewTable(self, n_action): #to do
        pass

    def SaveTable(self, file): #to do
        pass
