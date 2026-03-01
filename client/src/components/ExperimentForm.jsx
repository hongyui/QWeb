import React, { useState } from 'react';
import { Play, RefreshCw, Table as TableIcon } from 'lucide-react';
import DataMappingTable from './DataMappingTable'; // 匯入拆分出來的元件

const ExperimentForm = ({ currentExp, onStart, onClear, isIterating }) => {
    const [isTableOpen, setIsTableOpen] = useState(false);

    if (!currentExp) return null;

    return (
        <>
            <div className="bg-white p-4 rounded-4xl shadow-sm border border-slate-200 mb-6 transition-all">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                    <div>
                        <h2 className="text-2xl font-black text-slate-900 tracking-tight">{currentExp.title}</h2>
                        <p className="text-slate-500 text-sm">N={currentExp.quantumN}</p>
                    </div>
                    <div className="flex gap-3 w-full md:w-auto">
                        <button 
                            onClick={() => setIsTableOpen(!isTableOpen)}
                            className="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 flex items-center gap-2 font-medium"
                        >
                            <TableIcon size={16} /> {isTableOpen ? '隱藏數據' : '查看數據'}
                        </button>
                        <button 
                            onClick={onStart}
                            disabled={isIterating}
                            className={`flex-1 md:flex-none flex items-center justify-center gap-2 px-8 py-2.5 rounded-xl font-bold transition-all ${
                                isIterating ? 'bg-slate-100 text-slate-400' : 'bg-slate-900 text-white hover:bg-slate-800'
                            }`}
                        >
                            {isIterating ? <RefreshCw className="animate-spin" size={18} /> : <Play size={18} />}
                            {isIterating ? '運算中' : '開始迭代'}
                        </button>
                        <button onClick={onClear} className="px-4 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50">
                            清除
                        </button>
                    </div>
                </div>
            </div>

            {/* 當 isTableOpen 為 true 時，顯示懸浮表格元件 */}
            {isTableOpen && (
                <DataMappingTable 
                    mappings={currentExp.mappings} 
                    onClose={() => setIsTableOpen(false)} 
                />
            )}
        </>
    );
};

export default ExperimentForm;