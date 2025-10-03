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


    def escape_sql(self, value):
        return value.replace("'", "''")


    def table_name(self, tbl_name):
        tbl_name = tbl_name.replace(' ', '_')
        tbl_name = tbl_name.replace('-', '_')
        return tbl_name


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



    def new_agent(self, agent_name, description):
        agent_name_tbl= self.table_name(agent_name)
        description_tbl = self.table_name(description)
        
        new_agent_repo = os.path.join(self.DB_REPO, agent_name_tbl)
        os.makedirs(new_agent_repo)

        historical_games_table = self.table_name(f'{agent_name_tbl}_games_history')
        current_game_table = self.table_name(f'{agent_name_tbl}_current_game')
        current_session_table = self.table_name(f'{agent_name_tbl}_current_session')

        query_1 = f'''
            INSERT INTO {self.AGENTS_TBL} (name, status, description, sessions)
            VALUES ('{self.escape_sql(agent_name)}', 'inactive', '{self.escape_sql(description)}', 0)
        '''

        query_2 = f'''
            CREATE TABLE IF NOT EXISTS {historical_games_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT,
                score INTEGER,
                nb_green INTEGER,
                nb_red INTEGER,
                nb_moves INTEGER
            )
        '''

#        query_3 = f'''
#            CREATE TABLE IF NOT EXISTS {current_game_table} (
#                id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
#                status TEXT,
#                n_cells INTEGER,
#                snake_head TEXT,
#                snake_body TEXT,
#                green_apples TEXT,
#                red_apple TEXT,
#                score INTEGER,
#                green_score,
#                red_score
#            )
#        '''

        if agent_name != 'Human':
            query_4 = f'''
                CREATE TABLE IF NOT EXISTS {current_session_table} (
                    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
                    nb_games INTEGER
                )
            '''
            self.execute_queries([query_1, query_2, query_4])# query_3, query_4])
        
        else:
            self.execute_queries([query_1, query_2])#, query_3])

        self.agents_list.append(agent_name)



    def get_agents_list(self):
        query = f'''
            SELECT name, status FROM {self.AGENTS_TBL}
        '''
        results = self.execute_query(query)

        agents_list ={row[0]: row[1] for row in results}
        return agents_list


    def get_agent_file(self, agent_name):
        agent_name_escaped = self.table_name(agent_name)
        return os.path.join(self.DB_REPO, agent_name_escaped, f'{agent_name_escaped}.pkl')

    
    def update_current_game(self, agent_name, game_state):
        agent_name_tbl= self.table_name(agent_name)
        current_game_table = self.table_name(f'{agent_name_tbl}_current_game')

        snake_head_str = json.dumps(game_state['snake_head'])
        snake_body_str = json.dumps(game_state['snake_body'])
        green_apples_str = json.dumps(game_state['green_apples'])
        red_apple_str = json.dumps(game_state['red_apple'])

        query = f'''
            REPLACE INTO {current_game_table} 
            (id, status, n_cells, snake_head, snake_body, green_apples, red_apple, score, green_score, red_score)
            VALUES (1, '{game_state['status']}', {game_state['n_cells']}, '{snake_head_str}', '{snake_body_str}', '{green_apples_str}', '{red_apple_str}', {game_state['score']}, {game_state['green_score']}, {game_state['red_score']})
        '''

        self.execute_query(query)