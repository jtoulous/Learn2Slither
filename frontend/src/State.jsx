import React, { createContext, useContext, useState, useEffect, use } from 'react';
import { apiRequests } from './services/api_requests.js';


const StateContext = createContext();

export function State({ children }) {
    const [agentsList, setAgentsList] = useState({})
    
    // Leftbar.jsx
    const [showLeftBar, setShowLeftBar] = useState(false)
    
    // Home.jsx
    const [showNewAgentForm, setShowNewAgentForm] = useState(false)
    const [newAgent, setNewAgent] = useState({name: "", description: ""})
    
    // Agent.jsx
    const [currentAgent, setCurrentAgent] = useState("")
    const [currentTab, setCurrentTab] = useState("play")
    
    // TrainingTab.jsx
    const [trainingParams, setTrainingParams] = useState({sessions: 1000, epsilonDecay: "linear", visuals: false, speed: 1.0});
    
    //PlayTab
    const [newGameSetting, setNewGameSettings] = useState({gridSize: 10, exploratoryRatio: 0.05});
    const [currentGame, setCurrentGame] = useState({
        status: "inactive", 
        n_cells: 10, 
        snake_head: [], 
        snake_body: [], 
        green_apples: [],
        red_apples: [],
        score: 0,
        green_score: 0,
        red_score: 0
    })
    
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
                showNewAgentForm, setShowNewAgentForm,
                newAgent, setNewAgent,
                currentAgent, setCurrentAgent,
                currentTab, setCurrentTab,
                trainingParams, setTrainingParams,
                newGameSetting, setNewGameSettings,
                currentGame, setCurrentGame
            };
        }
    });



    return (
        <StateContext.Provider value={{
            agentsList, setAgentsList,
            showLeftBar, setShowLeftBar,
            showNewAgentForm, setShowNewAgentForm,
            newAgent, setNewAgent,
            currentAgent, setCurrentAgent,
            currentTab, setCurrentTab,
            trainingParams, setTrainingParams,
            newGameSetting, setNewGameSettings,
            currentGame, setCurrentGame
        }}>
            {children}
        </StateContext.Provider>
    );
}

export const GlobalState = () => useContext(StateContext);