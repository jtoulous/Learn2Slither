export const apiRequests = {

    getAgentsList: () => {
        return fetch(`http://localhost:54322/api/agents_list`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error getting agents list");
                }
                return res.json();
            });
    },

    sendNewAgent: (newAgent) => {
        const params = new URLSearchParams(newAgent);
        return fetch(`http://localhost:54322/api/new_agent?${params.toString()}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error creating new agent");
                }
                return res.json();
            });
    },

    newHumanGame: (gridSize) => {
        const params = new URLSearchParams({
            grid_size: gridSize
        });
        return fetch(`http://localhost:54322/api/human_new_game?${params.toString()}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error starting the game")
                }
                return res.json();
            });
    },


    newAgentGame: (agentName, gridSize, exploratoryRatio) => {
        const params = new URLSearchParams({
            agent_name: agentName,
            grid_size: gridSize,
            exploratory_ratio: exploratoryRatio
        });
        return fetch(`http://localhost:54322/api/agent_new_game?${params.toString()}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error starting the game")
                }
                return res.json();
            });
    },


    sendHumanMove: (move) => {
        const params = new URLSearchParams({
            move: move,
        });
        
        return fetch(`http://localhost:54322/api/human_send_move?${params.toString()}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error starting the game")
                }
                return res.json();
            });
    },


    getHumanStats: () => {
        return fetch(`http://localhost:54322/api/human_get_stats`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error("Error starting the game")
                }
                return res.json();
            });     
    }


};