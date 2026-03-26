import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Employees from './pages/Employees'
import EmployeeForm from './pages/EmployeeForm'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'

function App() {
  return (
    <BrowserRouter>
    <Navbar />

      <Routes>

        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute> }  />
        <Route path="/employees" element={  <ProtectedRoute><Employees /></ProtectedRoute>  }  />
         <Route path="/employees/create" element={<ProtectedRoute><EmployeeForm /></ProtectedRoute>} />
         <Route path="/employees/edit/:id" element={<ProtectedRoute><EmployeeForm /></ProtectedRoute>} />
       </Routes>
    </BrowserRouter>
  )
}

export default App