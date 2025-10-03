import React, { useState, useEffect } from "react"
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';

import "./StatsTab.css"

function StatsTab() {
    const {
        currentAgent,
    } = GlobalState();

    const isHumanAgent = currentAgent === 'Human';


    return (
        <div className="stats-tab-container">
            
            <div className="basic-stats-container">
            </div>

            <div className="historical-games-stats">
            </div>

            <div className="training-sessions-stats">
            </div>

        </div>
    )
}

export default StatsTab;