import React, { useState, useEffect } from "react"
import { useSearchParams } from "react-router-dom";
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';

import PlayTab from './PlayTab.jsx';
import TrainingTab from './TrainingTab.jsx';
import StatsTab from './StatsTab.jsx';

import "./Agent.css"


function Agent() {
    const [searchParams] = useSearchParams();
    
    const {
        currentAgent, setCurrentAgent,
        currentTab, setCurrentTab
    } = GlobalState();


    useEffect(() => {
        setCurrentAgent(searchParams.get('agent_name'));
    }, [searchParams, setCurrentAgent]);

    return (
        <div className="agent-page-container">
            
            <div className="agent-top-container">
                {currentAgent}
                <div className="settings-icon" onClick={() => console.log("Ouvrir les paramètres")}>⚙️</div>
            </div>
            
            <div className="tab-selection-container">
                <div className={`tab-select play-tab-select ${currentTab === 'play' ? 'active' : ''}`} onClick={() => setCurrentTab('play')}>
                     Play
                </div>

                {currentAgent !== 'Human' && (
                    <div className={`tab-select training-tab-select ${currentTab === 'training' ? 'active' : ''}`} onClick={() => setCurrentTab('training')}>
                        Training
                    </div>
                )}

                <div className={`tab-select stats-tab-select ${currentTab === 'stats' ? 'active' : ''}`} onClick={() => setCurrentTab('stats')}>
                    Stats
                </div>
            </div>
            
            <div className="tab-content">
                {currentTab === 'play' && <PlayTab />}
                {currentTab === 'training' && <TrainingTab />}
                {currentTab === 'stats' && <StatsTab />}
            </div>

        </div>
    );
}

export default Agent;