'use client';

import React, { useState } from 'react';
import { ContactFormData, LeadClassification } from '@/lib/types/contact';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { Select } from '../ui/Select';
import { Button } from '../ui/Button';

interface ContactFormProps {
  initialData?: Partial<ContactFormData>;
  onSubmit: (data: ContactFormData) => Promise<void>;
  onCancel?: () => void;
  submitLabel?: string;
}

const leadClassOptions = [
  { value: 'New', label: 'New' },
  { value: 'Contacted', label: 'Contacted' },
  { value: 'Growing Interest', label: 'Growing Interest' },
  { value: 'Leading', label: 'Leading' },
  { value: 'Converted', label: 'Converted' },
  { value: 'Cold', label: 'Cold' },
  { value: 'Dying', label: 'Dying' },
];

export function ContactForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = 'Submit',
}: ContactFormProps) {
  const [formData, setFormData] = useState<ContactFormData>({
    Full_name: initialData?.Full_name || '',
    email: initialData?.email || '',
    phone_number: initialData?.phone_number || '',
    company: initialData?.company || '',
    lead_class: initialData?.lead_class || 'New',
    notes: initialData?.notes || '',
    address: initialData?.address || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.Full_name.trim()) {
      newErrors.Full_name = 'Name is required';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof ContactFormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
    if (errors[field]) {
      setErrors({ ...errors, [field]: '' });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Full Name"
        value={formData.Full_name}
        onChange={handleChange('Full_name')}
        error={errors.Full_name}
        required
      />

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleChange('email')}
        error={errors.email}
        required
      />

      <Input
        label="Phone Number"
        type="tel"
        value={formData.phone_number}
        onChange={handleChange('phone_number')}
      />

      <Input
        label="Company"
        value={formData.company}
        onChange={handleChange('company')}
      />

      <Select
        label="Lead Classification"
        options={leadClassOptions}
        value={formData.lead_class}
        onChange={handleChange('lead_class')}
      />

      <Input
        label="Address"
        value={formData.address}
        onChange={handleChange('address')}
      />

      <Textarea
        label="Notes"
        value={formData.notes}
        onChange={handleChange('notes')}
        rows={3}
      />

      <div className="flex space-x-3 pt-4">
        <Button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : submitLabel}
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}