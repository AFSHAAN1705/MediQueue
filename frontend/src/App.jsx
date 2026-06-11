import { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.defaults.color = '#94a3b8';
ChartJS.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';

const ALGORITHMS = ['FCFS', 'SJF', 'Round Robin', 'Priority', 'SRTF'];

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [userRole, setUserRole] = useState(localStorage.getItem('role') || null);
  const [usernameStr, setUsernameStr] = useState(localStorage.getItem('username') || null);
  
  // Login Form State
  const [loginUser, setLoginUser] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // App State
  const [patients, setPatients] = useState([]);
  const [gantt, setGantt] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [algorithm, setAlgorithm] = useState('Round Robin');
  
  // Form state
  const [name, setName] = useState('');
  const [treatmentTime, setTreatmentTime] = useState(5);
  const [emergencyLevel, setEmergencyLevel] = useState(1);
  const [simulationTime, setSimulationTime] = useState(0);

  // Polling for live queue updates
  useEffect(() => {
    if (!token) return; // Only poll if logged in

    const fetchSchedule = async () => {
      try {
        const res = await fetch(`http://localhost:5000/queue/schedule?algorithm=${algorithm}`);
        if(res.ok) {
          const data = await res.json();
          setPatients(data.processes || []);
          setGantt(data.gantt_chart || []);
        }
        
        const metricRes = await fetch(`http://localhost:5000/metrics?algorithm=${algorithm}`);
        if(metricRes.ok) {
           const metricData = await metricRes.json();
           setMetrics(metricData);
        }
      } catch (err) {
        console.error("Failed to fetch schedule", err);
      }
    };

    fetchSchedule();
    const interval = setInterval(() => {
      setSimulationTime(t => t + 1); // increment virtual clock
      fetchSchedule();
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, [algorithm, simulationTime, token]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setIsLoggingIn(true);
    try {
      const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginUser.trim(), password: loginPass.trim() })
      });
      const data = await res.json();
      
      if (res.ok) {
        setToken(data.token);
        setUserRole(data.role);
        setUsernameStr(data.username);
        localStorage.setItem('token', data.token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('username', data.username);
      } else {
        setLoginError(data.message || 'Login failed');
      }
    } catch (err) {
      setLoginError('Server connection failed. Is the Flask backend running?');
    }
    setIsLoggingIn(false);
  };

  const handleLogout = () => {
    setToken(null);
    setUserRole(null);
    setUsernameStr(null);
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!name) return;
    
    try {
      await fetch('http://localhost:5000/patient/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          arrival_time: simulationTime,
          treatment_time: parseInt(treatmentTime),
          emergency_level: parseInt(emergencyLevel)
        })
      });
      setName('');
      setTreatmentTime(5);
      setEmergencyLevel(1);
      setSimulationTime(t => t); 
    } catch (err) {
      console.error(err);
    }
  };

  const chartData = {
    labels: [algorithm],
    datasets: [
      {
        label: 'Avg Waiting Time (mins)',
        data: metrics ? [metrics.average_waiting_time] : [0],
        backgroundColor: 'rgba(34, 211, 238, 0.8)', // Cyan-400
        borderRadius: 6,
      },
      {
        label: 'Avg Turnaround Time (mins)',
        data: metrics ? [metrics.average_turnaround_time] : [0],
        backgroundColor: 'rgba(192, 38, 211, 0.8)', // Fuchsia-600
        borderRadius: 6,
      }
    ],
  };

  const getEmergencyBadge = (level) => {
    switch(level) {
      case 5: return <span className="bg-rose-500/20 text-rose-300 text-xs font-bold px-3 py-1 rounded-full border border-rose-500/50 shadow-[0_0_10px_rgba(244,63,94,0.3)]">Critical (5)</span>;
      case 4: return <span className="bg-orange-500/20 text-orange-300 text-xs font-bold px-3 py-1 rounded-full border border-orange-500/50">Urgent (4)</span>;
      case 3: return <span className="bg-amber-500/20 text-amber-300 text-xs font-bold px-3 py-1 rounded-full border border-amber-500/50">Moderate (3)</span>;
      default: return <span className="bg-emerald-500/20 text-emerald-300 text-xs font-bold px-3 py-1 rounded-full border border-emerald-500/50">Low ({level})</span>;
    }
  };

  const colors = [
    'from-cyan-400 to-blue-500',
    'from-fuchsia-400 to-purple-600',
    'from-emerald-400 to-teal-500',
    'from-orange-400 to-rose-500',
    'from-indigo-400 to-violet-500'
  ];

  // --------------------------------------------------------------------------------
  // LOGIN SCREEN
  // --------------------------------------------------------------------------------
  if (!token) {
    return (
      <div className="min-h-screen p-4 md:p-8 font-sans relative flex items-center justify-center">
        {/* Decorative Orbs */}
        <div className="absolute top-[10%] left-[20%] w-[30%] h-[50%] rounded-full bg-cyan-600/30 blur-[150px] pointer-events-none animate-pulse"></div>
        <div className="absolute bottom-[10%] right-[20%] w-[30%] h-[50%] rounded-full bg-fuchsia-600/30 blur-[150px] pointer-events-none"></div>
        
        <div className="glass-panel p-10 w-full max-w-md relative z-10 border border-white/20 shadow-[0_0_50px_rgba(34,211,238,0.15)]">
          <div className="text-center mb-8">
            <div className="mx-auto w-16 h-16 bg-gradient-to-tr from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(34,211,238,0.5)]">
               <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">MediQueue</h1>
            <p className="text-slate-400 mt-2 text-sm">Sign in to access the scheduling engine.</p>
          </div>

          {loginError && (
            <div className="bg-rose-500/10 border border-rose-500/50 text-rose-400 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
               <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
               {loginError}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block mb-2 text-sm font-medium text-slate-300">Username</label>
              <input 
                type="text" 
                value={loginUser} 
                onChange={e => setLoginUser(e.target.value)} 
                className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block w-full p-3.5 outline-none transition-colors" 
                placeholder="admin, doctor, or receptionist" 
                required 
              />
            </div>
            <div>
              <label className="block mb-2 text-sm font-medium text-slate-300">Password</label>
              <input 
                type="password" 
                value={loginPass} 
                onChange={e => setLoginPass(e.target.value)} 
                className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block w-full p-3.5 outline-none transition-colors" 
                placeholder="••••••••" 
                required 
              />
            </div>
            <button 
              type="submit" 
              disabled={isLoggingIn}
              className="w-full text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-bold rounded-xl text-sm px-5 py-3.5 text-center shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all transform hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed mt-4"
            >
              {isLoggingIn ? 'Authenticating...' : 'Secure Login'}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-white/10 text-center">
             <p className="text-xs text-slate-500 mb-2">Demo Credentials:</p>
             <div className="flex justify-center gap-4 text-xs font-mono text-slate-400">
                <span>admin / admin123</span>
                <span>doctor / doctor123</span>
             </div>
          </div>
        </div>
      </div>
    );
  }

  // --------------------------------------------------------------------------------
  // DASHBOARD
  // --------------------------------------------------------------------------------
  return (
    <div className="min-h-screen p-4 md:p-8 font-sans relative">
      {/* Decorative Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-cyan-600/20 blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-fuchsia-600/20 blur-[120px] pointer-events-none"></div>

      <div className="max-w-7xl mx-auto space-y-8 relative z-10">
        
        {/* Header */}
        <header className="glass-panel p-6 md:p-8 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
          <div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight glowing-text">MediQueue Engine</h1>
            <div className="flex items-center gap-3 mt-3">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
              <p className="text-slate-400 font-medium border-r border-slate-700 pr-4">Virtual Time: <span className="text-white">Minute {simulationTime}</span></p>
              <p className="text-cyan-400 font-medium pl-2">
                 <span className="text-slate-400">Logged in as:</span> {usernameStr} ({userRole})
              </p>
            </div>
          </div>
          <div className="flex flex-col md:flex-row gap-4 w-full lg:w-auto items-start md:items-end">
            <div className="flex flex-col gap-2 w-full md:w-auto">
              <label className="text-xs uppercase tracking-wider font-bold text-slate-400">Scheduling Core</label>
              <select 
                className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block p-3 w-full md:w-56 transition-all hover:bg-slate-800/50 outline-none"
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value)}
              >
                {ALGORITHMS.map(a => <option key={a} value={a}>{a}</option>)}
              </select>
            </div>
            <button onClick={handleLogout} className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-3 rounded-xl text-sm font-bold border border-slate-700 transition-colors">
               Log Out
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Registration Form */}
          <div className="glass-panel p-6 lg:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-cyan-500/10 rounded-lg">
                <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path></svg>
              </div>
              <h2 className="text-2xl font-bold text-white">Intake Form</h2>
            </div>
            
            <form onSubmit={handleRegister} className="space-y-5">
              <div>
                <label className="block mb-2 text-sm font-medium text-slate-300">Patient Name</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block w-full p-3 outline-none transition-colors" placeholder="John Doe" required />
              </div>
              <div>
                <label className="block mb-2 text-sm font-medium text-slate-300">Treatment Duration (mins)</label>
                <input type="number" min="1" value={treatmentTime} onChange={e => setTreatmentTime(e.target.value)} className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block w-full p-3 outline-none transition-colors" required />
              </div>
              <div>
                <label className="block mb-2 text-sm font-medium text-slate-300">Triage Level</label>
                <select value={emergencyLevel} onChange={e => setEmergencyLevel(e.target.value)} className="bg-slate-900/50 border border-slate-700 text-white text-sm rounded-xl focus:ring-cyan-500 focus:border-cyan-500 block w-full p-3 outline-none transition-colors">
                  <option value={1}>1 - Low Priority</option>
                  <option value={2}>2 - Standard</option>
                  <option value={3}>3 - Moderate</option>
                  <option value={4}>4 - Urgent</option>
                  <option value={5}>5 - Critical (Ambulance)</option>
                </select>
              </div>
              <button type="submit" className="w-full text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-bold rounded-xl text-sm px-5 py-3.5 text-center shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all transform hover:scale-[1.02] active:scale-95">Admit Patient</button>
            </form>
          </div>

          {/* Live Queue */}
          <div className="glass-panel p-6 lg:col-span-2 flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-3">
                 <div className="p-2 bg-fuchsia-500/10 rounded-lg">
                    <svg className="w-6 h-6 text-fuchsia-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
                 </div>
                 <h2 className="text-2xl font-bold text-white">Active Queue</h2>
              </div>
              <span className="bg-emerald-500/10 text-emerald-400 text-xs font-bold px-3 py-1.5 rounded-full border border-emerald-500/20 flex items-center gap-2">
                 <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                 Live Sync
              </span>
            </div>
            
            <div className="overflow-x-auto flex-grow rounded-xl border border-white/5 bg-slate-900/30">
              <table className="w-full text-sm text-left text-slate-300">
                <thead className="text-xs uppercase bg-slate-800/50 text-slate-400 border-b border-white/5">
                  <tr>
                    <th className="px-6 py-4 rounded-tl-xl">Patient</th>
                    <th className="px-6 py-4">Arrival</th>
                    <th className="px-6 py-4">Duration</th>
                    <th className="px-6 py-4">Triage</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4 rounded-tr-xl">Wait Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {patients.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-800/30 transition-colors">
                      <td className="px-6 py-4 font-medium text-white">{p.name} <span className="text-slate-500 text-xs ml-1">#{p.id}</span></td>
                      <td className="px-6 py-4 font-mono">{p.arrival_time}</td>
                      <td className="px-6 py-4 font-mono">{p.treatment_time}m</td>
                      <td className="px-6 py-4">{getEmergencyBadge(p.emergency_level)}</td>
                      <td className="px-6 py-4">
                         {p.waiting_time !== null ? <span className="text-cyan-400 font-bold drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]">Scheduled</span> : <span className="text-slate-500 animate-pulse">Waiting...</span>}
                      </td>
                      <td className="px-6 py-4 font-mono">{p.waiting_time !== null ? `${p.waiting_time}m` : '-'}</td>
                    </tr>
                  ))}
                  {patients.length === 0 && (
                    <tr>
                      <td colSpan="6" className="px-6 py-12 text-center text-slate-500 italic">Queue is currently empty.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Gantt Chart & Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pb-10">
          
          <div className="glass-panel p-6 lg:col-span-2">
             <div className="flex items-center gap-3 mb-8">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                   <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
                </div>
                <h2 className="text-2xl font-bold text-white">Execution Timeline</h2>
             </div>

             {gantt.length === 0 ? (
               <div className="h-32 flex items-center justify-center border border-dashed border-slate-700 rounded-xl bg-slate-900/20">
                 <p className="text-slate-500">No execution data available.</p>
               </div>
             ) : (
               <div className="relative mt-4 mb-2">
                 <div className="w-full bg-slate-900/80 rounded-xl h-24 relative overflow-hidden border border-white/10 shadow-inner">
                   {gantt.map((block, idx) => {
                     const totalDuration = gantt[gantt.length - 1].end || 1;
                     const width = ((block.end - block.start) / totalDuration) * 100;
                     const left = (block.start / totalDuration) * 100;
                     const isIdle = block.id === 'IDLE';
                     
                     // Consistent color for each patient
                     const colorClass = isIdle ? 'bg-slate-800 border-dashed border-slate-600' : `bg-gradient-to-r ${colors[(block.id) % colors.length]} shadow-[0_0_15px_rgba(255,255,255,0.1)]`;
                     
                     return (
                       <div 
                         key={idx}
                         className={`absolute h-full flex flex-col justify-center items-center border-r border-white/20 transition-all hover:brightness-110 ${colorClass}`}
                         style={{ width: `calc(${width}% - 1px)`, left: `${left}%` }}
                         title={`${isIdle ? 'Idle' : 'Patient ID: ' + block.id} | ${block.start} - ${block.end}`}
                       >
                         <span className={`font-bold text-sm ${isIdle ? 'text-slate-500' : 'text-white drop-shadow-md'}`}>{isIdle ? 'IDLE' : `P${block.id}`}</span>
                         {!isIdle && <span className="text-[10px] text-white/80 font-mono mt-1">{block.end - block.start}m</span>}
                       </div>
                     );
                   })}
                 </div>
                 
                 <div className="flex justify-between text-xs text-slate-400 mt-4 font-mono px-1">
                   <span>T=0</span>
                   <span>T={gantt[gantt.length - 1].end}</span>
                 </div>
               </div>
             )}
          </div>
          
          <div className="glass-panel p-6 lg:col-span-1">
             <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-rose-500/10 rounded-lg">
                   <svg className="w-6 h-6 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>
                </div>
                <h2 className="text-xl font-bold text-white">Metrics</h2>
             </div>
             
             {metrics ? (
               <div className="h-48 w-full">
                 <Bar data={chartData} options={{ maintainAspectRatio: false, scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }, plugins: { legend: { labels: { color: '#e2e8f0' } } } }} />
               </div>
             ) : (
               <div className="h-48 flex items-center justify-center border border-dashed border-slate-700 rounded-xl bg-slate-900/20">
                 <p className="text-slate-500">Awaiting processing...</p>
               </div>
             )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
