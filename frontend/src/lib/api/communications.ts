import { apiClient } from './client';
import { MoreInfoResponse } from "../types/moreinfo";


export const moreInfoApi = {
    // Get more info by ID
    getMoreInfoById: async (contact_id: number): Promise<MoreInfoResponse> => {
        const params: Record<string, string> = {};
        return apiClient.get<MoreInfoResponse>(`/api/contact/moreinfo/${contact_id}`, params);
    },
};
export interface EmailData {
  subject: string;
  message: string;
}

export interface SMSData {
  message: string;
}

export interface EditContactData {
  // Define the fields that can be edited for a contact
  Full_name?: string;
  company?: string;
  lead_class?: string;
  email?: string;
  phone_number?: string;
  address?: string;
  notes?: string;
}

export const communicationsApi = {
  sendEmail: async (contactId: number, data: EmailData): Promise<{ success: boolean; message: string }> => {
    return apiClient.post<{ success: boolean; message: string }>(`/api/communications/send-email/${contactId}`, data);
  },

  sendSMS: async (contactId: number, data: SMSData): Promise<{ success: boolean; message: string }> => {
    return apiClient.post<{ success: boolean; message: string }>(`/api/communications/send-sms/${contactId}`, data);
  },
};

export const edit = {
  editContact: async (contactId: number, data: EditContactData) => {
    return apiClient.put(`/api/contacts/${contactId}`, data);
  }
}