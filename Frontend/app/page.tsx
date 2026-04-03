'use client';

import { useState, useCallback, useRef } from 'react';
import { PatientForm, VerifyPatient, ConnectingScreen, PatientData } from '@/frontend/components/onboarding';
import Dashboard from '@/frontend/components/dashboard/dashboard-main';
import SessionSummaryDialog from '@/frontend/components/dashboard/session-summary-dialog';
import { useEEG } from '@/frontend/hooks/use-eeg';
import { createPatient, startSession, endSession } from '@/lib/api';

type FlowStep = 'patient-form' | 'verify' | 'connecting' | 'dashboard';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<FlowStep>('patient-form');
  const [patientData, setPatientData] = useState<PatientData | null>(null);
  const [showSummary, setShowSummary] = useState(false);
  const [sessionDuration, setSessionDuration] = useState(0);
  const [endedSessionId, setEndedSessionId] = useState<string | null>(null);
  const sessionIdRef = useRef<string | null>(null);
  const sessionStartTimeRef = useRef<number>(0);
  const { disconnect, stopStreaming } = useEEG();
  const handlePatientFormSubmit = async (data: PatientData) => {
    setPatientData(data);
    try {
      await createPatient(data);
    } catch (error) {
      console.error('Failed to save patient:', error);
    }
    
    setCurrentStep('verify');
  };
  const handleEdit = () => {
    setCurrentStep('patient-form');
  };
  const handleConfirm = () => {
    setCurrentStep('connecting');
  };
  const handleConnected = useCallback(async () => {
    if (patientData) {
      try {
        const session = await startSession(patientData.patientId);
        sessionIdRef.current = session.sessionId;
        sessionStartTimeRef.current = Date.now();
        console.log('Session started:', session.sessionId);
      } catch (error) {
        console.error('Failed to start session:', error);
      }
    }
    setCurrentStep('dashboard');
  }, [patientData]);

  const handleEndSession = useCallback(async () => {
    if (patientData && sessionIdRef.current) {
      try {
        stopStreaming();
        await endSession(patientData.patientId, sessionIdRef.current);
        const duration = Math.floor((Date.now() - sessionStartTimeRef.current) / 1000);
        setSessionDuration(duration);
        setEndedSessionId(sessionIdRef.current);
        
        setShowSummary(true);
      } catch (error) {
        console.error('Failed to end session:', error);
        setShowSummary(true);
      }
    }
    
    await disconnect();
  }, [patientData, disconnect, stopStreaming]);
  const handleSummaryClose = () => {
    setShowSummary(false);
    setEndedSessionId(null);
    sessionIdRef.current = null;
    setPatientData(null);
    setCurrentStep('patient-form');
  };

  return (
    <>
      {currentStep === 'patient-form' && (
        <PatientForm 
          onSubmit={handlePatientFormSubmit} 
          initialData={patientData || undefined}
        />
      )}
      
      {currentStep === 'verify' && patientData && (
        <VerifyPatient
          patientData={patientData}
          onConfirm={handleConfirm}
          onEdit={handleEdit}
        />
      )}
      
      {currentStep === 'connecting' && patientData && (
        <ConnectingScreen
          patientData={patientData}
          onConnected={handleConnected}
        />
      )}
      
      {currentStep === 'dashboard' && patientData && (
        <Dashboard
          patientData={patientData}
          onEndSession={handleEndSession}
        />
      )}
      {patientData && endedSessionId && (
        <SessionSummaryDialog
          open={showSummary}
          onClose={handleSummaryClose}
          patientData={patientData}
          sessionId={endedSessionId}
          duration={sessionDuration}
        />
      )}
    </>
  );
}
