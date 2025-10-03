import React, { useState, useEffect } from "react"
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';

import "./TrainingTab.css"

function TrainingTab() {
    const {
        currentAgent,
        agentsList, setAgentsList,
        trainingParams, setTrainingParams
    } = GlobalState();

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setTrainingParams(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : 
                   type === 'number' ? parseInt(value) : 
                   type === 'float' ? parseFloat(value) : value
        }));
    };

    const startTraining = (e) => {
        e.preventDefault();
        console.log("Lancement de l'entraînement:", trainingParams);
    };

    return (
        <div className="training-tab-container">
            
            <div className="new-training-container">
                <form className="new-training-form" onSubmit={startTraining}>
                    <h1>Training Parameters</h1>

                    <div className="form-group">
                        <label>Sessions:</label>
                        <input type="number" name="sessions" value={trainingParams.sessions} onChange={handleInputChange}min="1"required/>
                    </div>

                    <div className="form-group">
                        <label>Epsilon Decay:</label>
                        <select name="epsilonDecay" value={trainingParams.epsilonDecay} onChange={handleInputChange}>
                            <option value="linear">Linear</option>
                            <option value="exponential">Exponential</option>
                            <option value="polynomial">Polynomial</option>
                            <option value="constant">Constant</option>
                        </select>
                    </div>

                    <div className="form-group checkbox-group">
                        <label>
                            <input type="checkbox" name="visuals" checked={trainingParams.visuals} onChange={handleInputChange}/>
                            Visuals
                        </label>
                    </div>

                    {trainingParams.visuals && (
                        <div className="form-group">
                            <label>Speed (seconds between moves):</label>
                            <input type="number" name="speed" value={trainingParams.speed} onChange={handleInputChange} step="0.1" min="0.1" required/>
                        </div>
                    )}

                    <button type="submit" className="start-training-button">
                        Start Training
                    </button>
                </form>
            </div>

            <div className="visuals-container">
                {}
            </div>

            <div className="stats-container">
                    
            </div>
            

        </div>
    )
}

export default TrainingTab;