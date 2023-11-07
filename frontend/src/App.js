import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import FormValue from './databaseSelect';
import AdminPage from './adminpage';
import HomePage from './HomePage';
import Header from './Header';


function App() {

  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/home" element={<Home />} />
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
      <div className="forms">
        <FormValue />
      </div>
    </div>
  );
}

export default App;
