import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'
import SupervisorDashboard from './pages/dashboard/SupervisorDashboard'
import StudentProgress from './components/features/supervisors/StudentProgress'
import EvaluationForm from './components/features/supervisors/EvaluationForm'
import WeeklyFeedback from './components/features/supervisors/WeeklyFeedback'
import ProfileEdit from './pages/profile/ProfileEdit'
import ProfileSetup from './pages/profile/ProfileSetup'
import './App.css'

function App(): React.JSX.Element {
  return (
    <Router>
      <Routes>
        {/* Profile setup route (standalone, no layout) */}
        <Route path="/profile-setup" element={<ProfileSetup />} />
        
        {/* Supervisor dashboard routes with layout */}
        <Route path="/supervisor" element={<MainLayout />}>
          <Route index element={<SupervisorDashboard />} />
          <Route path="dashboard" element={<SupervisorDashboard />} />
          <Route path="students" element={<StudentProgress />} />
          <Route path="evaluations" element={<EvaluationForm />} />
          <Route path="feedback" element={<WeeklyFeedback />} />
          <Route path="profile" element={<ProfileEdit />} />
        </Route>
        
        {/* Redirect root to supervisor dashboard for now */}
        <Route path="/" element={<SupervisorDashboard />} />
      </Routes>
    </Router>
  )
}

export default App
