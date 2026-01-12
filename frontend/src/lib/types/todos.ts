export type TodoPriority = 'low' | 'medium' | 'high';

export interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: TodoPriority;
  date: string;
  created_by?: number;
}

export interface TodoFormData {
  title: string;
  description?: string;
  priority?: TodoPriority;
}

export interface TodoFilters {
  completed?: boolean;
  priority?: TodoPriority;
}