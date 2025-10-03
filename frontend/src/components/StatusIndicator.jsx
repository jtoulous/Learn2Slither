import React from "react";
import "./StatusIndicator.css";




const StatusIndicator = ({ status, className = "" }) => {
    return (
        <span className={`status-indicator ${status} ${className}`}>
            <span className={`status-dot status-${status}`}></span>
        </span>
    );
};

export default StatusIndicator;