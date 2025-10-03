import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .DatabaseManager import DatabaseManager
from .WebsocketManager import WebsocketManager
from .RouterManager import RouterManager



class ServerManager:
    def __init__(self, db_path, host='0.0.0.0', port=8000):
        self.db_path = db_path
        self.host = host
        self.port = port

        self.ws_manager = WebsocketManager()
        self.db_manager = DatabaseManager(db_path)
        self.router_manager = RouterManager(self.db_manager, self.ws_manager)
    
        self.server = self.init_server()


    def init_server(self):
        server = FastAPI()
        server.include_router(self.router_manager.router)

        origins = [
            "http://localhost:54323",
        ]

        server.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return server


    def run(self):
        uvicorn.run(self.server, host=self.host, port=self.port)