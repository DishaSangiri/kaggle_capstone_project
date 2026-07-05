import React, { useState } from 'react';
import { useReality } from '../context/RealityContext';
import PlanetContainer from './PlanetContainer';
import AgentActivityPanel from './AgentActivityPanel';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Compass, BarChart3, Brain, PlusCircle, CheckCircle, 
  HelpCircle, Sparkles, TrendingUp, ShieldAlert, BookOpen
} from 'lucide-react';

export const DashboardLayout: React.FC = () => {
  const { planetState, habits, logHabit, error } = useReality();
  const [activeTab, setActiveTab] = useState<'overview' | 'simulation' | 'agents'>('overview');
  const [habitCategory, setHabitCategory] = useState<string>('focus');
  const [habitActivity, setHabitActivity] = useState<string>('');
  const [habitValue, setHabitValue] = useState<number>(5.0);
  const [successMsg, setSuccessMsg] = useState<string>('');

  // Status check for WS connection
  const wsConnected = true; // In a real environment, we'd pull from RealityContext state if required

  const handleLogHabit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!habitActivity) return;
    setSuccessMsg('');
    await logHabit(habitCategory, habitActivity, habitValue, { source: 'dashboard_ui' });
    setSuccessMsg(`Logged: "${habitActivity}" under ${habitCategory.toUpperCase()}! Simulation updated.`);
    setHabitActivity('');
    // Auto clear feedback message after 3 seconds
    setTimeout(() => setSuccessMsg(''), 3000);
  };

  // Convert projection json if present
  const projection = planetState?.simulation_projection ?? {};
  const projected30d = projection.projection_30d ?? {};
  const chaosEntropy = projection.chaos_entropy ?? 0.5;
  const reflection = projection.reflection ?? 'Reality is settling. Log your first actions to prompt the Oracle.';

  const equilibriumPercent = Math.round((planetState?.overall_equilibrium ?? 0.5) * 100);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-950 text-gray-100 font-sans">
      {/* Sidebar Navigation */}
      <aside className="w-full md:w-64 glass-panel border-r border-white/5 flex flex-col p-6 gap-6 justify-between shrink-0">
        <div className="flex flex-col gap-6">
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 bg-indigo-600/20 border border-indigo-500/30 rounded-xl">
              <Sparkles className="text-indigo-400 animate-pulse" size={22} />
            </div>
            <div>
              <h1 className="text-md font-bold tracking-wider uppercase text-white">ECHO</h1>
              <p className="text-[10px] text-gray-400 tracking-widest font-mono">RealityVerse</p>
            </div>
          </div>

          <nav className="flex flex-col gap-1">
            <button
              onClick={() => setActiveTab('overview')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activeTab === 'overview' 
                  ? 'bg-indigo-600/15 border-l-2 border-indigo-500 text-indigo-200' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-gray-200'
              }`}
            >
              <Compass size={18} />
              Overview Planet
            </button>
            <button
              onClick={() => setActiveTab('simulation')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activeTab === 'simulation' 
                  ? 'bg-indigo-600/15 border-l-2 border-indigo-500 text-indigo-200' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-gray-200'
              }`}
            >
              <BarChart3 size={18} />
              Simulations
            </button>
            <button
              onClick={() => setActiveTab('agents')}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activeTab === 'agents' 
                  ? 'bg-indigo-600/15 border-l-2 border-indigo-500 text-indigo-200' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-gray-200'
              }`}
            >
              <Brain size={18} />
              AI Governor Logs
            </button>
          </nav>
        </div>

        {/* Connection status card */}
        <div className="p-3 bg-white/5 border border-white/5 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-2">
            {wsConnected ? (
              <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse" />
            ) : (
              <span className="w-2.5 h-2.5 bg-red-500 rounded-full" />
            )}
            <span className="text-[10px] text-gray-400 font-medium">WS Channel Logs</span>
          </div>
          <span className="text-[9px] text-gray-500 uppercase font-mono">ONLINE</span>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col p-4 md:p-8 gap-6 overflow-y-auto max-w-7xl mx-auto w-full">
        {/* Top Header Card */}
        <header className="glass-panel p-6 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Ecosystem Control Dashboard
            </h2>
            <p className="text-xs text-gray-400">Manage habit adjustments and watch the planet react</p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Equilibrium Meter */}
            <div className="text-right">
              <span className="text-[10px] text-gray-400 uppercase tracking-widest block font-mono">Global Equilibrium</span>
              <span className="text-2xl font-extrabold text-indigo-400 font-mono">{equilibriumPercent}%</span>
            </div>
            <div className="w-12 h-12 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 flex items-center justify-center font-bold text-xs text-gray-200 font-mono animate-spin-slow">
              EQ
            </div>
          </div>
        </header>

        {/* Global Error Banner */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-xl text-sm flex items-center gap-2">
            <ShieldAlert size={16} /> {error}
          </div>
        )}

        {/* Grid Panels */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* LEFT COLUMN: Main tab display */}
          <div className="lg:col-span-8 flex flex-col gap-6">
            <AnimatePresence mode="wait">
              {activeTab === 'overview' && (
                <motion.div
                  key="overview-tab"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ duration: 0.25 }}
                  className="flex flex-col gap-6"
                >
                  {/* Planet Canvas Canvas */}
                    <div className="glass-panel rounded-2xl overflow-hidden border border-white/5 shadow-2xl relative min-h-[650px] flex items-center justify-center">
                    <div className="absolute top-4 right-4 z-10 glass-panel px-3 py-1.5 rounded-lg text-[10px] text-gray-300 font-semibold flex items-center gap-1.5">
                      <Sparkles size={12} className="text-yellow-400" /> WebGL Canvas Active
                    </div>
                    <PlanetContainer />
                  </div>

                  {/* Biome meters */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { name: 'Forest Biome', val: planetState?.forest_health ?? 0.5, color: 'from-emerald-500 to-teal-500', glow: 'border-glow-forest' },
                      { name: 'Ocean Currents', val: planetState?.ocean_health ?? 0.5, color: 'from-sky-500 to-blue-500', glow: 'border-glow-ocean' },
                      { name: 'Asset Crystals', val: planetState?.finance_health ?? 0.5, color: 'from-amber-500 to-orange-500', glow: 'border-glow-finance' },
                      { name: 'Citadel Shields', val: planetState?.focus_health ?? 0.5, color: 'from-indigo-500 to-purple-500', glow: 'border-glow-focus' },
                    ].map((biome) => (
                      <div key={biome.name} className={`glass-panel p-4 rounded-xl flex flex-col gap-2 transition-all hover:scale-[1.02] ${biome.glow}`}>
                        <span className="text-xs text-gray-400 font-semibold">{biome.name}</span>
                        <div className="flex items-baseline justify-between">
                          <span className="text-xl font-bold text-white font-mono">{Math.round(biome.val * 100)}%</span>
                          <span className="text-[10px] text-gray-500">Stability</span>
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                          <div 
                            className={`h-full bg-gradient-to-r ${biome.color} transition-all duration-500`}
                            style={{ width: `${biome.val * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}

              {activeTab === 'simulation' && (
                <motion.div
                  key="sim-tab"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ duration: 0.25 }}
                  className="flex flex-col gap-6"
                >
                  {/* Oracle Reflection Card */}
                  <div className="glass-panel p-6 rounded-2xl flex flex-col gap-3 border-l-4 border-teal-500">
                    <h3 className="text-md font-bold text-teal-400 flex items-center gap-2">
                      <BookOpen size={18} /> Reality Reflection Oracle
                    </h3>
                    <p className="text-sm italic text-gray-200 font-serif leading-relaxed">
                      "{reflection}"
                    </p>
                    <p className="text-[10px] text-gray-500 font-mono mt-1">Generated by: Reflection Agent (Gemini-2.5-Flash)</p>
                  </div>

                  {/* Future Forecast & Chaos Metrics */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* 30-Day Forecast */}
                    <div className="glass-panel p-6 rounded-2xl flex flex-col gap-4">
                      <div>
                        <h3 className="text-sm uppercase tracking-wider text-indigo-400 font-bold flex items-center gap-2">
                          <TrendingUp size={16} /> 30-Day Forecast Outlook
                        </h3>
                        <p className="text-xs text-gray-400">Biome predictions under current habits</p>
                      </div>
                      
                      <div className="flex flex-col gap-3.5">
                        {Object.entries(projected30d).map(([biome, value]: [string, any]) => (
                          <div key={biome} className="flex flex-col gap-1">
                            <div className="flex justify-between text-xs">
                              <span className="capitalize text-gray-300">{biome} Health</span>
                              <span className="font-mono text-gray-400">{Math.round(value * 100)}%</span>
                            </div>
                            <div className="w-full bg-white/5 rounded-full h-1">
                              <div 
                                className="h-full bg-indigo-500 rounded-full" 
                                style={{ width: `${value * 100}%` }}
                              />
                            </div>
                          </div>
                        ))}
                        {Object.keys(projected30d).length === 0 && (
                          <p className="text-xs text-gray-500 italic py-4">Waiting for first coordination cycle...</p>
                        )}
                      </div>
                    </div>

                    {/* Chaos Butterfly Indicator */}
                    <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between gap-4">
                      <div>
                        <h3 className="text-sm uppercase tracking-wider text-yellow-500 font-bold flex items-center gap-2">
                          <HelpCircle size={16} /> Butterfly Chaos Status
                        </h3>
                        <p className="text-xs text-gray-400">Simulating cascading system entropy</p>
                      </div>

                      <div className="flex flex-col items-center justify-center p-4 bg-white/5 rounded-xl text-center gap-2">
                        <div className="text-3xl font-extrabold font-mono text-yellow-400">
                          {chaosEntropy.toFixed(2)}
                        </div>
                        <span className="text-xs text-gray-300 font-medium">Entropy Rating</span>
                        <p className="text-[10px] text-gray-500 leading-relaxed">
                          {chaosEntropy > 0.6 
                            ? 'Entropy high. A small decrease in wellness habits could trigger a biome collapse.'
                            : 'Entropy is within safety bounds. Ecosystem holds high resilience.'
                          }
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {activeTab === 'agents' && (
                <motion.div
                  key="agents-tab"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ duration: 0.25 }}
                >
                  <AgentActivityPanel />
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* RIGHT COLUMN: Habits Logger Drawer & Recent Actions */}
          <div className="lg:col-span-4 flex flex-col gap-6">
            {/* Habit Form */}
            <div className="glass-panel p-6 rounded-2xl flex flex-col gap-4">
              <h3 className="text-sm uppercase tracking-wider text-indigo-400 font-bold flex items-center gap-2">
                <PlusCircle size={16} /> Log Habit Activity
              </h3>
              
              <form onSubmit={handleLogHabit} className="flex flex-col gap-4">
                {/* Category */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400">Activity Type</label>
                  <select 
                    value={habitCategory} 
                    onChange={(e) => setHabitCategory(e.target.value)}
                    className="w-full bg-white/5 border border-white/5 p-2 rounded-lg text-sm focus:outline-none focus:border-indigo-500/50"
                  >
                    <option value="focus" className="bg-gray-900">Focus Hours (Citadel)</option>
                    <option value="wellness" className="bg-gray-900">Mental Wellness (Ocean)</option>
                    <option value="finance" className="bg-gray-900">Budget Limit (Crystals)</option>
                    <option value="health" className="bg-gray-900">Physical Health (Forest)</option>
                  </select>
                </div>

                {/* Activity Description */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-gray-400">What did you do?</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Coded for 3 hours, Drank water, Bought lunch"
                    value={habitActivity}
                    onChange={(e) => setHabitActivity(e.target.value)}
                    className="w-full bg-white/5 border border-white/5 p-2.5 rounded-lg text-sm placeholder:text-gray-600 focus:outline-none focus:border-indigo-500/50"
                  />
                </div>

                {/* Score slider */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">Impact Value</span>
                    <span className="font-semibold text-indigo-300">{habitValue} points</span>
                  </div>
                  <input 
                    type="range" 
                    min="1" 
                    max="10" 
                    step="0.5" 
                    value={habitValue} 
                    onChange={(e) => setHabitValue(parseFloat(e.target.value))}
                    className="w-full accent-indigo-500 bg-white/10 rounded-lg appearance-none h-1 cursor-pointer"
                  />
                </div>

                {/* Log button */}
                <button
                  type="submit"
                  className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 rounded-lg text-sm transition-colors cursor-pointer mt-2"
                >
                  Log & Evolve
                </button>
              </form>

              {/* Feedback Alert */}
              <AnimatePresence>
                {successMsg && (
                  <motion.div 
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3.5 py-2 rounded-lg text-xs flex items-center gap-2 mt-2 leading-relaxed"
                  >
                    <CheckCircle size={14} className="shrink-0" />
                    <span>{successMsg}</span>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Recent Habit History */}
            <div className="glass-panel p-6 rounded-2xl flex flex-col gap-4">
              <div>
                <h3 className="text-sm uppercase tracking-wider text-gray-400 font-bold">
                  Recent Activities
                </h3>
                <p className="text-[10px] text-gray-500">Latest user logged changes</p>
              </div>

              <div className="flex flex-col gap-2.5 overflow-y-auto max-h-[220px]">
                {habits.slice(0, 8).map((h) => (
                  <div key={h.id} className="p-3 bg-white/5 border border-white/5 rounded-xl flex justify-between items-center gap-2">
                    <div>
                      <h4 className="text-xs font-semibold text-gray-200">{h.activity}</h4>
                      <span className="text-[9px] uppercase tracking-wider text-indigo-400 font-bold block mt-0.5">{h.category}</span>
                    </div>
                    <span className="text-xs font-mono font-bold text-indigo-300">+{h.value}</span>
                  </div>
                ))}
                {habits.length === 0 && (
                  <p className="text-xs text-gray-500 italic py-4 text-center">No habits logged yet today.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
