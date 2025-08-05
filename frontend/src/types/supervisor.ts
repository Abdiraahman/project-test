export interface SupervisorProfile {
  id: string
  name: string
  email: string
  phone: string
  company: string
  position: string
  bio: string
}

export interface StudentProgress {
  studentId: string
  supervisorId: string
  weeklyReports: WeeklyReport[]
  overallProgress: number
  currentTasks: Task[]
}

export interface WeeklyReport {
  weekNumber: number
  submissionDate: string
  content: string
  feedback?: string
  rating?: number
}

export interface Task {
  id: string
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed'
  dueDate: string
  priority: 'low' | 'medium' | 'high'
}

export interface Student {
  id: string
  name: string
  email: string
  phone: string
  university: string
  course: string
  year: number
  supervisorId: string
  progress: StudentProgress
}

export interface Evaluation {
  id: string
  studentId: string
  supervisorId: string
  type: 'weekly' | 'midterm' | 'final'
  score: number
  maxScore: number
  feedback: string
  submittedAt: string
  criteria: EvaluationCriteria[]
}

export interface EvaluationCriteria {
  id: string
  name: string
  description: string
  score: number
  maxScore: number
  weight: number
}

export interface WeeklyFeedback {
  id: string
  studentId: string
  supervisorId: string
  weekNumber: number
  feedback: string
  rating: number
  submittedAt: string
  tasks: Task[]
}