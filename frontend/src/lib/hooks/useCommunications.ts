import { useState, useEffect, useCallback } from 'react';
import { contactsApi } from '../api/contacts';
import { ApiError } from '../api/client';

interface CommunicationLog {
  id: number;
  contact: string;
  contact_id: number;
  subject?: string;
  message?: string;
  body?: string;
  sent_at: string;
}

interface CommunicationLogs {
  emails: CommunicationLog[];
  sms: CommunicationLog[];
}

export function useCommunications() {
  const [logs, setLogs] = useState<CommunicationLogs>({ emails: [], sms: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await contactsApi.getCommunicationLogs();
      setLogs(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to fetch communication logs');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  return { logs, loading, error, refetch: fetchLogs };
}

export function useContactEmails(contactId: number) {
  const [emails, setEmails] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEmails() {
      if (!contactId) return;
      setLoading(true);
      setError(null);
      try {
        const data = await contactsApi.getContactEmails(contactId);
        setEmails(data);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError('Failed to fetch emails');
        }
      } finally {
        setLoading(false);
      }
    }

    fetchEmails();
  }, [contactId]);

  return { emails, loading, error };
}