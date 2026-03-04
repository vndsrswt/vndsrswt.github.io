import os
import zipfile

# Define the project structure and file contents
project_name = "box-breathing-app"

files = {
    f"{project_name}/package.json": r'''{
  "name": "box-breathing-app",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.344.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.64",
    "@types/react-dom": "^18.2.21",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.6"
  }
}''',

    f"{project_name}/vite.config.js": r'''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
''',

    f"{project_name}/tailwind.config.js": r'''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
''',

    f"{project_name}/postcss.config.js": r'''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''',

    f"{project_name}/index.html": r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#1c1917" />
    <title>Breathe | Visual Meditation</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''',

    f"{project_name}/src/index.css": r'''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  min-height: 100vh;
}
''',

    f"{project_name}/src/main.jsx": r'''import React from 'react'
import ReactDOM from 'react-dom/client'
import BoxBreathing from './BoxBreathing.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BoxBreathing />
  </React.StrictMode>,
)
''',

    f"{project_name}/src/BoxBreathing.jsx": r'''import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RefreshCw, Settings, Sun, Moon, Square, ArrowUpCircle, Clock, Download, X } from 'lucide-react';

const BoxBreathing = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [breathingMode, setBreathingMode] = useState('box'); // 'box' or 'deep'
  const [secondsPerPhase, setSecondsPerPhase] = useState(4);
  const [sessionLimit, setSessionLimit] = useState(0); // 0 = Infinite, value in minutes
  const [phase, setPhase] = useState('idle'); 
  const [timeLeft, setTimeLeft] = useState(4);
  const [progress, setProgress] = useState(0); 
  const [totalCycleCount, setTotalCycleCount] = useState(0);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallHelp, setShowInstallHelp] = useState(false);
  
  const requestRef = useRef();
  const startTimeRef = useRef();

  // Handle PWA Install Prompt
  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') setDeferredPrompt(null);
    } else {
      setShowInstallHelp(true);
    }
  };

  // Calculate Max Cycles for Session Limit
  const phaseCount = breathingMode === 'box' ? 4 : 3;
  const cycleDuration = secondsPerPhase * phaseCount;
  const maxCycles = sessionLimit > 0 ? Math.ceil((sessionLimit * 60) / cycleDuration) : 0;

  // --- Phase Configurations ---
  const getPhaseStyles = (type) => {
    const colors = {
      idle: {
        dark: { text: 'text-stone-300', bg: 'bg-stone-800' },
        light: { text: 'text-stone-500', bg: 'bg-stone-200' }
      },
      inhale: {
        dark: { text: 'text-rose-200', glow: 'shadow-[0_0_40px_rgba(254,205,211,0.4)]', bg: 'bg-rose-300/20', border: 'border-rose-200' },
        light: { text: 'text-rose-600', glow: 'shadow-[0_0_30px_rgba(244,63,94,0.2)]', bg: 'bg-rose-200/60', border: 'border-rose-400' }
      },
      hold: {
        dark: { text: 'text-violet-200', glow: 'shadow-[0_0_40px_rgba(221,214,254,0.4)]', bg: 'bg-violet-300/20', border: 'border-violet-200' },
        light: { text: 'text-violet-600', glow: 'shadow-[0_0_30px_rgba(139,92,246,0.2)]', bg: 'bg-violet-200/60', border: 'border-violet-400' }
      },
      exhale: {
        dark: { text: 'text-teal-200', glow: 'shadow-[0_0_40px_rgba(153,246,228,0.4)]', bg: 'bg-teal-300/20', border: 'border-teal-200' },
        light: { text: 'text-teal-600', glow: 'shadow-[0_0_30px_rgba(20,184,166,0.2)]', bg: 'bg-teal-200/60', border: 'border-teal-400' }
      },
      'hold-out': {
        dark: { text: 'text-orange-100', glow: 'shadow-[0_0_40px_rgba(255,237,213,0.4)]', bg: 'bg-orange-200/20', border: 'border-orange-100' },
        light: { text: 'text-orange-600', glow: 'shadow-[0_0_30px_rgba(249,115,22,0.2)]', bg: 'bg-orange-200/60', border: 'border-orange-400' }
      }
    };
    return colors[type][isDarkMode ? 'dark' : 'light'];
  };

  const getPhaseConfig = (currentPhase) => {
    const style = getPhaseStyles(currentPhase === 'hold-in' || currentPhase === 'hold-out' ? 'hold' : currentPhase);
    let config = { label: currentPhase.toUpperCase(), instruction: '', scale: 1, from: { x: 0, y: 0 }, to: { x: 0, y: 0 }, ...style };

    if (breathingMode === 'box') {
      switch (currentPhase) {
        case 'idle': config = { ...config, label: 'Ready?', instruction: 'Press Play', from: {x:0, y:100}, to: {x:0, y:100} }; break;
        case 'inhale': config = { ...config, label: 'Inhale', instruction: 'In through nose', scale: 1.5, from: {x:0, y:100}, to: {x:0, y:0} }; break;
        case 'hold-in': config = { ...config, label: 'Hold', instruction: 'Hold breath', scale: 1.5, from: {x:0, y:0}, to: {x:100, y:0} }; break;
        case 'exhale': config = { ...config, label: 'Exhale', instruction: 'Out through mouth', scale: 1, from: {x:100, y:0}, to: {x:100, y:100} }; break;
        case 'hold-out': config = { ...config, style: getPhaseStyles('hold-out'), label: 'Hold', instruction: 'Keep empty', scale: 1, from: {x:100, y:100}, to: {x:0, y:100} }; break;
        default: break;
      }
    } else {
      switch (currentPhase) {
        case 'idle': config = { ...config, label: 'Ready?', instruction: 'Press Play', from: {x:50, y:100}, to: {x:50, y:100} }; break;
        case 'inhale': config = { ...config, label: 'Inhale', instruction: 'Deep belly breath', scale: 1.5, from: {x:50, y:100}, to: {x:50, y:0} }; break;
        case 'hold-in': config = { ...config, label: 'Hold', instruction: 'Pause at top', scale: 1.5, from: {x:50, y:0}, to: {x:50, y:0} }; break;
        case 'exhale': config = { ...config, label: 'Exhale', instruction: 'Slow release', scale: 1, from: {x:50, y:0}, to: {x:50, y:100} }; break;
        default: break;
      }
    }
    return config;
  };

  const currentPhaseConfig = getPhaseConfig(phase);

  // --- Animation Loop ---
  const animate = (time) => {
    if (!isPlaying) return;
    if (!startTimeRef.current) startTimeRef.current = time;
    const elapsed = time - startTimeRef.current;
    const phaseDuration = secondsPerPhase * 1000;
    
    setProgress(Math.min(elapsed / phaseDuration, 1));
    const newTimeLeft = Math.ceil(secondsPerPhase - (elapsed / 1000));
    setTimeLeft(newTimeLeft > 0 ? newTimeLeft : 1);

    if (elapsed >= phaseDuration) {
      startTimeRef.current = null;
      switchPhase();
    } else {
      requestRef.current = requestAnimationFrame(animate);
    }
  };

  const switchPhase = () => {
    setPhase((prev) => {
      // Check for Session Limit End
      let nextCycleCount = totalCycleCount;
      const isCycleEnd = (breathingMode === 'box' && prev === 'hold-out') || (breathingMode === 'deep' && prev === 'exhale');
      
      if (isCycleEnd) {
         nextCycleCount = totalCycleCount + 1;
         setTotalCycleCount(nextCycleCount);
         // Stop if limit reached
         if (sessionLimit > 0 && nextCycleCount >= maxCycles) {
             setIsPlaying(false);
             return 'idle';
         }
      }

      if (breathingMode === 'box') {
        if (prev === 'idle') return 'inhale';
        if (prev === 'inhale') return 'hold-in';
        if (prev === 'hold-in') return 'exhale';
        if (prev === 'exhale') return 'hold-out';
        if (prev === 'hold-out') return 'inhale';
      } else {
        if (prev === 'idle') return 'inhale';
        if (prev === 'inhale') return 'hold-in';
        if (prev === 'hold-in') return 'exhale';
        if (prev === 'exhale') return 'inhale';
      }
      return 'idle';
    });
  };

  useEffect(() => {
    if (isPlaying) {
      if (phase === 'idle') setPhase('inhale');
      requestRef.current = requestAnimationFrame(animate);
    } else {
      cancelAnimationFrame(requestRef.current);
      startTimeRef.current = null;
    }
    return () => cancelAnimationFrame(requestRef.current);
  }, [isPlaying, phase, secondsPerPhase, breathingMode]);

  useEffect(() => { reset(); }, [breathingMode, sessionLimit]);

  const togglePlay = () => setIsPlaying(!isPlaying);
  
  const reset = () => {
    setIsPlaying(false);
    setPhase('idle');
    setTimeLeft(secondsPerPhase);
    setProgress(0);
    setTotalCycleCount(0);
    startTimeRef.current = null;
  };

  const cycleSessionLimit = () => {
    const limits = [0, 1, 2, 5, 10];
    const currentIndex = limits.indexOf(sessionLimit);
    setSessionLimit(limits[(currentIndex + 1) % limits.length]);
  };

  const getDotStyle = () => {
    const { from, to } = currentPhaseConfig;
    const x = from.x + (to.x - from.x) * progress;
    const y = from.y + (to.y - from.y) * progress;
    return { left: `${x}%`, top: `${y}%`, opacity: isPlaying ? 1 : 0.5 };
  };

  // --- Styles ---
  const themeClasses = {
    bg: isDarkMode ? 'bg-[#1c1917]' : 'bg-[#fafaf9]',
    text: isDarkMode ? 'text-stone-200' : 'text-stone-600',
    subText: isDarkMode ? 'text-stone-500' : 'text-stone-400',
    trackBorder: isDarkMode ? 'border-stone-800' : 'border-stone-200',
    dotBg: isDarkMode ? 'bg-[#f5f5f4]' : 'bg-stone-700',
    controlBg: isDarkMode ? 'bg-stone-900/80' : 'bg-white/80',
    controlBorder: isDarkMode ? 'border-stone-800/50' : 'border-stone-200',
    orbIdle: isDarkMode ? 'bg-stone-800' : 'bg-stone-200',
    buttonPrimary: isDarkMode 
      ? 'bg-[#fafaf9] text-stone-800 hover:bg-white' 
      : 'bg-stone-800 text-stone-100 hover:bg-stone-700',
    buttonSecondary: isDarkMode 
      ? 'bg-stone-800 text-stone-400 hover:bg-stone-700 hover:text-white' 
      : 'bg-white text-stone-500 hover:bg-stone-100 hover:text-stone-800',
    activeMode: isDarkMode ? 'bg-stone-700 text-stone-100' : 'bg-stone-300 text-stone-800',
    inactiveMode: isDarkMode ? 'text-stone-500 hover:text-stone-300' : 'text-stone-400 hover:text-stone-600'
  };

  let scaleValue = 1;
  if (phase === 'inhale') scaleValue = 1 + (0.5 * progress);
  else if (phase === 'hold-in') scaleValue = 1.5;
  else if (phase === 'exhale') scaleValue = 1.5 - (0.5 * progress);

  return (
    <div className={`h-[100dvh] w-full flex flex-col items-center justify-between p-6 font-sans transition-colors duration-1000 overflow-hidden ${themeClasses.bg} ${themeClasses.text}`}>
      
      {/* Install Help Modal */}
      {showInstallHelp && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-6" onClick={() => setShowInstallHelp(false)}>
          <div className={`p-6 rounded-2xl max-w-sm w-full shadow-2xl ${isDarkMode ? 'bg-stone-900 text-stone-200' : 'bg-white text-stone-800'}`} onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium">Install App</h3>
              <button onClick={() => setShowInstallHelp(false)}><X size={20}/></button>
            </div>
            <p className="text-sm opacity-80 mb-4">To install this app on your device:</p>
            <ul className="text-sm space-y-2 opacity-70 list-disc pl-4">
              <li><strong>iOS (Safari):</strong> Tap the Share button <span className="inline-block border px-1 rounded text-[10px]">↑</span> and select "Add to Home Screen".</li>
              <li><strong>Android (Chrome):</strong> Tap the Menu <span className="inline-block border px-1 rounded text-[10px]">⋮</span> and select "Install App" or "Add to Home Screen".</li>
            </ul>
          </div>
        </div>
      )}

      {/* Top Bar: Controls */}
      <div className="w-full flex justify-between items-center z-20 max-w-md">
         {/* Install Button (Mobile Friendly) */}
         <button 
           onClick={handleInstallClick}
           className={`p-3 rounded-full transition-all ${themeClasses.buttonSecondary}`}
           aria-label="Install App"
         >
           <Download size={20} />
         </button>

         {/* Mode Switcher */}
        <div className={`flex items-center p-1 rounded-full border ${themeClasses.controlBorder} ${themeClasses.controlBg} backdrop-blur-md`}>
            <button 
                onClick={() => setBreathingMode('box')}
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium transition-all ${breathingMode === 'box' ? themeClasses.activeMode : themeClasses.inactiveMode}`}
            >
                <Square size={16} />
            </button>
            <button 
                onClick={() => setBreathingMode('deep')}
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium transition-all ${breathingMode === 'deep' ? themeClasses.activeMode : themeClasses.inactiveMode}`}
            >
                <ArrowUpCircle size={16} />
            </button>
        </div>

        {/* Theme Toggle */}
        <button 
          onClick={() => setIsDarkMode(!isDarkMode)}
          className={`p-3 rounded-full transition-all ${themeClasses.buttonSecondary}`}
        >
          {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>

      {/* Center Visualizer */}
      <div className="flex-1 flex flex-col items-center justify-center w-full max-w-md relative">
        
        {/* Header (Fades out when playing on mobile to save space) */}
        <div className={`absolute top-0 transition-opacity duration-500 ${isPlaying ? 'opacity-0 md:opacity-100' : 'opacity-100'}`}>
           <h1 className="text-3xl font-light tracking-[0.2em] opacity-90 text-center">BREATHE</h1>
        </div>

        {/* Visualizer Track */}
        <div 
            className="relative transition-all duration-700 ease-in-out" 
            style={{ 
                width: breathingMode === 'box' ? 'min(80vw, 300px)' : 'min(30vw, 120px)', 
                height: 'min(80vw, 300px)' 
            }}
        >
            <div className={`absolute inset-0 border-4 transition-all duration-1000 ${themeClasses.trackBorder} ${breathingMode === 'box' ? 'rounded-3xl' : 'rounded-full'}`} />
            <div className={`absolute inset-0 border-4 transition-all duration-300 ${currentPhaseConfig.border} opacity-40 ${phase === 'idle' ? 'hidden' : ''} ${breathingMode === 'box' ? 'rounded-3xl' : 'rounded-full'}`} />
            
            {/* Dot */}
            <div 
            className={`absolute w-8 h-8 -ml-4 -mt-4 rounded-full shadow-lg z-20 transition-transform duration-75 ease-linear ${themeClasses.dotBg}`}
            style={getDotStyle()}
            >
                <div className={`w-full h-full rounded-full opacity-60 animate-pulse ${currentPhaseConfig.bg}`} />
            </div>

            {/* Inner Content */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div 
                    className={`absolute w-40 h-40 rounded-full blur-[60px] transition-all duration-75 opacity-50 ${phase === 'idle' ? themeClasses.orbIdle : currentPhaseConfig.bg.replace('/20', '').replace('/60', '')}`}
                    style={{ transform: `scale(${scaleValue})` }}
                />
                <div className="relative z-10 text-center flex flex-col items-center justify-center w-[200px]">
                    <div className={`text-2xl md:text-3xl font-light tracking-widest uppercase mb-1 transition-colors duration-500 ${currentPhaseConfig.text} drop-shadow-sm`}>
                    {currentPhaseConfig.label}
                    </div>
                    <div className={`text-5xl md:text-6xl font-thin tabular-nums tracking-tighter mb-1 drop-shadow-sm transition-colors duration-500 ${isDarkMode ? 'text-white/90' : 'text-stone-800'}`}>
                    {phase === 'idle' ? secondsPerPhase : timeLeft}
                    </div>
                    <div className={`text-xs font-medium tracking-wider opacity-80 uppercase ${themeClasses.subText}`}>
                    {currentPhaseConfig.instruction}
                    </div>
                </div>
            </div>

            {/* Markers (Box Only) */}
            <div className={`transition-opacity duration-500 ${breathingMode === 'box' ? 'opacity-100' : 'opacity-0'}`}>
                <div className={`absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 -mt-1 -ml-1 rounded-tl-xl transition-colors duration-1000 ${isDarkMode ? 'border-stone-700' : 'border-stone-300'}`} />
                <div className={`absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 -mt-1 -mr-1 rounded-tr-xl transition-colors duration-1000 ${isDarkMode ? 'border-stone-700' : 'border-stone-300'}`} />
                <div className={`absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 -mb-1 -ml-1 rounded-bl-xl transition-colors duration-1000 ${isDarkMode ? 'border-stone-700' : 'border-stone-300'}`} />
                <div className={`absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 -mb-1 -mr-1 rounded-br-xl transition-colors duration-1000 ${isDarkMode ? 'border-stone-700' : 'border-stone-300'}`} />
            </div>
        </div>
      </div>

      {/* Bottom Controls */}
      <div className="w-full max-w-md flex flex-col gap-4 z-10 pb-4">
        
        {/* Main Controls */}
        <div className="flex items-center justify-center gap-4 w-full">
            <button 
                onClick={reset}
                className={`p-4 rounded-full transition-all shadow-lg active:scale-95 ${themeClasses.buttonSecondary}`}
            >
                <RefreshCw size={20} />
            </button>

            <button 
                onClick={togglePlay}
                className={`flex-1 flex items-center justify-center gap-3 py-4 rounded-full font-light tracking-wide transition-all shadow-lg active:scale-95 text-lg ${themeClasses.buttonPrimary}`}
            >
                {isPlaying ? <Pause size={24} /> : <Play size={24} fill="currentColor" />}
                {isPlaying ? 'PAUSE' : 'BEGIN'}
            </button>
        </div>

        {/* Settings Panel */}
        <div className={`p-4 rounded-2xl border backdrop-blur-sm w-full transition-colors duration-1000 ${themeClasses.controlBg} ${themeClasses.controlBorder}`}>
            
            {/* Speed Slider */}
            <div className="mb-4">
                <div className={`flex justify-between items-center mb-2 text-sm ${themeClasses.subText}`}>
                    <div className="flex items-center gap-2">
                        <Settings size={14} />
                        <span className="text-xs uppercase tracking-wider">Speed (Sec/Phase)</span>
                    </div>
                    <span className={`font-mono ${isDarkMode ? 'text-stone-200' : 'text-stone-800'}`}>{secondsPerPhase}s</span>
                </div>
                <input 
                    type="range" min="2" max="10" value={secondsPerPhase} 
                    onChange={(e) => {
                        setSecondsPerPhase(parseInt(e.target.value));
                        if (!isPlaying) setTimeLeft(parseInt(e.target.value));
                    }}
                    className={`w-full h-2 rounded-lg appearance-none cursor-pointer ${isDarkMode ? 'bg-stone-700' : 'bg-stone-300'} accent-rose-400 touch-none`}
                />
            </div>

            {/* Session Limit Toggle */}
            <div className="flex justify-between items-center">
                 <div className={`flex items-center gap-2 text-sm ${themeClasses.subText}`}>
                    <Clock size={14} />
                    <span className="text-xs uppercase tracking-wider">Stop After</span>
                 </div>
                 <button 
                    onClick={cycleSessionLimit}
                    className={`px-3 py-1 rounded-md text-xs font-mono border transition-all ${isDarkMode ? 'border-stone-700 hover:bg-stone-800' : 'border-stone-300 hover:bg-stone-100'}`}
                 >
                    {sessionLimit === 0 ? '∞ Infinite' : `${sessionLimit} Min`}
                 </button>
            </div>
        </div>

        {/* Stats */}
        <div className={`text-center text-xs font-mono tracking-widest uppercase ${themeClasses.subText}`}>
          Cycles: <span className="opacity-100 mx-1">{totalCycleCount}</span> 
          {sessionLimit > 0 && <span className="opacity-50">/ ~{maxCycles}</span>}
        </div>
      </div>

    </div>
  );
};

export default BoxBreathing;
'''
}

# Create directory structure and write files
print(f"Creating project: {project_name}...")
for filepath, content in files.items():
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"  Created: {filepath}")

# Create Zip file
zip_filename = f"{project_name}.zip"
print(f"\nCompressing to {zip_filename}...")
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_name):
        for file in files:
            file_path = os.path.join(root, file)
            # Add file to zip (using relative path)
            zipf.write(file_path, os.path.relpath(file_path, "."))

print(f"\nSuccess! Created {zip_filename}")
print("You can now unzip this file and run 'npm install' then 'npm run dev' to start the app.")