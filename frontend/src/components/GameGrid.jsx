import React from "react";

import "./GameGrid.css"


const renderPreviewGrid = (gridSize) => {
    return (
        <div className="futuristic-grid-container">
            <div className="grid-background-glow"></div>
            <div 
                className="snake-game-preview futuristic"
                style={{
                    gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
                    gridTemplateRows: `repeat(${gridSize}, 1fr)`
                }}
            >
                {Array.from({ length: gridSize * gridSize }).map((_, index) => (
                    <div key={index} className="grid-cell">
                        <div className="cell-inner"></div>
                    </div>
                ))}
            </div>
            <div className="grid-border grid-border-top"></div>
            <div className="grid-border grid-border-right"></div>
            <div className="grid-border grid-border-bottom"></div>
            <div className="grid-border grid-border-left"></div>
        </div>
    );
};

const renderGameGrid = (currentGame) => {
    const gridSize = currentGame.n_cells;
    const grid = [];

    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            grid.push({ x: i, y: j, type: 'empty' });
        }
    }

    const [headX, headY] = currentGame.snake_head;
    grid[(headX - 1) * gridSize + (headY - 1)].type = 'snake_head';

    currentGame.snake_body.forEach(([bodyX, bodyY], index) => {
        const isTail = index === currentGame.snake_body.length - 1;
        grid[(bodyX - 1) * gridSize + (bodyY - 1)].type = isTail ? 'snake_tail' : 'snake_body';
    });

    currentGame.green_apples.forEach(([appleX, appleY]) => {
        grid[(appleX - 1) * gridSize + (appleY - 1)].type = 'green_apple';
    });

    const [redX, redY] = currentGame.red_apple;
    grid[(redX - 1) * gridSize + (redY - 1)].type = 'red_apple';

    return (
        <div className="futuristic-grid-container">
            <div className="grid-background-glow"></div>
            <div 
                className="snake-game-preview futuristic"
                style={{
                    gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
                    gridTemplateRows: `repeat(${gridSize}, 1fr)`
                }}
            >
                {grid.map((cell, index) => (
                    <div key={index} className={`grid-cell ${cell.type}`}>
                        <div className="cell-inner"></div>
                    </div>
                ))}
            </div>
            <div className="grid-border grid-border-top"></div>
            <div className="grid-border grid-border-right"></div>
            <div className="grid-border grid-border-bottom"></div>
            <div className="grid-border grid-border-left"></div>
        </div>
    );
};



function GameGrid({ currentGame, newGameSetting }) {
    if (currentGame.status !== 'active') {
        return renderPreviewGrid(newGameSetting.gridSize);
    }
    
    return renderGameGrid(currentGame);
}

export default GameGrid;