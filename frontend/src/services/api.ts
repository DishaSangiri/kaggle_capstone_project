import type { UserHabit, PlanetState, AgentLog } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  async fetchPlanetState(): Promise<PlanetState> {
    const response = await fetch(`${API_BASE_URL}/planet/state`);
    if (!response.ok) throw new Error('Failed to fetch planet state');
    return response.json();
  },

  async fetchAgentLogs(): Promise<AgentLog[]> {
    const response = await fetch(`${API_BASE_URL}/agents/logs`);
    if (!response.ok) throw new Error('Failed to fetch agent logs');
    return response.json();
  },

  async fetchHabits(): Promise<UserHabit[]> {
    const response = await fetch(`${API_BASE_URL}/habits`);
    if (!response.ok) throw new Error('Failed to fetch habits');
    return response.json();
  },

  async logHabit(habit: UserHabit): Promise<UserHabit> {
    const response = await fetch(`${API_BASE_URL}/habits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(habit),
    });
    if (!response.ok) throw new Error('Failed to log habit');
    return response.json();
  },

  async triggerCoordinationCycle(): Promise<{
    success: boolean;
    cycle_id: string;
    new_state: PlanetState;
    logs: AgentLog[];
  }> {
    const response = await fetch(`${API_BASE_URL}/agents/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to run agent coordination cycle');
    return response.json();
  },
};
export default api;
