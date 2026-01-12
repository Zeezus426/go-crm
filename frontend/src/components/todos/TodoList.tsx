'use client';

import React, { useState } from 'react';
import { Todo } from '@/lib/types/todos';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: number, completed: boolean) => void;
  onDelete: (id: number) => void;
}

const priorityColors: Record<string, 'gray' | 'blue' | 'red'> = {
  'low': 'gray',
  'medium': 'blue',
  'high': 'red',
};

export function TodoList({ todos, onToggle, onDelete }: TodoListProps) {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  const filteredTodos = todos.filter((todo) => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  return (
    <div className="space-y-4">
      <div className="flex space-x-2 mb-4">
        <Button
          variant={filter === 'all' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setFilter('all')}
        >
          All
        </Button>
        <Button
          variant={filter === 'active' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setFilter('active')}
        >
          Active
        </Button>
        <Button
          variant={filter === 'completed' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setFilter('completed')}
        >
          Completed
        </Button>
      </div>

      <div className="space-y-3">
        {filteredTodos.map((todo) => (
          <Card key={todo.id} className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={(e) => onToggle(todo.id, e.target.checked)}
                className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <div className={`flex-1 ${todo.completed ? 'opacity-50 line-through' : ''}`}>
                <h4 className="font-medium text-gray-900">{todo.title}</h4>
                {todo.description && (
                  <p className="text-sm text-gray-600 mt-1">{todo.description}</p>
                )}
                <div className="flex items-center space-x-2 mt-2">
                  <Badge variant={priorityColors[todo.priority]} size="sm">
                    {todo.priority}
                  </Badge>
                  <span className="text-xs text-gray-500">
                    {new Date(todo.date).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
            <Button
              variant="danger"
              size="sm"
              onClick={() => onDelete(todo.id)}
            >
              Delete
            </Button>
          </Card>
        ))}
      </div>

      {filteredTodos.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          {filter === 'all'
            ? 'No todos yet. Create one to get started!'
            : `No ${filter} todos.`}
        </div>
      )}
    </div>
  );
}