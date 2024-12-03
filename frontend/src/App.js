import React, {useState} from 'react'
import Home from './subcomponents/main/Home'
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import TripDetail from './subcomponents/main/TripDetail';
import LogIn from './subcomponents/main/LogIn';
import CreateTrip from './subcomponents/main/CreateTrip';
import CreateAccount from './subcomponents/main/CreateAccount';
import EditTripDay from './subcomponents/main/EditTripDay';
import EditTripMembers from './subcomponents/main/EditTripMembers';
import './App.css';

const initialState = {
  userId: '',
  username: ''
};


function App() {
  //const [route, setRoute] = useState(initialState.route);  // route state
  const [user, setUser] = useState(initialState.userId);
  const [username, setUsername] = useState(initialState.username);

  const onUserChange = (userId, username) => {
    setUser(userId)
    setUsername(username)
    console.info('User state changed. userId: ' + userId + ' , username: ' + username);

  }
  return (
    // pass state change methods to other pages, e.g. onRouteChange = {this.onRouteChange}
    // access methods from within pages via this.prop.onRouteChange(

    <Router>
      <Routes>
        <Route 
          path='/'
          element={user ? <Home username={username} userId={user}/> : <Navigate to="/login" />}
        />
        <Route path='/trip/:id' element={<TripDetail />} />
        <Route path='/login' element={<LogIn onUserChange = {onUserChange} />} />
        <Route path='/createaccount' element={<CreateAccount />} />
        <Route path='/createtrip' element={<CreateTrip />} />
        <Route path='/editTripDay/:dayNum/:tripId/:date' element={<EditTripDay />} />
        <Route path='/editTripMembers/:tripId' element={<EditTripMembers />} />


      </Routes>
    </Router>
  )
}

export default App;
