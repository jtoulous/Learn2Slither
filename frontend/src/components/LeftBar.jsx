import React from "react";
import { GlobalState } from '../State.jsx';
import StatusIndicator from './StatusIndicator.jsx';
import "./LeftBar.css";

function LeftBar() {
    const {
        agentsList,
        showLeftBar, setShowLeftBar
    } = GlobalState();

    return (
        <div className="left-bar-wrapper">
            <div className={`left-bar ${showLeftBar ? "open" : ""}`}>
                {Object.entries(agentsList).map(([eq, status]) => (
                    <a key={eq} className="agent-link" href={`/agent?agent_name=${eq}`}>
                        <StatusIndicator status={status} />
                        <span className="agent-name">{eq}</span>
                    </a>
                ))}
                {showLeftBar && (
                    <div className="retract-arrow" onClick={() => setShowLeftBar(false)}>❮</div>
                )}
            </div>
            {!showLeftBar && (
                <div className="toggle-arrow" onClick={() => setShowLeftBar(true)}>
                    ❯
                </div>
            )}
        </div>
    );
}

export default LeftBar;
