import {React,Component} from "react";
import './form.css';
import Papa from 'papaparse';

// Create a class-based component named FormValue
class FormValue extends Component {
  // Initialize the state in the constructor
  constructor() {
    super();
    this.state = {
      isError: false,
      apimessage: "",
      data: [],
    };

    // Bind the 'this' context to the handler function
    this.onValueChange = this.onValueChange.bind(this);
    this.formSubmit = this.formSubmit.bind(this);
  }
  // This method will be called when the user clicks on a radio button
  onValueChange(event) {
    this.setState({
      selectedOption: event.target.value
    });

  }

  exportDataAsCSV = () => {
    const data = this.state.data;
    if (data && data.length > 0) {
        const csv = Papa.unparse(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('hidden','');
        link.setAttribute('href', url);
        link.setAttribute('download', 'data.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert('No data to export');
    }
  }


  // This method will be called when the user clicks on the submit button
  formSubmit(event) {
    // Prevent default form submission behavior
    event.preventDefault();

    // Get the form data
    const form = event.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());

    // Body for the API call
    const data = {
      "database_url": formJson.database_url,
      "query": formJson.query,
      "database_type": formJson.database_type,
      "server_address": formJson.server_address,
      "database_name": formJson.database_name,
      "username": formJson.username,
      "password": formJson.password
    }
    
    // API Call
    fetch('http://localhost:5000/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    })
    // Get the response from the API call
    .then(response => response.json())
    // Store the data returned by the API call
    .then(data => {
      // Check if the API call was successful
      if(data.status === "Success"){
        this.setState({data: data.message})
        alert("Database connected successfully");
        console.log(data.message);
        this.setState({isError: false});
        this.setState({apimessage: data.message});
      }
      else{
        this.setState({isError: true});
        this.setState({apimessage: data.message});
      }
    }
    // Catch and log any errors
    ).catch(error => {
      alert("Error select a database");
      data.status = "Error";
    })
  }
  
  // Render the component on the screen
  render() {
    const { isError, apimessage, data } = this.state;
    return (
      <div className="form-container">
        <form onSubmit={this.formSubmit} id="body">
          <div className="title">
            <h4>Choose Your Preferred Database</h4>
          </div>
          <div className="radio-group">
            <div className="radio">
              <label id="dbtype">
                <input type="radio" value="postgres" name="database_type" />
                PostgreSQL
              </label>
              <p>The official PostgreSQL JDBC Driver</p>
            </div>
            <div className="radio">
              <label id="dbtype">
                <input type="radio" value="mysql" name="database_type" />
                MySQL
              </label>
              <p>The official MySQL JDBC Driver</p>
            </div>
          </div>
          <hr />
          <div className="title">
            <h4>Enter Connection Details of the Selected Database</h4>
          </div>
          <div className="form-details">
            <table cellSpacing="0">
              <tbody>
                <tr id="row">
                  <td id="details"><label id="details">URL:</label></td>
                  <td id="input"><label>URL for the database</label><br/><input className="ip" type="text" name="database_url" defaultValue="None"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Database Name:</label></td>
                  <td id="input"><label>Name your Database</label><br/><input className="ip" type="text" name="database_name" defaultValue="None"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Server Address:</label></td>
                  <td id="input"><label>Enter Server Address</label><br/><input className="ip" type="text" name="server_address" defaultValue="None"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Port:</label></td>
                  <td id="input"><label>Port number for your database</label><br/><input type="text" name="port" className="port"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Username:</label></td>
                  <td id="input"><label>Username to access your database</label><br/><input className="ip" type="text" name="username" defaultValue="None"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Password:</label></td>
                  <td id="input"><label>Password for the user</label><br/><input className="ip" type="password" name="password" defaultValue="None"/></td>
                </tr>
                <tr id="row">
                  <td id="details"><label id="details">Query:</label></td>
                  <td id="input"><label>Enter query</label><br/><input className="ip" type="text" name="query" defaultValue="None"/></td>
                </tr>
              </tbody>
            </table>
            <button className="btn" type="submit">
              Submit
            </button>
          </div>
          <div className={`error ${isError ? 'show' : 'hide'}`}>
            <span className="message">Error: {apimessage}</span>
          </div>
        </form>
        <div className="table-display">
          {data.length > 1 && (
            <table>
              <thead>
                <tr>
                  {data[0].map((head, headIndex) => <th key={headIndex}>{head}</th>)}
                </tr>
              </thead>
              <tbody>
                {data.slice(1).map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => <td key={cellIndex}>{cell}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <button className="btn" type="button" onClick={this.exportDataAsCSV}>
          Export as CSV
        </button>
      </div>
    );
  }
}

export default FormValue;