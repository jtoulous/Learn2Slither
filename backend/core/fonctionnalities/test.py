from SnakeEngin import SnakeEngin
from Agent import Agent, TrainingCycle, Interpreter




training_params = {
    'nb_sessions': 1000,
    'epsilon_decay_strat': 'linear',
    'epsilon_init': 1,
    'epsilon_min': 0.05,
    'epsilon_decay_rate': 0.995,
    'epsilon_decay_k': 1.0,
    'epsilon_decay_power': 2.0  
}



if __name__ == '__main__':
    try:
        game_engin = SnakeEngin()
        agent = Agent('Tonton Adolf')

        training_cycle = TrainingCycle(agent, game_engin, training_params)


        while training_cycle.status == 'running':
            training_cycle.nxt_move()
            input()

    

    except Exception as error:
        print(f'Error: {error}')