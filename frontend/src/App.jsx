import React from 'react'
import { Routes, Route } from "react-router-dom"

import WebsocketManager from './services/WebsocketManager.jsx'

import TopBar from './components/TopBar.jsx'
import LeftBar from './components/LeftBar.jsx'

import Home from './pages/Home.jsx'
import Agent from './pages/Agent.jsx'


function App() {
  return (
    <>
      <WebsocketManager />
      <TopBar />
      <LeftBar />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/agent' element={<Agent />} />
      </Routes>
    </>
  )
}
  

export default App
