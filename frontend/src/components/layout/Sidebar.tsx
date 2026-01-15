'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: '📊' },
  { name: 'Contacts', href: '/contacts', icon: '👥' },
  { name: 'Apex Research', href: '/apex', icon: '🔬' },
  { name: 'Super Researcher', href: '/super-researcher', icon: '🧪' },
  { name: 'Research Pipeline', href: '/research', icon: '📈' },
  // { name: 'Communications', href: '/communications', icon: '💬' },
  { name: 'Todos', href: '/todos', icon: '✅' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 bg-gray-900 min-h-screen p-4">
      <div className="flex items-center justify-center mb-8">
        <h1 className="text-2xl font-bold text-white">Go-CRM</h1>
      </div>

      <nav className="space-y-2">
        {navigation.map((item) => {
          const isActive = pathname?.startsWith(item.href);
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}