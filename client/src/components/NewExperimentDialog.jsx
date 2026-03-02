import React, { useState, useEffect, useRef } from 'react';
import { X, ChevronLeft, ChevronRight, Upload, Table as TableIcon } from 'lucide-react';

    

const getInitialState = () => ({
    title: '未命名實驗',
    quantumN: 4,
    mappings: []
});

const NewExperimentDialog = ({ isOpen, onClose, onCreate }) => {
    const [step, setStep] = useState(1);
    const fileInputRef = useRef(null);
    const [formData, setFormData] = useState({
        title: '未命名實驗',
        quantumN: 4,
        mappings: [] // 儲存 Step 2 的表格數據
    });
    const isReady = step === 1 ? formData.title.length > 0 : formData.mappings.length > 0;

    useEffect(() => {
        if (isOpen) {
            setStep(1);
            setFormData(getInitialState()); 
        }
    }, [isOpen]);

    // 2. 當 N 改變時：只生成新的表格數據，不重置 title
    useEffect(() => {
        // 只有在視窗開啟時才執行
        if (isOpen) {
            const numRows = Math.pow(2, formData.quantumN);
            const newMappings = Array.from({ length: numRows }, (_, i) => ({
                input: i.toString(2).padStart(formData.quantumN, '0'),
                target: i,
                output: i.toString(2).padStart(formData.quantumN, '0')
            }));
            
            // 使用 prev 確保只更新 mappings，不影響 title
            setFormData(prev => ({ ...prev, mappings: newMappings }));
        }
    }, [formData.quantumN, isOpen]);

    if (!isOpen) return null;

    const nextStep = () => setStep(s => s + 1);
    const prevStep = () => setStep(s => s - 1);

    const handleClose = () => {
        setStep(1); // 關閉時重置步驟
        onClose();  // 執行外部傳入的關閉邏輯
    };

    const handleTableChange = (index, newValue) => {
        const updatedMappings = [...formData.mappings];
        const numericValue = parseInt(newValue, 10) || 0;
        const binaryValue = numericValue.toString(2).padStart(formData.quantumN, '0');

        updatedMappings[index] = {
            ...updatedMappings[index],
            target: newValue,
            output: binaryValue // 這裡儲存的是二進位字串
        };

        setFormData(prev => ({
            ...prev,
            mappings: updatedMappings
        }));
    };

    const handleFinalSubmit = () => {
        onCreate(formData);
        setStep(1); // 重置步驟
        onClose();
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const text = e.target.result;
            const values = text.split(',')
                .map(v => parseInt(v.trim()))
                .filter(v => !isNaN(v));

            const expectedCount = Math.pow(2, formData.quantumN);
            if (values.length !== expectedCount) {
                alert(`數據長度錯誤！\n\n您設定的量子位元數 N=${formData.quantumN}，預期需要 ${expectedCount} 個數據，但您上傳的檔案包含 ${values.length} 個數據。\n\n請調整數據後再上傳。`);
                return;
            }
            const updatedMappings = formData.mappings.map((mapping, idx) => {
                const newValue = values[idx];
                const binaryValue = newValue.toString(2).padStart(formData.quantumN, '0');
                
                return {
                    ...mapping,
                    target: newValue,
                    output: binaryValue
                };
            });

            setFormData(prev => ({ ...prev, mappings: updatedMappings }));
        };
        reader.readAsText(file);
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
            <div className="bg-white w-full max-w-3xl rounded-xl shadow-2xl flex flex-col max-h-[90vh]">
                
                {/* Header */}
                <div className="flex justify-between items-center p-6 border-b border-slate-100">
                <h3 className="text-xl font-bold text-slate-800">配置實驗參數 ({step}/3)</h3>
                <button onClick={handleClose} className="text-slate-400 hover:text-slate-600 transition-colors">
                    <X size={20} />
                </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-8">
                
                {/* Step 1: 設定實驗基礎 */}
                {step === 1 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
                    <h4 className="text-2xl font-bold text-slate-800">第一步：設定實驗基礎</h4>
                    <div className="space-y-6">
                        <div className="flex items-center gap-4">
                        <label className="w-32 font-medium text-slate-700">實驗名稱：</label>
                        <input 
                            type="text"
                            className="flex-1 p-2 border border-blue-100 rounded-lg bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none"
                            value={formData.title}
                            onChange={(e) => setFormData({...formData, title: e.target.value})}
                        />
                        </div>
                        <div className="flex items-center gap-4">
                        <label className="w-32 font-medium text-slate-700">量子位元數 (N): </label>
                        <input 
                            type="number"
                            className="w-24 p-2 border border-blue-100 rounded-lg bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none"
                            value={formData.quantumN}
                            onChange={(e) => setFormData({...formData, quantumN: parseInt(e.target.value) || 0})}
                        />
                        </div>
                    </div>
                    </div>
                )}

                {/* Step 2: 輸入數據 */}
                {step === 2 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                    <h4 className="text-2xl font-bold text-slate-800">第二步：輸入數據</h4>
                    <div className="flex gap-3">
                        {/* 隱藏的檔案輸入框 */}
                        <input 
                            type="file" 
                            ref={fileInputRef} 
                            className="hidden" 
                            accept=".txt" 
                            onChange={handleFileUpload} 
                        />
                        {/* 觸發檔案上傳的按鈕 */}
                        <button 
                            onClick={() => fileInputRef.current.click()}
                            className="flex items-center gap-2 px-4 py-2 border border-blue-200 bg-blue-50 text-blue-700 rounded-lg text-sm font-medium hover:bg-blue-100 transition"
                        >
                            <Upload size={16} /> 從 TXT 上傳 (逗號分隔)
                        </button>
                    </div>

                    <div className="border border-slate-200 rounded-xl overflow-hidden">
                        <table className="w-full text-left border-collapse table-fixed">
                            <thead className="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th className="w-1/4 p-3 text-sm font-bold text-slate-600">輸入 |Input⟩</th>
                                    <th className="w-1/2 p-3 text-sm font-bold text-slate-600">目標輸出</th>
                                    <th className="w-1/4 p-3 text-sm font-bold text-slate-600">輸出預覽 |Output⟩</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {formData.mappings.map((row, idx) => (
                                    <tr key={idx} className="hover:bg-blue-50/30 transition-colors">
                                        {/* 輸入欄 */}
                                        <td className="p-3 text-sm font-mono text-indigo-600">|{row.input}⟩</td>
                                        
                                        {/* 輸入目標欄 */}
                                        <td className="p-2">
                                            <input 
                                                type="number"
                                                min="0"
                                                max={Math.pow(2, formData.quantumN) - 1}
                                                className="w-full p-2 border border-slate-200 rounded bg-white focus:border-blue-500 outline-none"
                                                value={row.target} // 確保 row.target 是定義好的
                                                onChange={(e) => handleTableChange(idx, e.target.value)}
                                            />
                                        </td>
                                        
                                        <td className="p-3 text-sm font-mono text-indigo-400">
                                            |{row.output ?? parseInt(row.target || 0).toString(2).padStart(formData.quantumN, '0')}⟩
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
                )}

                {/* Step 3: 最後確認 */}
                {step === 3 && (
                    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
                    <h4 className="text-2xl font-bold text-slate-800">第三步：最後確認</h4>
                    <div className="space-y-4 text-lg">
                        <p className="flex gap-2">
                        <span className="font-bold text-slate-600">實驗名稱：</span>
                        <span className="text-slate-800">{formData.title}</span>
                        </p>
                        <p className="flex gap-2">
                        <span className="font-bold text-slate-600">量子位元：</span>
                        <span className="text-slate-800">{formData.quantumN}</span>
                        </p>
                        <p className="flex gap-2 text-green-600 font-medium">
                        <span className="font-bold text-slate-600">數據狀態：</span>
                        已準備就緒
                        </p>
                    </div>
                    </div>
                )}

                </div>

                {/* Footer Actions */}
                <div className="p-6 border-t border-slate-100 flex justify-between bg-slate-50/50">
                {step > 1 ? (
                    <button 
                    onClick={prevStep}
                    className="px-6 py-2 border border-slate-300 bg-white rounded-xl font-bold text-slate-700 hover:bg-slate-50 transition"
                    >
                    上一步
                    </button>
                ) : <div></div>}
                
                {step < 3 ? (
                    <button 
                        onClick={nextStep}
                        // 透過條件式加入 animate-pulse 與 ring 效果
                        className={`px-8 py-2 border rounded-xl font-bold transition active:scale-95 shadow-sm 
                            ${isReady 
                                ? 'bg-blue-50 border-blue-300 text-blue-700 animate-pulse ring-4 ring-blue-500/30' 
                                : 'bg-white border-slate-200 text-slate-700 hover:shadow'
                            }
                        `}
                    >
                        下一步
                    </button>
                ) : (
                    <button 
                        onClick={handleFinalSubmit}
                        // 同樣加入 animate-pulse 與 ring 效果，讓視覺一致
                        className={`px-8 py-2 rounded-xl font-bold transition active:scale-95 shadow-lg 
                            ${isReady 
                                ? 'bg-blue-600 text-white animate-pulse ring-4 ring-blue-500/30' 
                                : 'bg-slate-900 text-white hover:bg-slate-800'
                            }
                        `}
                    >
                        確認並開始
                    </button>
                )}
                </div>
            </div>
        </div>
    );
};

export default NewExperimentDialog;