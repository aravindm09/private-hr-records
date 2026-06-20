import {BrowserRouter, Routes, Route} from 'react-router-dom'
import './App.css'
import Login from './pages/login.jsx'
import Register from './pages/register.jsx'
import Dashboard from './pages/dashboard.jsx'
import DatasetPage from './pages/datasetpage.jsx'
import ProtectedRoute from './pages/protectedroute.jsx'
import Generator from './pages/generator.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
            <ProtectedRoute>
                <Dashboard />
            </ProtectedRoute>
        } />
        <Route path='/projects/:projectID' element={<DatasetPage />}/>
        <Route path='/generator/:projectID' element={<Generator />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
