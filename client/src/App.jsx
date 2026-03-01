import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ExperimentForm from './components/ExperimentForm';
import CircuitCanvas from './components/CircuitCanvas';
import NewExperimentDialog from './components/NewExperimentDialog';
import { PlusCircle } from 'lucide-react';

function App() {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [experiments, setExperiments] = useState([]);
  const [activeExp, setActiveExp] = useState(null); // 當前正在編輯/顯示的實驗
  const [isIterating, setIsIterating] = useState(false);
  const [showCircuit, setShowCircuit] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/experiments')
      .then(res => res.json())
      .then(data => {
          console.log("從後端抓到的所有實驗:", data); // 在此檢查 data[0].input_data 是否存在
          setExperiments(data);
      })
      .catch(err => console.error("資料載入失敗:", err));
  }, []);

  const handleCreateNew = async (data) => {
    try {
      const response = await fetch('http://localhost:8000/experiments', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
      });
      const { id } = await response.json();
      
      const newExp = { id, ...data }; 
      setExperiments([newExp, ...experiments]);
      setActiveExp(newExp);
      setShowCircuit(false);
      setIsDialogOpen(false);
    } catch (err) {
        console.error("建立實驗失敗:", err);
    }
  };

  const handleClearAll = async () => {
    try {
        await fetch('http://localhost:8000/experiments', { method: 'DELETE' });
        setExperiments([]);
        setActiveExp(null);
        setShowCircuit(false);
    } catch (err) {
        console.error("清除資料失敗:", err);
    }
  };

  const handleStartIteration = async () => {
    if (!activeExp) return;
    setIsIterating(true);
    setShowCircuit(true);

    const payload = {
        title: activeExp.title,
        quantumN: activeExp.quantumN,
        mappings: activeExp.mappings || []
    };

    try {
        // 使用您後端定義的優化路由
        const response = await fetch(`http://localhost:8000/optimize/${activeExp.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = ""; 

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const parsedData = JSON.parse(line.replace('data: ', ''));
                    console.log("後端傳回的原始數據:", parsedData);
                    setActiveExp(prev => ({
                        ...prev,
                        circuit: parsedData.circuit,
                        epoch: parsedData.epoch,
                        progress: parsedData.total_epochs > 0 
                            ? Math.min(100, Math.round((parsedData.epoch / parsedData.total_epochs) * 100)) 
                            : 0,
                        circuit_data: parsedData.circuit_data || null
                    }));
                }
            }
        }
    } catch (error) {
        console.error("連接錯誤:", error);
    } finally {
        setIsIterating(false);
    }
  };

  const parseInputData = (inputDataString) => {
    if (!inputDataString) return [];
    
    return inputDataString.split('\n').filter(line => line.trim() !== "").map(line => {
        const [input, target] = line.split(',');
        const targetint = parseInt(target, 10)
        return { 
            input: input, 
            target: targetint,
            output: targetint.toString(2).padStart(input.length, '0')
        };
    });
  };

  return (
    <div className="flex h-screen bg-[#f8fafc] overflow-hidden">
      <Sidebar 
        isOpen={isSidebarOpen} 
        experiments={experiments} 
        onAdd={() => setIsDialogOpen(true)}
        onClearAll={handleClearAll}
        onSelect={async (exp) => {
          try {
              const response = await fetch(`http://localhost:8000/experiments/${exp.id}`);
              const fullData = await response.json();
              
              // 解析為包含 input 和 target 的物件陣列
              const mappedData = parseInputData(fullData.input_data);
              // console.log("解析後的映射資料:", mappedData); 
              let parsedCircuit = null;
              if (fullData.circuit_data) {
                  try {
                      // 如果後端存的是 JSON 字串，這裡必須解析
                      parsedCircuit = typeof fullData.circuit_data === 'string' 
                          ? JSON.parse(fullData.circuit_data) 
                          : fullData.circuit_data;
                  } catch (e) {
                      console.error("解析電路資料失敗:", e);
                  }
              }

              setActiveExp({
                  ...fullData,
                  mappings: mappedData,
                  circuit: parsedCircuit // 確保這裡存的是物件
              });
              
              setShowCircuit(!!parsedCircuit);
          } catch (err) {
              console.error("載入實驗詳情失敗", err);
          }
      }}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <Header toggleSidebar={() => setSidebarOpen(!isSidebarOpen)} />
        
        <main className="flex-1 p-8 overflow-y-auto">
          <div className="max-w-6xl mx-auto h-full">
            {activeExp ? (
              /* 已選取實驗時顯示主介面 */
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <ExperimentForm 
                  currentExp={activeExp}
                  setExp={setActiveExp}
                  onStart={handleStartIteration}
                  onClear={() => setShowCircuit(false)}
                  isIterating={isIterating}
                />
                <CircuitCanvas 
                  showCircuit={showCircuit} 
                  isIterating={isIterating} 
                  n={activeExp.quantumN} 
                  circuitData={activeExp.circuit}
                  progress={activeExp.progress || 0}
                />
              </div>
            ) : (
              /* 空白狀態：顯示新增按鈕 */
              <div className="h-full flex flex-col items-center justify-center text-center">
                <div className="bg-white p-12 rounded-3xl shadow-sm border border-slate-200 flex flex-col items-center max-w-md transition-all hover:shadow-md">
                  <div className="w-20 h-20 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6">
                    <PlusCircle size={40} />
                  </div>
                  <h2 className="text-2xl font-bold text-slate-800 mb-2">開始您的量子實驗</h2>
                  <p className="text-slate-500 mb-8 leading-relaxed">
                    目前尚未選取任何實驗。請從側邊欄選擇歷史紀錄，或點擊下方按鈕建立新的電路優化任務。
                  </p>
                  <button 
                    onClick={() => setIsDialogOpen(true)}
                    className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-bold transition shadow-lg shadow-blue-100"
                  >
                    立即建立新實驗
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>

      <NewExperimentDialog 
        isOpen={isDialogOpen} 
        onClose={() => setIsDialogOpen(false)} 
        onCreate={handleCreateNew} 
      />
    </div>
  );
}

export default App;