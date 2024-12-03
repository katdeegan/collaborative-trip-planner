/* Home page after user logs in. User can view list of all trip
groups they are a member of, and create a new trip group. */

import React, { Component } from "react";
import { Table } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faPlus } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import Title from './Title';
<<<<<<< HEAD
import '../styles/form-styles.css'; 

function Home({username, userId}) {
  const handleLogOut = () => {
=======

class Home extends Component {
    // TO-DO - check if uses is logged in
    constructor(props) {
        super(props);
        // Initialize state
        this.state = {
            isAuthenticated: true
          //isAuthenticated: localStorage.getItem('authToken') ? true : false, // Check if the user is logged in
        };
      }
    
      // Handle log out
      handleLogOut = () => {
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
        console.log('Loggin user out...');
        // log user out
        /*
        this.setState({ isAuthenticated: false }); // Update the state to logged out
        localStorage.removeItem('authToken'); // Remove the authentication token
        */
      };

<<<<<<< HEAD
  return (
            <>
            <div className='two-item-grid-container'>
              <h4>Welcome, {username}!</h4>
                <Link to='/login'>
                <button onClick={handleLogOut}>Log Out</button>
=======
    render() {
        return (
            <>
            <div>
                <Link to='/login'>
                <button onClick={this.handleLogOut}>Log Out</button>
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
                </Link>
            </div>
            <Title/>
            <TripGroupList/>
            <div>
                <Link to='/createtrip'>
                <button style={{ alignItems: 'center', padding: '10px 20px', borderRadius: '5px' }}>
                <FontAwesomeIcon icon={faPlus} style={{ marginRight: '8px' }} />
                New Trip
                </button>
                </Link>
            </div>
            </>
<<<<<<< HEAD
        );
    
=======
        )
    }
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
}


class TripGroupList extends Component {
    // TO DO - dyanmically retrieve trip list

    /*
    constructor(props) {
        super(props);
        this.state = {
          data: [],        // To store the fetched data
          loading: true,   // To track loading state
          error: null,     // To track any errors
        };
      }
    
      // Lifecycle method to fetch data when the component mounts
      componentDidMount() {
        this.fetchData();
      }
    
      // Fetch data from an API or database
      async fetchData() {
        try {
          const response = await fetch('/api/data'); // Replace with your API endpoint
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const result = await response.json();
          this.setState({
            data: result,   // Set the fetched data
            loading: false, // Set loading to false when data is fetched
          });
        } catch (error) {
          this.setState({
            error: error.message, // Set error message in state
            loading: false,       // Set loading to false even if there's an error
          });
        }
      } */
    
    render() {
        /*
        const { data, loading, error } = this.state;

        if (loading) {
        return <div>Loading...</div>;
        }

        if (error) {
        return <div>Error: {error}</div>;
        }*/

        // TO DO - delete. placeholder trip list.
        const tripGroups = ["Trip 1", "Roadtrip!!", "BOATS"];
        const tripId = 100;

        return (
            <Table>
                <thread>
                    <th>Trip Groups</th>
                    <th></th>
                </thread>
                <tbody>
                    {tripGroups.map((item, idx) => (
                        <tr key={idx}>
                            {/* TO dO - update based on DB, link to trip detail page */}
                            <td>{item}</td>
                            <td>
                                <Link to={`/trip/${tripId}`}>
                                    <FontAwesomeIcon icon={faArrowRight} />
                                </Link>
                            </td>
            
                        </tr>
                    ))}
                </tbody>
            </Table>

        )
    }
}



export default Home;
