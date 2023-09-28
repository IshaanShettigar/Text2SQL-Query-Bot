import React, { Component } from "react";
import Papa from 'papaparse';
import './chatui.css'

class FormValue extends Component {
  constructor() {
    super();
    this.state = {
      isError: false,
      apimessage: "",
      data: [],
      databases: [],
      selectedDatabase: null,
      sql: "",
      question: "",
      selectedThumb: null,
    };

    this.formSubmit = this.formSubmit.bind(this);
    this.handleThumbsUp = this.handleThumbsUp.bind(this);
    this.handleThumbsDown = this.handleThumbsDown.bind(this);
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

  handleThumbsUp = async () => {
    if (this.state.selectedThumb !== 'up') {
      this.setState({ selectedThumb: 'up' });
      this.handleThumb('up');
    }
  };

  handleThumbsDown = async () => {
    if (this.state.selectedThumb !== 'down') {
      this.setState({ selectedThumb: 'down' });
      this.handleThumb('down');
    }
  };

  handleThumb(type) {
    const { question, generatedSQL } = this.state;
    fetch(`http://localhost:5000/thumb_${type}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question, sql: generatedSQL }),
    }).catch(error => {
      console.error(`Error in thumbs ${type}:`, error);
    });

    if (type === 'up') {
      this.setState(prevState => ({ thumbsUp: prevState.thumbsUp + 1 }));
    } else {
      this.setState(prevState => ({ thumbsDown: prevState.thumbsDown + 1 }));
    }
  }

  exportDataAsCSV = () => {
    const data = this.state.data;
    if (data && data.length > 0) {
      const csv = Papa.unparse(data);
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('hidden', '');
      link.setAttribute('href', url);
      link.setAttribute('download', 'data.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      alert('No data to export');
    }
  }

  async formSubmit(event) {
    event.preventDefault();

    if (!this.state.selectedDatabase) {
      alert("Please select a database.");
      return;
    }

    const form = event.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());

    const data = {
      ...formJson,
      database_url: this.state.selectedDatabase.url,
      database_name: this.state.selectedDatabase.name,
      database_type: this.state.selectedDatabase.type,
      question: this.state.question,
    }

    try {
      // Wait for the SQL to be generated before proceeding.
      const generatedSQL = await this.getGeneratedSQL(data);
      this.setState({ generatedSQL });

      const data2 = {
        ...formJson,
        database_url: this.state.selectedDatabase.url,
        database_name: this.state.selectedDatabase.name,
        database_type: this.state.selectedDatabase.type,
        query: generatedSQL,
      }

      // Proceed with retrieve_data.
      fetch('http://localhost:5000/retrieve_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data2),
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
    } catch (error) {
      console.log(error);
      this.setState({ isError: true, apimessage: "Error: " + error });
    }
  }

  getGeneratedSQL(data) {
    return new Promise((resolve, reject) => {
      fetch('http://localhost:5000/generate_SQL', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...data,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === "Success") {
            this.setState({ generatedSQL: data.sql });
            resolve(data.sql);
          } else {
            this.setState({ isError: true, apimessage: data.message });
            reject(data.message);
          }
        })
        .catch(error => {
          console.log(error);
          this.setState({ isError: true, apimessage: "Unable to generate SQL" });
          reject("Unable to generate SQL");
        });
    });
  }

  render() {
    const { isError, apimessage, data, databases } = this.state;
    return (
      <div className="parent">
        <form className="input-container" onSubmit={this.formSubmit}>
          <select onChange={this.onDatabaseChange} className="select-db">
            <option value="" disabled selected>Select a Database</option>
            {databases.map(db => (
              <option value={db.name} key={db.name}>{db.database_name} ({db.type})</option>
            ))}
          </select>
          <img src={require("./assets/search.png")} alt="Search icon" style={{ width: '20px' }} />
          <input type="text" placeholder="Ask a question about your data..." onChange={(e) => this.setState({ question: e.target.value })} />
          <button type="button" className="cross-btn"><img src={require("./assets/cross.png")} style={{ width: '15px' }} alt="Cross button" /></button>
          <button type="submit" className="go-btn">Go</button>
        </form>

        <div className="card-container">
          <div className="card" id="card1">
            <p className="question">Give me all Male Patients</p>
            <p className="db-name">Thrombosis Prediction</p>
          </div>
          <div class="card" id="card2">
            <p class="question">Give me everyone that has the most severe thrombosis</p>
            <p class="db-name">Thrombosis Prediction</p>
          </div>
          <div class="card" id="card3">
            <p class="question">Give me all IDs who have SLE disease</p>
            <p class="db-name">Thrombosis Prediction</p>
          </div>
        </div>

        <div>
          <p>Generated SQL: {this.state.generatedSQL}</p>
          {this.state.data.length > 1 && (
            <div className="thumbs-container">
              <button type="button" onClick={this.handleThumbsUp} className={`thumbs-up ${this.state.selectedThumb === 'up' ? 'selected' : ''}`}>
                Thumbs Up 👍
              </button>
              <button type="button" onClick={this.handleThumbsDown} className={`thumbs-down ${this.state.selectedThumb === 'down' ? 'selected' : ''}`}>
                Thumbs Down 👎
              </button>
            </div>
          )}
        </div>

        <div className={`error ${isError ? 'show' : 'hide'}`}>
          <span className="message">Error: {apimessage}</span>
        </div>

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

        {/* Export as CSV Button */}
        <button className="btn" type="button" onClick={this.exportDataAsCSV}>
          Export as CSV
        </button>

      </div>
    );
  }
}

export default FormValue;