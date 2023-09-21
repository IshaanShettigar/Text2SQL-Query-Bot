import React, { Component } from "react";
import './databaseSelect.css';
import Papa from 'papaparse';

class FormValue extends Component {
  constructor() {
    super();
    this.state = {
      isError: false,
      apimessage: "",
      data: [],
      databases: [],
      selectedDatabase: null,
    };
    
    this.formSubmit = this.formSubmit.bind(this);
}


  componentDidMount() {
    fetch('http://localhost:5000/getDB')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.status === 'Success') {
          this.setState({ databases: data.databases });
        } else {
          console.error('Error fetching databases:', data.message);
        }
      })
      .catch(error => console.error('Error fetching databases:', error));
  }

  onDatabaseChange = (event) => {
    const selectedDbName = event.target.value;
    const selectedDb = this.state.databases.find(db => db.name === selectedDbName);
    this.setState({
      selectedDatabase: selectedDb,

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

  formSubmit(event) {
    event.preventDefault();

    if (!this.state.selectedDatabase) {
      alert("Please select a database.");
      return;
    }


    const form = event.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());

    // Update data with selectedDatabase details
    const data = {
      ...formJson,
      database_url: this.state.selectedDatabase.url,
      database_name: this.state.selectedDatabase.name,
      database_type: this.state.selectedDatabase.type,
    }
    console.log('Sending Data:', data);

    fetch('http://localhost:5000/retrieve', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "Success") {
          this.setState({ data: data.message, isError: false, apimessage: data.message });
          alert("Database connected successfully");
        }
        else {
          this.setState({ isError: true, apimessage: data.message });
        }
      })
      .catch(error => {
        alert("Error: Unable to connect to the database");
        console.log(error);
        this.setState({ isError: true, apimessage: "Unable to connect to the database" });
      })
  }

  render() {
    const { isError, apimessage, data, databases } = this.state;
    return (
      <div className="form-container">
        <form onSubmit={this.formSubmit} id="body">
          <div className="title">
            <h4>Choose Your Preferred Database</h4>
          </div>
          <div className="radio-group">
            <select onChange={this.onDatabaseChange} className="input">
              <option value="" disabled selected>Select a Database</option>
              {databases.map(db => (
                <option value={db.name} key={db.name}>{db.database_name} ({db.database_type})</option>
              ))}
            </select>
          </div>

          <div className="form-details">
            <table cellSpacing="0">
              <tbody>
                <tr id="row">
                  <td id="input"><label className="label">Enter query</label><input className="input" type="text" name="query" defaultValue="None"/></td>
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