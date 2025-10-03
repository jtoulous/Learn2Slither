import React, { useState, useEffect } from "react"
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';
import { useNavigate } from "react-router-dom"; 

import StatusIndicator from '../components/StatusIndicator.jsx';

import "./Home.css"


function Home() {
    const {
        currentAgent, setCurrentAgent,
        agentsList, setAgentsList,
        showNewAgentForm, setShowNewAgentForm,
        newAgent, setNewAgent
    } = GlobalState()

    const navigate = useNavigate();

    const sendNewAgent = (e) => {
        e.preventDefault();
        apiRequests.sendNewAgent(newAgent)
            .then(() => {
                setShowNewAgentForm(false);
                return apiRequests.getAgentsList();
            })
            .then(data => setAgentsList(data))
            .catch(err => console.error(err));
    };

    const handleAgentClick = (agentName) => {
        setCurrentAgent(agentName);
        navigate(`/agent?agent_name=${agentName}`);
    };

    return (
        <div className="home-page-container">
            
            <div className="new-agent">        
                <button className="new-agent-button" onClick={() => setShowNewAgentForm(true)}>New Agent</button>

                {showNewAgentForm && (
                    <div className="home-popup-form">
                        <form className="agent-form-popup" onSubmit={sendNewAgent}>

                            <label>Agent Name:
                                <input type="text" name="name" value={newAgent.name} onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })} required/>
                            </label>

                            <label>Description:
                                <input type="text" name="info" value={newAgent.info} onChange={(e) => setNewAgent({ ...newAgent, info: e.target.value })}/>
                            </label>

                            <div className="popup-buttons">
                                <button type="submit" className="agent-button">Create</button>
                                <button type="button" className="agent-button" onClick={() => setShowNewAgentForm(false)}>Cancel</button>
                            </div>
                        </form>
                    </div>
                )}
            </div>

            <div className="agents-container">
                <h1>Your agents:</h1>
                <ul className="agents-list">
                    {Object.entries(agentsList).map( ([name, status]) => (
                        <li key={name} className="agent-item">
                            <div className="agent-form">
                                <span className="agent-name">
                                    <StatusIndicator status={status} />
                                    {name}
                                </span>
                                <input type="hidden" name="agent_name" value={name}/>
                                <button className="agent-button" type="button" onClick={() => handleAgentClick(name)}>Check</button>
                            </div>
                        </li>
                    ))}
                </ul>

            </div>
        
        
        </div>
    )
}

export default Home