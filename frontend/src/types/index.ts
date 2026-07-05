export interface UserHabit {
  id?: number;
  category: string;
  activity: string;
  value: number;
  raw_metadata?: Record<string, any>;
  timestamp?: string;
}

export interface PlanetState {
  id: number;
  forest_health: number;
  ocean_health: number;
  finance_health: number;
  focus_health: number;
  overall_equilibrium: number;
  last_updated: string;
  agent_version: string;
  simulation_projection: {
    projection_30d?: {
      forest?: number;
      ocean?: number;
      finance?: number;
      focus?: number;
    };
    chaos_entropy?: number;
    reflection?: string;
    patterns?: {
      streaks?: string[];
      burnout_risk?: boolean;
      habit_consistency?: string;
    };
  };
}

export interface AgentLog {
  id: number;
  agent_name: string;
  cycle_id: string;
  action: string;
  status: 'RUNNING' | 'SUCCESS' | 'WARNING' | 'FAILED';
  rationale: string;
  impact_summary: Record<string, any>;
  timestamp: string;
}
