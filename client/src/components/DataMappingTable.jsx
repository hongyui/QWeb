import React from 'react';
import { X, Table as TableIcon } from 'lucide-react';

const DataMappingTable = ({ mappings, onClose }) => {
    return (
        /* 將動畫類別放在 className，不放在 CSS 的 @apply */
        <div className="floating-table-card transition-all transform scale-100 opacity-100">
            <div className="p-3 bg-slate-50 border-b flex justify-between items-center">
                <span className="flex items-center gap-2 font-bold text-xs text-slate-600 uppercase">
                    <TableIcon size={14} /> 數據映射表
                </span>
                <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
                    <X size={14} />
                </button>
            </div>
            <div className="max-h-[400px] overflow-y-auto">
                <table className="w-full text-left border-collapse">
                    <thead className="bg-slate-50 border-b border-slate-200 sticky top-0 shadow-sm">
                        <tr>
                            <th className="table-header-sm">輸入 |Input⟩</th>
                            <th className="table-header-sm">目標輸出</th>
                            <th className="table-header-sm">輸出預覽 |Output⟩</th>
                        </tr>
                    </thead>
                    <tbody>
                        {mappings?.map((row, idx) => (
                            <tr key={idx} className="border-b border-slate-50 hover:bg-blue-50/30 transition-colors">
                                <td className="table-cell-mono-primary">|{row.input}⟩</td>
                                <td className="p-3 text-sm text-slate-700">{row.target}</td>
                                <td className="table-cell-mono-indigo">|{row.output}⟩</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DataMappingTable;