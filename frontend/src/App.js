import Home from './subcomponents/main/Home'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TripDetail from './subcomponents/main/TripDetail';
import LogIn from './subcomponents/main/LogIn';
import CreateTrip from './subcomponents/main/CreateTrip';
import CreateAccount from './subcomponents/main/CreateAccount';
import EditTripDay from './subcomponents/main/EditTripDay';
import EditTripMembers from './subcomponents/main/EditTripMembers';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/trip/:id' element={<TripDetail />} />
        <Route path='/login' element={<LogIn />} />
        <Route path='/createaccount' element={<CreateAccount />} />
        <Route path='/createtrip' element={<CreateTrip />} />
        <Route path='/editTripDay/:dayNum/:tripId/:date' element={<EditTripDay />} />
        <Route path='/editTripMembers/:tripId' element={<EditTripMembers />} />


      </Routes>
    </Router>
  );
}

export default App;
