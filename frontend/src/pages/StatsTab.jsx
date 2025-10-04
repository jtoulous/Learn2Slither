import React, { useState, useEffect } from "react"
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';
import { useNavigate } from "react-router-dom"; 


import "./StatsTab.css"


function Stats() {
    const {
        currentAgent,
        scoresStats, setScoreStats,
        detailsStats, setDetailsStats
    } = GlobalState();

    const isHumanAgent = currentAgent === 'Human';


    useEffect(() => {
        if (isHumanAgent) {
            apiRequests.getHumanStats(currentAgent)
                .then(data => {
                    setScoreStats(data.scoresStats);
                    setDetailsStats(data.detailsStats);
                })
                .catch(err => console.error(err));
        }
    }, [currentAgent]);


    return (
        <div className="stats-page-container">


            <div className="scores-curves-container">                
            </div>

            <div className="details-curves-container">
            </div>

     

            {!isHumanAgent && (
                <div className="agent-training-stats-container">        
                </div>
            )}
        
        </div>
    )
}

export default Stats