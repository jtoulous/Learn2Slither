import React, { createContext, useContext, useState, useEffect, use } from 'react';
import { apiRequests } from './services/api_requests.js';


const StateContext = createContext();

export function State({ children }) {
    const [agentsList, setAgentsList] = useState({})
    
    // Leftbar.jsx
    const [showLeftBar, setShowLeftBar] = useState(false)
    
    // Home.jsx
    const [newAgent, setNewAgent] = useState({name: "", description: ""})
    
    // Agent.jsx
    const [currentAgent, setCurrentAgent] = useState("")
    const [currentTab, setCurrentTab] = useState("play")
    
    // TrainingTab.jsx
    const [currentTraining, setCurrentTraining] = useState(null)

    //PlayTab
    const [currentGame, setCurrentGame] = useState({status: "inactive", n_cells: 10, snake_head: [], snake_body: [], green_apples: [],red_apples: [],score: 0,green_score: 0,red_score: 0})
    
    //Stats
    const [scoresStats, setScoreStats] = useState({})
    const [detailsStats, setDetailsStats] = useState({})



    useEffect(() => {
        apiRequests.getAgentsList()
        .then(data => setAgentsList(data))
        .catch(err => console.error(err));
    }, []);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            window._globalState = {
                agentsList, setAgentsList,
                showLeftBar, setShowLeftBar,
                newAgent, setNewAgent,
                currentAgent, setCurrentAgent,
                currentTab, setCurrentTab,
                currentGame, setCurrentGame,
                currentTraining, setCurrentTraining
            };
        }
    });



    return (
        <StateContext.Provider value={{
            agentsList, setAgentsList,
            showLeftBar, setShowLeftBar,
            newAgent, setNewAgent,
            currentAgent, setCurrentAgent,
            currentTab, setCurrentTab,
            currentGame, setCurrentGame,
            currentTraining, setCurrentTraining
        }}>
            {children}
        </StateContext.Provider>
    );
}

export const GlobalState = () => useContext(StateContext);