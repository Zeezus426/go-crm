import { useState, useEffect, useCallback } from 'react';
import { todosApi } from '../api/todos';
import { Todo, TodoFormData, TodoFilters } from '../types/todos';
import { ApiError } from '../api/client';

export function useTodos(filters?: TodoFilters) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTodos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await todosApi.getAllTodos(filters);
      setTodos(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to fetch todos');
      }
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const createTodo = useCallback(async (data: TodoFormData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await todosApi.createTodo(data);
      await fetchTodos();
      return result;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to create todo');
      }
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchTodos]);

  const updateTodo = useCallback(async (id: number, data: TodoFormData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await todosApi.updateTodo(id, data);
      await fetchTodos();
      return result;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to update todo');
      }
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchTodos]);

  const deleteTodo = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const result = await todosApi.deleteTodo(id);
      await fetchTodos();
      return result;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to delete todo');
      }
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchTodos]);

  const toggleTodoComplete = useCallback(async (id: number, completed: boolean) => {
    return updateTodo(id, { title: '', completed } as TodoFormData);
  }, [updateTodo]);

  return {
    todos,
    loading,
    error,
    refetch: fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodoComplete,
  };
}