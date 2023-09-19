import FormValue from './databaseSelect';
function App() {
  return (
    <div className="App">
      <h2 style={{color:"black",textAlign:"center",fontFamily:"Roboto"}}>Database Select</h2>
      <p style={{color:"black",textAlign:"center",fontFamily:"Roboto"}}>A database selection tool designed to assist users retreive SQL commands for chosen  database.</p>
      <div className="forms">
        <FormValue/>
      </div>
    </div>
  );
}

export default App;