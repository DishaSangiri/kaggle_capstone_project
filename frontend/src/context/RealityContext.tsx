import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { PlanetState, AgentLog, UserHabit } from '../types';
import { api } from '../services/api';

interface RealityContextType {
  planetState: PlanetState | null;
  agentLogs: AgentLog[];
  habits: UserHabit[];
  isLoading: boolean;
  error: string | null;
  logHabit: (category: string, activity: string, value: number, meta?: Record<string, any>) => Promise<void>;
  triggerCycle: () => Promise<void>;
  refreshAll: () => Promise<void>;
}

const RealityContext = createContext<RealityContextType | undefined>(undefined);

export const RealityProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [planetState, setPlanetState] = useState<PlanetState | null>(null);
  const [agentLogs, setAgentLogs] = useState<AgentLog[]>([]);
  const [habits, setHabits] = useState<UserHabit[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refreshAll = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [state, logs, list] = await Promise.all([
        api.fetchPlanetState(),
        api.fetchAgentLogs(),
        api.fetchHabits(),
      ]);
      setPlanetState(state);
      setAgentLogs(logs);
      setHabits(list);
    } catch (err: any) {
      setError(err.message || 'Failed to refresh RealityVerse metrics.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const triggerCycle = useCallback(async () => {
    try {
      setIsLoading(true);
      const result = await api.triggerCoordinationCycle();
      if (result.success) {
        setPlanetState(result.new_state);
        // Refresh the log history list to incorporate final states
        const freshLogs = await api.fetchAgentLogs();
        setAgentLogs(freshLogs);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to run agent coordination cycle.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logHabit = useCallback(async (category: string, activity: string, value: number, meta?: Record<string, any>) => {
    try {
      await api.logHabit({ category, activity, value, raw_metadata: meta });
      // Refresh current logged list
      const freshHabits = await api.fetchHabits();
      setHabits(freshHabits);
      // Automatically trigger an orchestration cycle to evolve the planet in response to the user's action
      await triggerCycle();
    } catch (err: any) {
      setError(err.message || 'Failed to log habit activity.');
    }
  }, [triggerCycle]);

  // Establish live WebSockets subscription for real-time agent log streaming
  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: any = null;

    const connectWS = () => {
      ws = new WebSocket('ws://localhost:8000/ws/logs');

      ws.onopen = () => {
        console.log('RealityVerse: Live websocket stream connected.');
      };

      ws.onmessage = (event) => {
        try {
          const freshLog: AgentLog = JSON.parse(event.data);
          // Stream updates onto top of execution stack
          setAgentLogs((prevLogs) => {
            // Avoid duplicate log insertions
            if (prevLogs.some(log => log.id === freshLog.id || (log.cycle_id === freshLog.cycle_id && log.agent_name === freshLog.agent_name && log.action === freshLog.action))) {
              return prevLogs;
            }
            return [freshLog, ...prevLogs];
          });
        } catch (err) {
          console.error('RealityVerse: Error parsing websocket message:', err);
        }
      };

      ws.onclose = () => {
        console.log('RealityVerse: WebSocket disconnected. Attempting reconnect...');
        reconnectTimeout = setTimeout(connectWS, 3000);
      };

      ws.onerror = (err) => {
        console.error('RealityVerse: WebSocket connection error:', err);
        ws?.close();
      };
    };

    connectWS();
    refreshAll();

    return () => {
      if (ws) {
        ws.onclose = null; // Prevent reconnect loops on unmount
        ws.close();
      }
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
    };
  }, [refreshAll]);

  return (
    <RealityContext.Provider
      value={{
        planetState,
        agentLogs,
        habits,
        isLoading,
        error,
        logHabit,
        triggerCycle,
        refreshAll,
      }}
    >
      {children}
    </RealityContext.Provider>
  );
};

export const useReality = () => {
  const context = useContext(RealityContext);
  if (context === undefined) {
    throw new Error('useReality must be used within a RealityProvider');
  }
  return context;
};
