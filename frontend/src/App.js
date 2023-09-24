import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import FormValue from './databaseSelect';
import AdminPage from './adminpage'; // Adjust the import path if needed
import HomePage from './HomePage';
// import any other components you have

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li><Link to="/">Home Page</Link></li>
            <li><Link to="/home">Database Select</Link></li>
            <li><Link to="/admin">Admin Page</Link></li>
            {/* Add more Links as needed */}
          </ul>
        </nav>

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
      <h2 style={{ color: "black", textAlign: "center", fontFamily: "Roboto" }}>
        Database Select
      </h2>
      <p
        style={{
          color: "black",
          textAlign: "center",
          fontFamily: "Roboto",
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
