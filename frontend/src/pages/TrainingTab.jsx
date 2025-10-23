import React, { useState, useEffect, useRef } from "react"
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';

import "./TrainingTab.css"

function TrainingTab() {
    const {
        currentAgent,
        currentTraining,
    } = GlobalState();
    
    const [trainingParams, setTrainingParams] = useState({sessions: 1000, epsilonDecayStrat: "linear", epsilonInit: 1, epsilonMin: 0.05, epsilonDecayRate: 0.995, epsilonDecayK: 1.0, epsilonDecayPower: 2.0, visuals: false, speed: 1.0});
    const [toggleVisuals, setToggleVisuals] = useState(false)
    const [inputSpeed, setInputSpeed] = useState(1)
    const [toggleSBS, setToggleSBS] = useState(false)

    const toggleVisualsRef = useRef(toggleVisuals)
    const inputSpeedRef = useRef(inputSpeed)
    const toggleSBSRef = useRef(toggleSBS)

    useEffect(() => {
      toggleVisualsRef.current = toggleVisuals;
      inputSpeedRef.current = inputSpeed;
      toggleSBSRef.current = toggleSBS;
    }, [toggleVisuals, inputSpeed, toggleSBS]);



    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setTrainingParams(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : 
                   type === 'number' ? parseFloat(value) : value
        }));
    };

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    const waitForSpacebar = () => {
        return new Promise((resolve) => {
            const handleKeyPress = (e) => {
                if (e.code === 'Space') {
                    e.preventDefault();
                    document.removeEventListener('keydown', handleKeyPress);
                    resolve();
                }
            };

            document.addEventListener('keydown', handleKeyPress);
        });
    };


    const runTraining = async (e) => {
        e.preventDefault();

        try {
            const res = await apiRequests.agentNewTraining(currentAgent, trainingParams);

            if (res.ok) {
                let training_status = "running";

                while (training_status === "running") {

                    if (toggleVisualsRef.current === true) {   
                        if (toggleSBSRef.current === true) {
                            await waitForSpacebar();
                        }     
                        else {
                            await sleep(inputSpeedRef.current * 1000);
                        }
                    }

                    const trainingRes = await apiRequests.agentContinueTraining(currentAgent, toggleVisuals);
                    training_status = trainingRes.training_status;
                }
            }
        } 
        catch (err) {
            console.error(err);
        }
    };


    return (
        <div className="training-tab-container">
            
            <div className="new-training-container">
                <form className="new-training-form" onSubmit={runTraining}>
                    <h1>Training Parameters</h1>

                    <div className="form-group">
                        <label>Sessions:</label>
                        <input type="number" name="sessions" value={trainingParams.sessions} onChange={handleInputChange} min="1" required/>
                    </div>


                    <div className="form-group">
                        <label>Epsilon Decay Strategy:</label>
                        <select name="epsilonDecayStrat" value={trainingParams.epsilonDecayStrat} onChange={handleInputChange}>
                            <option value="linear">Linear</option>
                            <option value="exponential">Exponential</option>
                            <option value="polynomial">Polynomial</option>
                            <option value="constant">Constant</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Epsilon init:</label>
                        <input type="number" name="epsilonInit" value={trainingParams.epsilonInit} onChange={handleInputChange} min="0" max="1" required/>
                    </div>

                    {trainingParams.epsilonDecayStrat != 'constant' && (
                        <div>

                            <div className="form-group">
                                <label>Epsilon min:</label>
                                <input type="number" name="epsilonMin" value={trainingParams.epsilonMin} onChange={handleInputChange} min="0" max="1" step="0.01"/>
                            </div>

                            {trainingParams.epsilonDecayStrat === 'exponential' && (
                                <div className="form-group">
                                    <label>Epsilon Decay rate:</label>
                                    <input type="number" name="epsilonDecayRate" value={trainingParams.epsilonDecayRate} onChange={handleInputChange} min="0" max="1"/>
                                </div>
                            )}

                            {trainingParams.epsilonDecayStrat === 'polynomial' && (
                                <div>
                                    <div className="form-group">
                                        <label>Epsilon Decay K:</label>
                                        <input type="number" name="epsilonDecayK" value={trainingParams.epsilonDecayK} onChange={handleInputChange} min="0" max="1"/>
                                    </div>

                                    <div className="form-group">
                                        <label>Epsilon Decay Power:</label>
                                        <input type="number" name="epsilonDecayPower" value={trainingParams.epsilonDecayPower} onChange={handleInputChange} min="0" max="1"/>
                                    </div>
                                </div>
                            )}


                        </div>
                    )}


                    <div className="form-group checkbox-group">
                        <label>
                            <input type="checkbox" name="visuals" checked={trainingParams.visuals} onChange={handleInputChange}/>
                            Visuals
                        </label>
                    </div>

                    {trainingParams.visuals && (
                        <div>
                            <div className="form-group">
                                <label>Speed (seconds between moves):</label>
                                <input type="number" name="speed" value={trainingParams.speed} onChange={handleInputChange} step="0.1" min="0.1" required/>
                            </div>
                        
                            <div className="form-group checkbox-group">
                                <label>Step by step:</label>
                                <input type="checkbox" name="step-by-step" checked={toggleSBS} onChange={() => setToggleSBS(!toggleSBS)}/>
                            </div>
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