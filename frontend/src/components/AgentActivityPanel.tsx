import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReality } from '../context/RealityContext';
import type { AgentLog } from '../types';
import { 
  Eye, Zap, RefreshCw, Trees, Droplet, 
  Coins, Shield, Compass, BrainCircuit, Activity,
  Play, CheckCircle2, AlertTriangle, XCircle, Clock
} from 'lucide-react';

const getAgentIcon = (name: string) => {
  switch (name) {
    case 'Observer': return <Eye size={18} className="text-sky-400" />;
    case 'Pattern': return <Activity size={18} className="text-fuchsia-400" />;
    case 'Butterfly': return <Zap size={18} className="text-yellow-400" />;
    case 'Forest Governor': return <Trees size={18} className="text-emerald-400" />;
    case 'Ocean Governor': return <Droplet size={18} className="text-cyan-400" />;
    case 'Finance Governor': return <Coins size={18} className="text-amber-400" />;
    case 'Focus Governor': return <Shield size={18} className="text-indigo-400" />;
    case 'Future Simulation': return <Compass size={18} className="text-pink-400" />;
    case 'Reflection': return <BrainCircuit size={18} className="text-teal-400" />;
    case 'Reality Coordinator': return <RefreshCw size={18} className="text-rose-400" />;
    default: return <Activity size={18} className="text-gray-400" />;
  }
};

const getStatusBadge = (status: AgentLog['status']) => {
  switch (status) {
    case 'SUCCESS':
      return (
        <span className="flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <CheckCircle2 size={12} /> Success
        </span>
      );
    case 'RUNNING':
      return (
        <span className="flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 animate-pulse">
          <Clock size={12} className="animate-spin" /> Running
        </span>
      );
    case 'WARNING':
      return (
        <span className="flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
          <AlertTriangle size={12} /> Warning
        </span>
      );
    case 'FAILED':
      return (
        <span className="flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">
          <XCircle size={12} /> Failed
        </span>
      );
  }
};

export const AgentActivityPanel: React.FC = () => {
  const { agentLogs, triggerCycle, isLoading } = useReality();
  const [filterAgent, setFilterAgent] = useState<string>('ALL');

  const filteredLogs = filterAgent === 'ALL' 
    ? agentLogs 
    : agentLogs.filter(log => log.agent_name === filterAgent);

  const uniqueAgents = Array.from(new Set(agentLogs.map(log => log.agent_name)));

  return (
    <div className="flex flex-col h-full gap-4">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 glass-panel rounded-xl">
        <div>
          <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2">
            <BrainCircuit className="text-indigo-400" /> Agent Activity Panel
          </h2>
          <p className="text-xs text-gray-400">Monitor multi-agent execution cycles in real time</p>
        </div>
        
        <button
          onClick={triggerCycle}
          disabled={isLoading}
          className="flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-800 disabled:text-gray-500 rounded-lg cursor-pointer transition-colors shadow-lg shadow-indigo-600/15"
        >
          <Play size={14} className={isLoading ? 'animate-spin' : ''} />
          {isLoading ? 'Coordinating...' : 'Trigger Cycle'}
        </button>
      </div>

      {/* Filter Options */}
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-thin">
        <button
          onClick={() => setFilterAgent('ALL')}
          className={`px-3 py-1 rounded-lg text-xs font-medium border transition-colors cursor-pointer whitespace-nowrap ${
            filterAgent === 'ALL' 
              ? 'bg-indigo-600/20 border-indigo-500/40 text-indigo-300' 
              : 'border-white/5 text-gray-400 hover:border-white/10'
          }`}
        >
          All Activities
        </button>
        {uniqueAgents.map(agent => (
          <button
            key={agent}
            onClick={() => setFilterAgent(agent)}
            className={`px-3 py-1 rounded-lg text-xs font-medium border transition-colors cursor-pointer whitespace-nowrap ${
              filterAgent === agent 
                ? 'bg-indigo-600/20 border-indigo-500/40 text-indigo-300' 
                : 'border-white/5 text-gray-400 hover:border-white/10'
            }`}
          >
            {agent}
          </button>
        ))}
      </div>

      {/* Real-time Log Stream */}
      <div className="flex-1 overflow-y-auto max-h-[500px] pr-1 flex flex-col gap-3">
        <AnimatePresence initial={false}>
          {filteredLogs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 glass-panel rounded-xl text-gray-500">
              <Compass size={32} className="animate-spin mb-2 text-gray-600" />
              <p className="text-sm">No agent activity logged yet.</p>
              <p className="text-xs text-gray-600 mt-1">Submit habits or click Trigger Cycle to begin.</p>
            </div>
          ) : (
            filteredLogs.slice(0, 30).map((log) => (
              <motion.div
                key={`${log.cycle_id}-${log.agent_name}-${log.action}`}
                initial={{ opacity: 0, y: -20, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, x: -100 }}
                transition={{ duration: 0.3 }}
                className="glass-panel p-4 rounded-xl flex flex-col gap-2 hover:border-white/15 transition-all group"
              >
                {/* Log Header */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="p-2 bg-white/5 rounded-lg group-hover:bg-white/10 transition-colors">
                      {getAgentIcon(log.agent_name)}
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-200">{log.agent_name}</h4>
                      <p className="text-[10px] text-gray-500 font-mono">Action: {log.action}</p>
                    </div>
                  </div>
                  {getStatusBadge(log.status)}
                </div>

                {/* Log Rationale */}
                <p className="text-xs text-gray-300 leading-relaxed pl-11">
                  {log.rationale}
                </p>

                {/* Log Footer / Timestamp */}
                <div className="flex items-center justify-between text-[9px] text-gray-500 pl-11 pt-1 border-t border-white/5">
                  <span className="font-mono truncate max-w-[150px] md:max-w-none">Cycle: {log.cycle_id}</span>
                  <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AgentActivityPanel;
