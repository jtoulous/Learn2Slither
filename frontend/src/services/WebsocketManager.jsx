import React, { useEffect, useRef } from "react";
import { GlobalState } from '../State.jsx';


function WebsocketManager() {
    const state = GlobalState();
    const stateRef = useRef(state);

    useEffect(() => {
        stateRef.current = state;
    });

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:54322/ws')

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)

            switch(data.type){
                case 'agents_list_update':
                    stateRef.current.setAgentsList(data.payload);
                    break;
                    
                case 'agent_status_update':
                    stateRef.current.setAgentsList(prev => ({
                        ...prev,
                        [data.payload.agent_name]: data.payload.status
                    }));
                    break;

                case 'current_game_update':
                    // ✅ Direct dans la ref, toujours à jour
                    if (stateRef.current.currentAgent === data.payload.agent_name) {
                        stateRef.current.setCurrentGame(data.payload.game_state);
                    }
                    break;
            }
        };

        // ... reste du code WebSocket
    }, []);

    return null;
}

export default WebsocketManager