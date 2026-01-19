import { LeadClassification } from '../types/contact';

export const LEAD_CLASSIFICATIONS: LeadClassification[] = [
  'New',
  'Contacted',
  'Growing Interest',
  'Leading',
  'Converted',
  'Cold',
  'Dying',
];

export const LEAD_CLASS_COLORS: Record<LeadClassification, string> = {
  'New': 'bg-blue-100 text-blue-800',
  'Contacted': 'bg-yellow-100 text-yellow-800',
  'Growing Interest': 'bg-orange-100 text-orange-800',
  'Leading': 'bg-purple-100 text-purple-800',
  'Converted': 'bg-green-100 text-green-800',
  'Cold': 'bg-gray-100 text-gray-800',
  'Dying': 'bg-red-100 text-red-800',
};

export const TODO_PRIORITIES = ['low', 'medium', 'high'] as const;

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const ROUTES = {
  dashboard: '/dashboard',
  contacts: '/contacts',
  contactDetail: (id: number) => `/contacts/${id}`,
  apex: '/apex',
  apexDetail: (id: number) => `/apex/${id}`,
  superResearcher: '/super-researcher',
  superResearcherDetail: (id: number) => `/super-researcher/${id}`,
  research: '/research',
  stagedLeads: '/research/staged',
  activeLeads: '/research/active',
  todos: '/todos',
  communications: '/communications',
  emails: '/communications/emails',
  sms: '/communications/sms',
} as const;