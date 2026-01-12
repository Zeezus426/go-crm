import { apiClient } from './client';
import {
  Contact,
  ContactFormData,
  ContactFilters,
  SentEmail,
  SentSms,
  EmailFormData,
  SmsFormData,
} from '../types/contacts';

export const contactsApi = {
  // Get all contacts with optional filters
  getAllContacts: async (filters?: ContactFilters): Promise<Contact[]> => {
    const params: Record<string, string> = {};
    if (filters?.lead_class) params.lead_class = filters.lead_class;
    if (filters?.search) params.search = filters.search;
    if (filters?.sort_by) params.sort_by = filters.sort_by;

    return apiClient.get<Contact[]>('/api/contacts/index', params);
  },

  // Get single contact by ID
  getContactById: async (id: number): Promise<Contact> => {
    return apiClient.get<Contact>(`/api/contacts/moreinfo/${id}`);
  },

  // Create new contact
  createContact: async (data: ContactFormData): Promise<Contact> => {
    return apiClient.post<Contact>('/api/contacts/add', data);
  },

  // Update existing contact
  updateContact: async (id: number, data: ContactFormData): Promise<Contact> => {
    return apiClient.post<Contact>(`/api/contacts/update/${id}`, data);
  },

  // Delete contact
  deleteContact: async (id: number): Promise<{ success: boolean; message: string }> => {
    return apiClient.delete<{ success: boolean; message: string }>(`/api/contacts/delete/${id}`);
  },

  // Send email to contact
  sendEmail: async (id: number, data: EmailFormData): Promise<SentEmail> => {
    return apiClient.post<SentEmail>(`/api/contacts/send-email/${id}`, data);
  },

  // Send SMS to contact
  sendSms: async (id: number, data: SmsFormData): Promise<SentSms> => {
    return apiClient.post<SentSms>(`/api/contacts/send-sms/${id}`, data);
  },

  // Get contact's email history
  getContactEmails: async (id: number): Promise<SentEmail[]> => {
    return apiClient.get<SentEmail[]>(`/api/contacts/contact-emails/${id}`);
  },

  // Get all communication logs
  getCommunicationLogs: async (): Promise<{
    emails: Array<{
      id: number;
      contact: string;
      contact_id: number;
      subject: string;
      message: string;
      sent_at: string;
    }>;
    sms: Array<{
      id: number;
      contact: string;
      contact_id: number;
      body: string;
      sent_at: string;
    }>;
  }> => {
    return apiClient.get('/api/contacts/communication-logs');
  },
};