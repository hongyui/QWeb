import React from 'react';
import { Plus, Trash2, History, Cpu } from 'lucide-react';

const Sidebar = ({ isOpen, experiments, onAdd, onClearAll, onSelect }) => {
    return (
        // 外層 aside：只負責控制「可視區域」的寬度
        <aside 
            className={`bg-slate-900 text-white transition-all duration-300 ease-in-out border-r border-slate-800 flex flex-col ${isOpen ? 'w-64' : 'w-0'} overflow-hidden`}
        >
            {/* 內層容器：固定寬度 256px (w-64)，保證內容永遠不會被壓縮 */}
            <div className="w-64 flex flex-col h-full">
                <div className="p-4 flex items-center gap-2 border-b border-slate-800">
                    <Cpu className="text-blue-400 shrink-0" />
                    <span className="font-bold text-lg whitespace-nowrap tracking-tight">量子實驗平台</span>
                </div>
                
                <div className="p-4">
                    <button 
                        onClick={onAdd}
                        className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 py-2.5 rounded-lg font-medium transition-all active:scale-95 whitespace-nowrap"
                    >
                        <Plus size={18} /> 新增實驗
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto px-3">
                    <div className="text-[10px] font-bold text-slate-500 px-2 mb-3 uppercase tracking-[0.2em] flex items-center gap-2">
                        <History size={12} className="shrink-0" /> 歷史紀錄
                    </div>
                    <div className="space-y-1">
                        {experiments.map((exp) => (
                            <div 
                                key={exp.id} 
                                onClick={() => onSelect(exp)}
                                className="group flex items-center justify-between p-2.5 hover:bg-slate-800 rounded-lg cursor-pointer transition-colors"
                            >
                                <div className="truncate text-sm text-slate-300 group-hover:text-white">
                                    {exp.title}
                                </div>
                                <span className="text-[10px] bg-slate-700 px-1.5 py-0.5 rounded text-slate-400 uppercase shrink-0 ml-2">
                                    n={exp.quantumN}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="p-4 border-t border-slate-800">
                    <button 
                        onClick={onClearAll}
                        className="w-full flex items-center gap-2 text-xs text-slate-500 hover:text-red-400 transition-colors whitespace-nowrap"
                    >
                        <Trash2 size={14} className="shrink-0" /> 清除所有歷史數據
                    </button>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;