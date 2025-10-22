import os
import json
import time

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .fonctionnalities.SnakeEngin import SnakeEngin
from .fonctionnalities.Agent import Agent 



class RouterManager:
    def __init__(self, db_manager, ws_manager):
        self.db_manager = db_manager
        self.ws_manager = ws_manager
        self.router = APIRouter()

        self.routes()
        
        self.snake_engins = {}
        self.agents = {}

        agents_list = self.db_manager.get_agents_list()

        for agent in agents_list:
            self.snake_engins[agent] = SnakeEngin()
#            if agent != 'Human':
#                self.agents[agent] = Agent.load(self.db_manager.get_agent_file(agent))


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
                self.snake_engins[name] = SnakeEngin()

                updated_agents_list = self.db_manager.get_agents_list()
                await self.ws_manager.update_agents_list(updated_agents_list)

                #if name != 'Human':
                    # ADD INSTANCIATION DE L AGENT

                return JSONResponse(content={"status": "ok"})


            except Exception as error:
                print(f"api/new_equipment ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))

        

        @self.router.get("/api/human_new_game")
        async def human_new_game(grid_size: int):
            try:    
                self.snake_engins['Human'].new_game(grid_size)

                game_state = self.snake_engins['Human'].game_state()
                
                await self.ws_manager.update_current_game("Human", game_state)

                return JSONResponse(content={"status": "ok"})

            except Exception as error:
                print(f"api/human_new_game ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))



        @self.router.get("/api/human_send_move")
        async def human_send_move(move):
            try:    
                self.snake_engins['Human'].execute_move(move)

                game_state = self.snake_engins['Human'].game_state()

                if game_state['status'] == 'end':
                    self.db_manager.save_game_results('Human', game_state)

                await self.ws_manager.update_current_game("Human", game_state)
                return JSONResponse(content={"status": "ok"})


            except Exception as error:
                print(f"api/human_send_move ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))



        @self.router.get("/api/human_get_stats")
        async def human_get_stats():
            try:    
                scores_stats, details_stats = self.db_manager.get_stats('Human')
                
                await self.ws_manager.send_stats('Human', scores_stats, details_stats, None)
                return JSONResponse(content={"status": "ok"})


            except Exception as error:
                print(f"api/human_get_stats ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))


        @self.router.get("/api/agent_new_game")
        async def agent_new_game(agent_name, grid_size, exploratory_ratio):
            try:
                self.snake_engins[agent_name] = SnakeEngin()
                self.snake_engins[agent_name].new_game(grid_size)

                game_state = self.snake_engins[agent_name].game_state()
                
                await self.ws_manager.update_current_game(agent_name, game_state)

                return JSONResponse(content={"status": "ok"})
                
            except Exception as error:
                print(f"api/agent_new_game ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))



        @self.router.get("/api/agent_new_training")
        async def agent_start_training(agent_name, nb_sessions, epsilon_decay):
            try:
                self.ongoing_trainings[agent_name] = TrainingCycle(self.db_manager, self.agents[agent_name], self.snake_engins[agent_name], nb_sessions, epsilon_decay)
                
                self.ws_manager.update_current_training(agent_name, self.ongoing_trainings[agent_name].training_state())


            except Exception as error:
                print(f"api/agent_new_training ===> ERROR: {str(error)}", flush=True)
                raise HTTPException(status_code=500, detail=str(error))




#        @self.router.get("api/agent_continue_training")
#        async def agent_continue_training(agent_name):
#            try:    
#                training_cycle = self.ongoing_trainings[agent_name]
#                training_cycle.nxt_move()
#
#                self.ws_manager.update_current_training(agent_name, training_cycle.training_state())
#
#                if training_cycle.status == 'done':
#                    del self.ongoing_trainings[agent_name]
#
#
#            except Exception as error:
#                print(f"api/agent_nxt_move ===> ERROR: {str(error)}", flush=True)
#                raise HTTPException(status_code=500, detail=str(error))\


#        @self.router.get("api/agent_nxt_move_game")
#        async def agent_nxt_move_game(agent_name):
#            try:    
#            except Exception as error:
#                print(f"api/agent_nxt_move ===> ERROR: {str(error)}", flush=True)
#                raise HTTPException(status_code=500, detail=str(error))\
