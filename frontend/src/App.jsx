import {BrowserRouter, Routes, Route} from 'react-router-dom'
import './App.css'
import Login from './pages/login.jsx'
import Register from './pages/register.jsx'
import Dashboard from './pages/dashboard.jsx'
import DatasetPage from './pages/datasetpage.jsx'
import ProtectedRoute from './pages/protectedroute.jsx'
import Generator from './pages/generator.jsx'
import UploadDataset from './pages/uploadDataset.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
            <ProtectedRoute>
                <Dashboard />
            </ProtectedRoute>} />
        <Route path='/projects/:projectID' element={<ProtectedRoute>  <DatasetPage /> </ProtectedRoute>}/>
        <Route path='/generator/:projectID' element={<ProtectedRoute> <Generator /> </ProtectedRoute>}/>
        <Route path='/uploads/:projectID' element={<ProtectedRoute> <UploadDataset /> </ProtectedRoute>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
