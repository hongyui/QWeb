import React from 'react';
import { Menu, Zap } from 'lucide-react';
import logo from '../assets/logo.png';

const Header = ({ toggleSidebar }) => {
    return (
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-20">
            <div className="flex items-center gap-4">
                <button 
                onClick={toggleSidebar}
                className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-600"
                >
                    <Menu size={20} />
                </button>
                <div className="flex items-center gap-2.5">
                    <img 
                        src={logo} 
                        alt="QuantumSolver Logo" 
                        className="w-30 h-30 object-contain" 
                    />
                    <h1 className="text-xl font-extrabold tracking-tight text-slate-800">
                        Quantum<span className="text-blue-600">Solver</span>
                    </h1>
                </div>
            </div>
        
        </header>
    );
};

export default Header;