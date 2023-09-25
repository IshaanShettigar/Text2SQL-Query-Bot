import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import FormValue from './databaseSelect';
import AdminPage from './adminpage'; // Adjust the import path if needed
import HomePage from './HomePage';
import Header from './Header'; // Import the Header component

// import any other components you have

function App() {

  return (
    <Router>
      <div className="App">

        <Header /> {/* Pass the callback function */}

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/home" element={<Home />} />
          {/* Add more Routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h2 style={{ color: "black", textAlign: "center", fontFamily: "Arial", margin: "50px 0 20px 0" }}>
        Database Select
      </h2>
      <p
        style={{
          color: "black",
          textAlign: "center",
          fontFamily: "Arial",
        }}
      >
        A database selection tool designed to assist users retrieve SQL commands for chosen database.
      </p>
      <div className="forms">
        <FormValue />
      </div>
    </div>
  );
}

export default App;
