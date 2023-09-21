import React, { Component } from "react";
import './adminpage.css';

class AdminPage extends Component {
    constructor() {
      super();
      this.state = {
        database_type: "",
        database_url: "",
        database_name: "",
      };
    }
  
    handleChange = (event) => {
      this.setState({
        [event.target.name]: event.target.value
      });
    }
  
    handleSubmit = (event) => {
      event.preventDefault();
  
      const { database_type, database_url, database_name } = this.state;
  
      // Simple form validation
      if (!database_type || !database_url || !database_name) {
        alert("Please fill out all fields.");
        return;
      }
  
      const data = {
        database_type,
        database_url,
        database_name,
      };
  
      fetch('http://localhost:5000/addDB', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => {
        if(data.status === "Success"){
          alert("Database added successfully");
          // Clearing the form fields after successful submission
          this.setState({
            database_type: "",
            database_url: "",
            database_name: "",
          });
        }
        else{
          alert("Error adding the database");
        }
      })
      .catch(error => {
        alert("Network error or server not responding. Please try again later.");
      });
    }
  
    render() {
        return (
          <div className="admin-container">
            <div className="admin-title">
              <h4>Admin Page</h4>
            </div>
            <form onSubmit={this.handleSubmit} className="form-group">
              <label className="label">
                Database Type:
                <select name="database_type" value={this.state.database_type} onChange={this.handleChange} className="input">
                  <option value="">Select Database Type</option>
                  <option value="mysql">MySQL</option>
                  <option value="postgres">PostgreSQL</option>
                </select>
              </label>
              <label className="label">
                Database URL:
                <input type="text" name="database_url" value={this.state.database_url} onChange={this.handleChange} placeholder="e.g., postgresql://user:password@host:port/dbname" className="input" />
              </label>
              <label className="label">
                Database Name:
                <input type="text" name="database_name" value={this.state.database_name} onChange={this.handleChange} placeholder="Enter a name for your database" className="input" />
              </label>
              <button type="submit" className="button">Add Database</button>
            </form>
          </div>
        );
      }
  }
  
  export default AdminPage;
  