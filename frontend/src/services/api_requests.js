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
    },


    agentNewTraining: (currentAgent, trainingParams) => {
        const formData = new FormData();

        formData.append("agent_name", currentAgent.name)
        formData.append("nb_sessions", trainingParams.sessions)
        formData.append("epsilon_decay_strat", trainingParams.epsilonDecayStrat)
        formData.append("epsilon_init", trainingParams.epsilonInit)
        formData.append("epsilon_min", trainingParams.epsilonMin)
        formData.append("epsilon_decay_rate", trainingParams.epsilonDecayRate)
        formData.append("epsilon_decay_k", trainingParams.epsilonDecayK)
        formData.append("epsilon_decay_power", trainingParams.epsilonDecayPower)

        
        return fetch(`http://localhost:54322/api/agent_new_training`, {
            method: "POST",
            body: formData
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Error starting new training")
            }
            return res.json();
        })
    },

    
    agentContinueTraining: (currentAgent, toggleVisuals) => {
        const formData = new FormData();

        formData.append("agent_name", currentAgent.name)
        formData.append("visuals", toggleVisuals)
        
        return fetch(`http://localhost:54322/api/agent_continue_training`, {
            method: "POST",
            body: formData
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Error starting continuing training")
            }
            return res.json();
        })
    }

};