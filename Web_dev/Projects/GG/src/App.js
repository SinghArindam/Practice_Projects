
import './App.css';

import React, { Component, useState } from 'react'
import Navbar from './components/Navbar';
import News from './components/News';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoadingBar from 'react-top-loading-bar' 
export default function App () {
  const apiKey=process.env.REACT_APP_NEWS_API
  const[progress, setProgress1]=useState(0);
 
 const setProgress=(progress)=>{
    setProgress1(progress);
  }

    return (
      <div>
   {/* Without a unique key, React assumes that the component hasn't changed and does not reinitialize it,    */}
<Router>
<Navbar/>
<LoadingBar
        color='#f11946'
        progress={progress}
      
       
      />
<div className="container main">
<Routes>
  <Route exact path="/"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="latest" pagesize={6} country={"us"} category={"latest"} />
  }
 
  />
    <Route exact path="/business"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="business" pagesize={6} country={"us"} category={"business"} />
  }
  />
   <Route exact path="/entertainment"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="entertainment" pagesize={6} country={"us"} category={"entertainment"} />
  }
  />
   <Route exact path="/health"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="health" pagesize={6} country={"us"} category={"health"} />
  }
  />
   <Route exact path="/science"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="science" pagesize={6} country={"us"} category={"science"} />
  }
  />
   <Route exact path="/sports"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="sports" pagesize={6} country={"us"} category={"sport"} />
  }
  />
   <Route exact path="/technology"
  element={
    <News setProgress={setProgress} apiKey={apiKey} key="technology" pagesize={6} country={"us"} category={"technology"} />
  }
  />
  
</Routes>
</div>
</Router>
      
      </div>
    )
 
}




