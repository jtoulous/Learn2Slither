from fastapi import WebSocket
from typing import List, Any, Dict
import json


class WebsocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    

    async def connect(self, websocket: WebSocket):
        """Connecte un websocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total: {len(self.active_connections)}")


    def disconnect(self, websocket: WebSocket):
        """Déconnecte un websocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"WebSocket disconnected. Remaining: {len(self.active_connections)}")


    async def broadcast(self, message: dict):
        """Balance le message à tous les clients connectés"""
        message_str = json.dumps(message)
        disconnected = []
        
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message_str)
            except:
                disconnected.append(websocket)
        
        for websocket in disconnected:
            self.disconnect(websocket)


    async def update_agents_list(self, agents_list: dict):
        """Met à jour la liste des agents"""
        await self.broadcast({
            "type": "agents_list_update",
            "payload": agents_list
        })


    async def update_agent_status(self, agent_name: str, status: str):
        """Met à jour le statut d'un agent"""
        await self.broadcast({
            "type": "agent_status_update", 
            "payload": {
                "agent_name": agent_name,
                "status": status
            }
        })


    async def update_current_game(self, agent_name, game_state):
        await self.broadcast({
            "type": "current_game_update",
            "payload": {
                "agent_name": agent_name,
                "game_state": game_state
            }
        })


    async def update_current_training(self, agent_name, training_state):
        await self.broadcast({
            "type": "current_training_update",
            "payload": {
                "agent_name": agent_name,
                "training_state": training_state
            }
        })