import { Student, Evaluation, SupervisorProfile, WeeklyFeedback } from '../../types/supervisor'

// Base API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = {
  get: async (endpoint: string) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      }
    })
    return response.json()
  },
  
  post: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify(data)
    })
    return response.json()
  },
  
  put: async (endpoint: string, data: any) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify(data)
    })
    return response.json()
  }
}

export const supervisorAPI = {
  // Get students assigned to supervisor
  getStudents: (): Promise<Student[]> => {
    return apiClient.get('/supervisors/students')
  },
  
  // Submit weekly feedback
  submitFeedback: (feedback: WeeklyFeedback): Promise<void> => {
    return apiClient.post('/supervisors/feedback', feedback)
  },
  
  // Get evaluations for supervisor
  getEvaluations: (): Promise<Evaluation[]> => {
    return apiClient.get('/supervisors/evaluations')
  },
  
  // Submit evaluation
  submitEvaluation: (evaluation: Evaluation): Promise<void> => {
    return apiClient.post('/supervisors/evaluations', evaluation)
  },
  
  // Update supervisor profile
  updateProfile: (profile: SupervisorProfile): Promise<void> => {
    return apiClient.put('/supervisors/profile', profile)
  },
  
  // Get supervisor profile
  getProfile: (): Promise<SupervisorProfile> => {
    return apiClient.get('/supervisors/profile')
  },
  
  // Get student progress details
  getStudentProgress: (studentId: string): Promise<Student> => {
    return apiClient.get(`/supervisors/students/${studentId}`)
  }
}