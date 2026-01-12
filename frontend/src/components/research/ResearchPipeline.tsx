'use client';

import React from 'react';
import { ApexContact } from '@/lib/types/apex';
import { SuperResearcher } from '@/lib/types/super-researcher';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

interface ResearchPipelineProps {
  stagedLeads: {
    apex: ApexContact[];
    super: SuperResearcher[];
  };
  activeLeads: {
    apex: ApexContact[];
    super: SuperResearcher[];
  };
  onPromote?: (type: 'apex' | 'super', id: number) => void;
  onContactClick?: (type: 'apex' | 'super', id: number) => void;
}

export function ResearchPipeline({
  stagedLeads,
  activeLeads,
  onPromote,
  onContactClick,
}: ResearchPipelineProps) {
  const totalStaged = stagedLeads.apex.length + stagedLeads.super.length;
  const totalActive = activeLeads.apex.length + activeLeads.super.length;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Staged Leads Column */}
      <Card title={`Staged Leads (${totalStaged})`}>
        <div className="space-y-3">
          {stagedLeads.apex.map((contact) => (
            <div
              key={contact.id}
              className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div
                  className="flex-1 cursor-pointer"
                  onClick={() => onContactClick?.('apex', contact.id)}
                >
                  <h4 className="font-medium text-gray-900">{contact.full_name}</h4>
                  <p className="text-sm text-gray-600">{contact.company}</p>
                  <p className="text-sm text-gray-600">{contact.email}</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="blue">Apex</Badge>
                    <Badge>{contact.lead_class}</Badge>
                  </div>
                </div>
                {onPromote && (
                  <Button
                    size="sm"
                    variant="success"
                    onClick={() => onPromote('apex', contact.id)}
                  >
                    Promote
                  </Button>
                )}
              </div>
            </div>
          ))}

          {stagedLeads.super.map((contact) => (
            <div
              key={contact.id}
              className="p-4 border border-gray-200 rounded-lg hover:border-purple-500 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div
                  className="flex-1 cursor-pointer"
                  onClick={() => onContactClick?.('super', contact.id)}
                >
                  <h4 className="font-medium text-gray-900">{contact.full_name}</h4>
                  <p className="text-sm text-gray-600">{contact.company}</p>
                  <p className="text-sm text-gray-600">{contact.email}</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="purple">Super</Badge>
                    <Badge>{contact.lead_class}</Badge>
                  </div>
                </div>
                {onPromote && (
                  <Button
                    size="sm"
                    variant="success"
                    onClick={() => onPromote('super', contact.id)}
                  >
                    Promote
                  </Button>
                )}
              </div>
            </div>
          ))}

          {totalStaged === 0 && (
            <div className="text-center py-8 text-gray-500">
              No staged leads found.
            </div>
          )}
        </div>
      </Card>

      {/* Active Leads Column */}
      <Card title={`Active Leads (${totalActive})`}>
        <div className="space-y-3">
          {activeLeads.apex.map((contact) => (
            <div
              key={contact.id}
              className="p-4 border border-green-200 rounded-lg"
            >
              <div
                className="cursor-pointer"
                onClick={() => onContactClick?.('apex', contact.id)}
              >
                <h4 className="font-medium text-gray-900">{contact.full_name}</h4>
                <p className="text-sm text-gray-600">{contact.company}</p>
                <p className="text-sm text-gray-600">{contact.email}</p>
                <div className="flex items-center space-x-2 mt-2">
                  <Badge variant="blue">Apex</Badge>
                  <Badge variant="green">Active</Badge>
                  <Badge>{contact.lead_class}</Badge>
                </div>
              </div>
            </div>
          ))}

          {activeLeads.super.map((contact) => (
            <div
              key={contact.id}
              className="p-4 border border-green-200 rounded-lg"
            >
              <div
                className="cursor-pointer"
                onClick={() => onContactClick?.('super', contact.id)}
              >
                <h4 className="font-medium text-gray-900">{contact.full_name}</h4>
                <p className="text-sm text-gray-600">{contact.company}</p>
                <p className="text-sm text-gray-600">{contact.email}</p>
                <div className="flex items-center space-x-2 mt-2">
                  <Badge variant="purple">Super</Badge>
                  <Badge variant="green">Active</Badge>
                  <Badge>{contact.lead_class}</Badge>
                </div>
              </div>
            </div>
          ))}

          {totalActive === 0 && (
            <div className="text-center py-8 text-gray-500">
              No active leads found.
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}