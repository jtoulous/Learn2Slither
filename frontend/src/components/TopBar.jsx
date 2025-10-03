import React from "react"

import logo from "../assets/suez_logo.png" 
import "./TopBar.css"


function TopBar() {
  return (
    <div className="top-bar">
      <div className="top-bar-logo">
        <img src={logo} alt="SUEZ Logo" />
      </div>
      <h1>
        <a href="/" className="top-bar-link">
          Learn2Slither
        </a>
      </h1>
    </div>
  )
}

export default TopBar