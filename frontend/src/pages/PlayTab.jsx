import React, { useEffect, useState } from "react";
import { GlobalState } from '../State.jsx';
import { apiRequests } from '../services/api_requests.js';
import GameGrid from '../components/GameGrid.jsx';

import "./PlayTab.css"

function PlayTab() {
    const {
        currentAgent,
        currentGame, setCurrentGame,
    } = GlobalState();

    const [newGameSetting, setNewGameSettings] = useState({gridSize: 10, exploratoryRatio: 0.05});

    const isHumanAgent = currentAgent === 'Human';


    const handleInputChange = (e) => {
        const { name, value, type } = e.target;
        setNewGameSettings(prev => ({
            ...prev,
            [name]: type === 'number' ? parseInt(value) : parseFloat(value)
        }));
    };


    //  KEY EVENTS WHEN GAME IS ACTIVE
    useEffect(() => {
        const handleKeyPress = (e) => {
            if (!isHumanAgent || currentGame.status !== 'active') return;

            let move;
            switch(e.key) {
                case 'ArrowUp':
                    move = 0;
                    break;
                case 'ArrowDown':
                    move = 1;
                    break;
                case 'ArrowLeft':
                    move = 2;
                    break;
                case 'ArrowRight':
                    move = 3;
                    break;
                default:
                    return;
            }

            apiRequests.sendHumanMove(move)
                .then(response => console.log("Move sent:", move))
                .catch(err => console.error("Move error:", err));

            e.preventDefault();
        };

        window.addEventListener('keydown', handleKeyPress);
        
        return () => {
            window.removeEventListener('keydown', handleKeyPress);
        };
    }, [isHumanAgent, currentGame.status, currentAgent]);


    const startGame = (e) => {
        e.preventDefault();
        console.log("Lancement de la partie:", { agent: currentAgent, ...newGameSetting });
        
        if (isHumanAgent) {
            apiRequests.newHumanGame(newGameSetting.gridSize)
                .then(response => console.log("Game started for human:", response))
                .catch(err => console.error(err));
        } 
        else {
            apiRequests.newAgentGame(currentAgent, newGameSetting.gridSize, newGameSetting.exploratoryRatio)
                .then(response => console.log("Game started for AI:", response))
                .catch(err => console.error(err));
        }
    };


    return (
        <div className="play-tab-container">
            <div className="game-main-content">
                <div className="game-visuals-container">
                    <div className="game-display">
                        <GameGrid currentGame={currentGame} newGameSetting={newGameSetting} />
                    </div>
                </div>

                <div className="game-settings-sidebar">
                    <div className="params-and-button">
                        <form className="game-params-form" onSubmit={startGame}>
                            <h2>Game Settings</h2>

                            <div className="form-group">
                                <label>Grid Size:</label>
                                <input type="number" name="gridSize" value={newGameSetting.gridSize} onChange={handleInputChange} min="5" max="50" required className="number-input"/>
                            </div>

                            {!isHumanAgent && (
                                <div className="form-group">
                                    <label>Exploratory Ratio: {newGameSetting.exploratoryRatio.toFixed(2)}</label>
                                    <input type="range" name="exploratoryRatio" value={newGameSetting.exploratoryRatio} onChange={handleInputChange} min="0" max="1" step="0.01" className="slider"/>
                                    <div className="slider-values">
                                        <span>0</span>
                                        <span>0.5</span>
                                        <span>1</span>
                                    </div>
                                </div>
                            )}
                        </form>
                        
                        <button type="submit" className="start-game-button" onClick={startGame}>
                            🚀 Start Game
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PlayTab;