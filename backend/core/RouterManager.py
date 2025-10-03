import os
import json
import time

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .fonctionnalities.SnakeEngin import SnakeEngin
#from fonctionnalities.Agent import Agent 



class RouterManager:
    def __init__(self, db_manager, ws_manager):
        self.db_manager = db_manager
        self.ws_manager = ws_manager
        self.router = APIRouter()

        self.snake_engins = {}

        self.routes()


    def routes(self):
        @self.router.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            print("🔵 WebSocket connection attempt...", flush=True)
            await self.ws_manager.connect(websocket)
            try:
                print("🟢 WebSocket connected successfully!", flush=True)
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                print("🔴    WebSocket disconnected", flush=True)
                self.ws_manager.disconnect(websocket)


        @self.router.get("/api/agents_list")
        async def agents_list():
            try:
                agents_list = self.db_manager.get_agents_list()

                return JSONResponse(content=agents_list)

            except Exception as error:
                print(f"api/agents_list ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))



        @self.router.get("/api/new_agent")
        async def new_agent(name, description):
            try:
                if self.db_manager.check_existing_agent(name) is True:
                    raise HTTPException(status_code=400, detail="Agent name already taken")

                self.db_manager.new_agent(name, description)

                updated_agents_list = self.db_manager.get_agents_list()
                await self.ws_manager.update_agents_list(updated_agents_list)

                #if name != 'Human':
                    # ADD INSTANCIATION DE L AGENT

                self.snake_engins[name] = None

                return JSONResponse(content={"status": "ok"})


            except Exception as error:
                print(f"api/new_equipment ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))

        

#        @self.router.get("/api/new_training")
#        async def new_training(agent_name, sessions, epsilon_init, epsilon_decay, visuals, speed=1):
#            try:
#                agent_save_file = db_manager.get_agent_file(agent_name)
#
#                snake_engin = SnakeEngin()
#                agent = Agent.load(agent_save_file)
#
#                agent.new_training(sessions, epsilon_init, epsilon_decay)
#
#                for i in range(sessions):
#                    snake_engin.new_game()
#                    agent.new_game()
#
#                    self.ws_manager.update_running_game(snake_engin.game_data())
#
#                    while game_engin.status == 'active':
#                        game_data = snake_engin.game_data()
#
#                        agent.update_q_table(game_data)
#                        next_move = agent.get_next_move(game_data)
#
#                        snake_engin.apply_move(next_move)
#                        self.ws_manager.update_running_game(snake_engin.game_data())
#
#                        if visuals is True:
#                            time.sleep(speed)
#
#
#
#                return JSONResponse(content={"status": "ok"})
#
#
#            except Exception as error:
#                print(f"api/new_training ===> ERROR: {str(error)}", flush=True)
#                raise HTTPException(status_code=500, detail=str(error))
#

        

        ###  ICI
        @self.router.get("/api/human_start_game")
        async def human_start_game(grid_size: int):
            try:    
                self.snake_engins['Human'] = SnakeEngin()
                self.snake_engins['Human'].new_game(grid_size)

                game_state = self.snake_engins['Human'].game_state()
                
#                self.db_manager.update_current_game('Human', game_state)
                await self.ws_manager.update_current_game("Human", game_state)

                return JSONResponse(content={"status": "ok"})

            except Exception as error:
                print(f"api/human_start_game ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))



        @self.router.get("/api/human_send_move")
        async def human_send_move(move):
            try:    
                self.snake_engins['Human'].execute_move(move)

                game_state = self.snake_engins['Human'].game_state()

#                self.db_manager.update_current_game('Human', game_state)
                await self.ws_manager.update_current_game("Human", game_state)
                return JSONResponse(content={"status": "ok"})


            except Exception as error:
                print(f"api/human_send_move ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))
