import React, {useState} from 'react'
import Home from './subcomponents/main/Home'
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import TripDetail from './subcomponents/main/TripDetail';
import LogIn from './subcomponents/main/LogIn';
import CreateTrip from './subcomponents/main/CreateTrip';
import CreateAccount from './subcomponents/main/CreateAccount';
import EditTripDay from './subcomponents/main/EditTripDay';
import EditTripMembers from './subcomponents/main/EditTripMembers';
import UploadFile from './subcomponents/main/UploadFile';
import './App.css';

const initialState = {
  userId: '',
  username: '',
  tripId: '',
  tripDayNum: '',
  tripDayDate: '',
};


function App() {
  const [user, setUser] = useState(initialState.userId);
  const [username, setUsername] = useState(initialState.username);
  const [tripId, setTripId] = useState(initialState.tripId);
  const [tripDayNum, setTripDayNum] = useState(initialState.tripDayNum);
  const [tripDayDate, setTripDayDate] = useState(initialState.tripDayDate);

  const onUserChange = (userId, username) => {
    setUser(userId)
    setUsername(username)
    console.info('User state changed. userId: ' + userId + ' , username: ' + username);

  }

  const onTripChange = (tripId) => {
    setTripId(tripId)
    console.info('Trip ID changed. tripId: ' + tripId);

  }

  const onTripDayChange = (dayNum, dayDate) => {
    setTripDayNum(dayNum)
    setTripDayDate(dayDate)
    console.info('Trip day changed. Day ' + tripDayNum + ' ,' + tripDayDate);

  }



  return (
    <Router>
      <Routes>
        <Route 
          path='/'
          element={user ? <Home username={username} userId={user} onUserChange = {onUserChange} tripId = {tripId} onTripChange = {onTripChange}/> : <Navigate to="/login" />}
        />
        <Route path='/tripDetails' element={<TripDetail userId={user} tripId={tripId} onTripChange = {onTripChange} onTripDayChange = {onTripDayChange}/>} />
        <Route path='/login' element={<LogIn onUserChange = {onUserChange} />} />
        <Route path='/createaccount' element={<CreateAccount onUserChange = {onUserChange} />} />
        <Route path='/createtrip' element={<CreateTrip userId={user}/>} />
        <Route path='/editTripDay' element={<EditTripDay userId={user} tripId={tripId} tripDayNum={tripDayNum} tripDayDate={tripDayDate} onTripDayChange={onTripDayChange}/>} />
        <Route path='/editTripMembers/:tripId' element={<EditTripMembers tripId={tripId}/>} />
        <Route path='/uploadTripDocument' element={<UploadFile userId={user} tripId={tripId}/>} />


      </Routes>
    </Router>
  )
}

export default App;
