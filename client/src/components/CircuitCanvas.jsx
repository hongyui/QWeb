import React from 'react';
import { Search } from 'lucide-react';

const CircuitCanvas = ({ showCircuit, isIterating, n, circuitData, progress = 0 }) => {
    const quantumN = parseInt(n) || 0;
    
    const stepWidth = circuitData && circuitData.length > 20 ? 50 : 80;
    const rowHeight = 60;
    const startX = 100;
    const startY = 60; 

    return (
        <div className="bg-[#0f172a] rounded-3xl shadow-2xl overflow-hidden min-h-[450px] flex flex-col border border-slate-800">
            {/* Header */}
            <div className="p-4 bg-slate-900/50 border-b border-slate-800 flex justify-between items-center">
                <div className="flex items-center gap-2">
                    <div className="flex gap-2">
                        <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
                    </div>
                    {/* 計算中文字 */}
                    {isIterating && (
                        <span className="text-[10px] font-mono text-blue-400 animate-pulse ml-2 tracking-widest">
                            CALCULATING...
                        </span>
                    )}
                </div>
                <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">Optimal Circuit View</span>
            </div>

            {/* 虛線進度條：固定在頂部 */}
            {isIterating && (
                <div className="w-full h-1 bg-slate-900">
                    <svg width="100%" height="100%">
                        <line 
                            x1="0" y1="2" x2="100%" y2="2" 
                            stroke="#334155" strokeWidth="2" strokeDasharray="4 4" 
                        />
                        <line 
                            x1="0" y1="2" x2={`${progress}%`} y2="2" 
                            stroke="#60fa7c" strokeWidth="2" 
                        />
                    </svg>
                </div>
            )}
            
            {/* 滾動容器 */}
            <div className="flex-1 overflow-auto p-10 flex items-center justify-start">
                {!showCircuit && !isIterating && (
                    <div className="text-slate-600 text-center w-full">
                        <Search size={32} className="opacity-20 mx-auto mb-4" />
                        <p className="text-sm">尚未生成電路。</p>
                    </div>
                )}

                {isIterating && !showCircuit && (
                    <div className="flex flex-col items-center gap-4 w-full">
                        <div className="w-64 bg-slate-800 rounded-full h-2.5 overflow-hidden">
                            <div className="bg-blue-500 h-2.5 rounded-full transition-all duration-300 ease-out" style={{ width: `${progress}%` }}></div>
                        </div>
                        <p className="text-slate-500 text-xs font-mono">{Math.round(progress)}%</p>
                    </div>
                )}

                {showCircuit && circuitData && (
                    <div className="animate-in fade-in zoom-in duration-500 min-w-full">
                        <svg width={Math.max(600, circuitData.length * stepWidth + 100)} height={quantumN * rowHeight + 50}>
                            {[...Array(quantumN)].map((_, i) => (
                                <g key={i}>
                                    <line x1="60" y1={startY + i * rowHeight} x2={startX + circuitData.length * stepWidth} y2={startY + i * rowHeight} stroke="#334155" strokeWidth="2" />
                                    <text x="20" y={startY + 5 + i * rowHeight} fill="#64748b" fontSize="12" className="font-mono font-bold">q[{i}]</text>
                                </g>
                            ))}

                            {circuitData.map((gateStep, stepIdx) => {
                                const x = startX + stepIdx * stepWidth;
                                const activeIndices = gateStep.map((v, i) => (v === 1 || v === 0 || v === 3) ? i : -1).filter(i => i !== -1);
                                
                                return (
                                    <g key={stepIdx}>
                                        <text x={x} y={startY - 30} textAnchor="middle" fill="#64748b" fontSize="10" className="font-mono font-bold">
                                            GATE {stepIdx + 1}
                                        </text>
                                        {activeIndices.map((rowIdx, idx) => {
                                            if (idx === activeIndices.length - 1) return null;
                                            const nextRowIdx = activeIndices[idx + 1];
                                            return (
                                                <line key={idx} x1={x} y1={startY + rowIdx * rowHeight + 10} x2={x} y2={startY + nextRowIdx * rowHeight - 10} stroke="#60a5fa" strokeWidth="2" />
                                            );
                                        })}
                                        {gateStep.map((val, rowIdx) => {
                                            if (val === 1) return <circle key={rowIdx} cx={x} cy={startY + rowIdx * rowHeight} r="6" fill="#60a5fa" />;
                                            if (val === 0) return <circle key={rowIdx} cx={x} cy={startY + rowIdx * rowHeight} r="6" fill="none" stroke="#60a5fa" strokeWidth="2" />;
                                            if (val === 3) return (
                                                <g key={rowIdx}>
                                                    <circle cx={x} cy={startY + rowIdx * rowHeight} r="10" fill="none" stroke="#6060fa" strokeWidth="2" />
                                                    <line x1={x-5} y1={startY + rowIdx * rowHeight} x2={x+5} y2={startY + rowIdx * rowHeight} stroke="#6060fa" strokeWidth="2" />
                                                    <line x1={x} y1={startY + rowIdx * rowHeight - 5} x2={x} y2={startY + rowIdx * rowHeight + 5} stroke="#6060fa" strokeWidth="2" />
                                                </g>
                                            );
                                            return null;
                                        })}
                                    </g>
                                );
                            })}
                        </svg>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CircuitCanvas;