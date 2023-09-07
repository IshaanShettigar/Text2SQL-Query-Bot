import FormValue from './databaseSelect';
function App() {
  return (
    <div className="App">
      <h2 style={{color:"white",textAlign:"center",fontFamily:"Roboto"}}>Database Select</h2>
      <p style={{color:"white",textAlign:"center",fontFamily:"Roboto"}}>A database selection tool designed to assist users in choosing the most appropriate database management system (DBMS) for their specific application or project requirements.</p>
      <div className="forms">
        <FormValue/>
      </div>
    </div>
  );
}

export default App;
