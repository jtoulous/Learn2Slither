import os
import json
import sqlite3





class DatabaseManager:
    def __init__(self, db_repo, agents_info_tbl='agents_info'):
        self.DB_REPO = db_repo
        self.DB_FILE = os.path.join(self.DB_REPO, 'database.db')
        self.AGENTS_TBL = agents_info_tbl

        self.agents_list = []

        os.makedirs(db_repo, exist_ok=True)

        query_1 = f'''
            CREATE TABLE IF NOT EXISTS {self.AGENTS_TBL} (
                name TEXT PRIMARY KEY,
                status TEXT,
                description TEXT,
                sessions INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''

        self.execute_query(query_1)
        
        if 'Human' not in self.get_agents_list():
            self.new_agent('Human', 'Human account')


    def escape_sql_vals(self, string):
        escaped_string = string.replace("'", "''")
        return escaped_string

    def escape_sql(self, string):
        escaped_string = string.replace("'", "''").replace(" ", "_").replace("-", "_")
        return escaped_string


    def execute_queries(self, queries, db=None):
        if db is None:
            db = self.DB_FILE

        connection = None
        try:
            connection = sqlite3.connect(db, timeout=10)
            cursor = connection.cursor()

            for query in queries:
                cursor.execute(query)

            connection.commit()


        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution des requêtes : {e}")
            if connection:
                connection.rollback()
            raise

        finally:
            if connection:
                connection.close()


    def execute_query(self, query, db=None):
        if db is None:
            db = self.DB_FILE

        connection = None
        try:
            connection = sqlite3.connect(db)
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            connection.commit()
            connection.close()
            return results

        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution des requêtes : {e}")
            if connection:
                connection.rollback()
            raise

        finally:
            if connection:
                connection.close()


    def check_existing_agent(self, agent_name):
        if agent_name in self.agents_list:
            return True
        return False 



    def get_agents_list(self):
        query = f'''
            SELECT name, status FROM {self.AGENTS_TBL}
        '''
        results = self.execute_query(query)

        agents_list ={row[0]: row[1] for row in results}
        return agents_list


    def get_agent_file(self, agent_name):
        agent_name_escaped = self.escape_sql(agent_name)
        return os.path.join(self.DB_REPO, agent_name_escaped, f'{agent_name_escaped}.pkl')


#    def get_nb_cycles(self, agent_name):



    def new_agent(self, agent_name, description):
        agent_name_tbl= self.escape_sql(agent_name)
        description_tbl = self.escape_sql(description)
        
        new_agent_repo = os.path.join(self.DB_REPO, agent_name_tbl)
        os.makedirs(new_agent_repo, exist_ok=True)

        historical_games_table = self.escape_sql(f'{agent_name_tbl}_games_history')
        current_game_table = self.escape_sql(f'{agent_name_tbl}_current_game')
        current_session_table = self.escape_sql(f'{agent_name_tbl}_current_session')

        query_1 = f'''
            INSERT INTO {self.AGENTS_TBL} (name, status, description, sessions)
            VALUES ('{self.escape_sql_vals(agent_name)}', 'inactive', '{self.escape_sql_vals(description)}', 0)
        '''

        query_2 = f'''
            CREATE TABLE IF NOT EXISTS {historical_games_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_group TEXT,
                n_cells INTEGER,
                score INTEGER,
                green_score INTEGER,
                red_score INTEGER,
                nb_moves INTEGER
            )
        '''

        if agent_name != 'Human':
            query_3 = f'''
                CREATE TABLE IF NOT EXISTS {current_session_table} (
                    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
                    nb_games INTEGER
                )
            '''
            self.execute_queries([query_1, query_2, query_3])
        
        else:
            self.execute_queries([query_1, query_2])

        self.agents_list.append(agent_name)



    
    def save_game_results(self, cycle_group, agent_name, game_state):
        agent_name_escaped = self.escape_sql(agent_name)
        historical_games_table = f'{agent_name_escaped}_games_history'

        query = f'''
            INSERT INTO {historical_games_table} (game_group, n_cells, score, green_score, red_score, nb_moves)
            VALUES ('{cycle_group}', {game_state['n_cells']}, {game_state['score']}, {game_state['green_score']}, {game_state['red_score']}, {game_state['nb_moves']})
        '''
        
        self.execute_query(query)