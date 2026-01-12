'use client';

import React from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { ResearchPipeline } from '@/components/research/ResearchPipeline';
import { useResearchPipeline } from '@/lib/hooks/useResearch';
import { useRouter } from 'next/navigation';
import { Loader } from '@/components/ui/Loader';

export default function ResearchPage() {
  const { stagedLeads, activeLeads, loading, error, promoteApexContact } = useResearchPipeline();
  const router = useRouter();

  const handleContactClick = (type: 'apex' | 'super', id: number) => {
    if (type === 'apex') {
      router.push(`/apex/${id}`);
    } else {
      router.push(`/super-researcher/${id}`);
    }
  };

  const handlePromote = async (type: 'apex' | 'super', id: number) => {
    if (type === 'apex') {
      try {
        await promoteApexContact(id);
      } catch (error) {
        console.error('Failed to promote contact:', error);
      }
    }
    // Add super researcher promotion logic when needed
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center h-96">
          <Loader size="lg" />
        </div>
      </MainLayout>
    );
  }

  if (error) {
    return (
      <MainLayout>
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Research Pipeline</h1>
          <p className="text-gray-600 mt-2">
            Manage and convert research leads through the pipeline from staged to active.
          </p>
        </div>

        <ResearchPipeline
          stagedLeads={stagedLeads}
          activeLeads={activeLeads}
          onContactClick={handleContactClick}
          onPromote={handlePromote}
        />
      </div>
    </MainLayout>
  );
}