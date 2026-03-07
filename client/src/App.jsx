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
		if (window.confirm("確定要刪除所有實驗嗎？")) {
			try {
				await fetch('http://localhost:8000/experiments', { method: 'DELETE' });
				setExperiments([]);
				setActiveExp(null);
				setShowCircuit(false);
			} catch (err) {
				console.error("清除資料失敗:", err);
			}
		}
	};

	const handleClear = async () => {
		if (!activeExp) return;
		const updatedExp = { ...activeExp, circuit: null, circuit_data: null };
		setActiveExp(updatedExp);
		setShowCircuit(false);

		setExperiments(prev => prev.map(exp => 
			exp.id === updatedExp.id ? updatedExp : exp
		));

		// 同步後端
		try {
			await fetch(`http://localhost:8000/experiments/${updatedExp.id}`, {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ circuit_data: null })
			});
		} catch (err) {
			console.error("清除電路資料失敗:", err);
		}
	};

	const handleExport = async () => {
		// 檢查是否有有效的實驗與電路數據
		if (!activeExp || !activeExp.circuit) {
			alert("目前沒有可匯出的電路資料！");
			return;
		}

		try {
			// 呼叫後端新增的 generate-qasm 路由
			const response = await fetch('http://localhost:8000/generate-qasm', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					circuit: activeExp.circuit,
					title: activeExp.title || "circuit"
				}),
			});

			if (!response.ok) {
				throw new Error('後端生成 QASM 失敗');
			}

			const data = await response.json();
			const qasmString = data.qasm;

			// 建立下載連結並觸發下載
			const blob = new Blob([qasmString], { type: "text/plain" });
			const url = URL.createObjectURL(blob);
			const link = document.createElement('a');
			link.href = url;
			link.download = `${data.title}.qasm`;
			document.body.appendChild(link);
			link.click();

			// 清理
			document.body.removeChild(link);
			URL.revokeObjectURL(url);

		} catch (error) {
			console.error("匯出失敗:", error);
			alert("匯出失敗，請檢查後端連線或電路數據是否正確。");
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

	const handleDelete = async (id) => {
		if (window.confirm("確定要刪除這個實驗嗎？")) {
			// 從前端 State 移除，讓 UI 即時更新
			setExperiments((prev) => prev.filter((exp) => exp.id !== id));
			try {
				await fetch(`http://localhost:8000/experiments/${id}`, {
					method: 'DELETE',
				});
			} catch (error) {
				console.error("刪除失敗:", error);
			}

			// 如果刪除的剛好是目前正在查看的實驗，則清空畫面
			if (activeExp && activeExp.id === id) {
				setActiveExp(null);
			}
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

	const handleBackToHome = () => {
		setActiveExp(null);
		setShowCircuit(false);
	};

	return (
		<div className="app-layout">
		<Sidebar 
			isOpen={isSidebarOpen} 
			experiments={experiments} 
			onAdd={() => setIsDialogOpen(true)}
			onClearAll={handleClearAll}
			onSelect={async (exp) => {
				try {
					const response = await fetch(`http://localhost:8000/experiments/${exp.id}`);
					const fullData = await response.json();
					const mappedData = parseInputData(fullData.input_data);
					let parsedCircuit = null;
					if (fullData.circuit_data) {
						try {
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
						circuit: parsedCircuit 
					});
					setShowCircuit(!!parsedCircuit);
				} catch (err) {
				console.error("載入實驗詳情失敗", err);
				}
			}}
			onDelete={handleDelete}
		/>

		<div className="flex-1 flex flex-col min-w-0">
			<Header
				toggleSidebar={() => setSidebarOpen(!isSidebarOpen)}
				onBackToHome={handleBackToHome}
			/>

			<main className="main-content">
				<div className="content-container">
					{activeExp ? (
							<div className="active-exp-wrapper">
								<ExperimentForm
								currentExp={activeExp}
								setExp={setActiveExp}
								onStart={handleStartIteration}
								onClear={handleClear}
								isIterating={isIterating}
								onExport={handleExport}/>

								<CircuitCanvas
								showCircuit={showCircuit}
								isIterating={isIterating}
								n={activeExp.quantumN}
								circuitData={activeExp.circuit}
								progress={activeExp.progress || 0}/>
							</div>
						) : (
						<div className="empty-dashboard-wrapper">

							{/* 歡迎列 */}
							<section className="welcome-section">
								<div>
									<h1 className="welcome-title">您好, 研究員</h1>
									<p className="welcome-subtitle">準備好開始新的量子電路優化了嗎？</p>
								</div>
								<div className="stat-card-group">
									<div className="stat-card">
										<div className="stat-card-label">系統狀態</div>
										<div className="stat-card-value status-ready">Ready</div>
									</div>
								</div>
							</section>

							{/* 主操作區 */}
							<div className="hero-grid">
								<div className="hero-banner">
									<div className="hero-content">
										<h2 className="hero-title">建立全新實驗</h2>
										<p className="hero-desc">
											目前尚未選取任何實驗。請從側邊欄選擇歷史紀錄，或點擊下方按鈕建立新的電路優化任務。
										</p>
										<button
										onClick={() => setIsDialogOpen(true)}
										className="hero-btn">
											<PlusCircle size={20} />
											立即開始
										</button>
									</div>
									<div className="hero-bg-icon">
										<PlusCircle size={240} />
									</div>
								</div>
							</div>

							{/* 底部資源 */}
							{/* <div className="resource-grid">
								<div className="resource-card">
									<div className="resource-icon-box bg-orange-100 text-orange-600">📚</div>
									<div className="resource-text">查看操作文件</div>
								</div>
								<div className="resource-card">
									<div className="resource-icon-box bg-purple-100 text-purple-600">🧪</div>
									<div className="resource-text">範例專案匯入</div>
								</div>
							</div> */}
						</div>
					)}
				</div>
			</main>
		</div>

		<NewExperimentDialog 
		isOpen={isDialogOpen} 
		onClose={() => setIsDialogOpen(false)} 
		onCreate={handleCreateNew} />
		</div>
	);
}

export default App;