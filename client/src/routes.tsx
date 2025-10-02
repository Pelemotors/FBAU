import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Posts from './pages/Posts';
import Groups from './pages/Groups';
import Schedules from './pages/Schedules';
import Logs from './pages/Logs';
import Settings from './pages/Settings';

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-md border-b">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex items-center space-x-8 space-x-reverse">
                <Link to="/" className="text-xl font-bold text-gray-800">
                  פייסבוק אוטומציה
                </Link>
                <div className="flex space-x-6 space-x-reverse">
                  <Link to="/" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    דשבורד
                  </Link>
                  <Link to="/posts" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    פוסטים
                  </Link>
                  <Link to="/groups" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    קבוצות
                  </Link>
                  <Link to="/schedules" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    תזמונים
                  </Link>
                  <Link to="/logs" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    לוגים
                  </Link>
                  <Link to="/settings" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    הגדרות
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/posts" element={<Posts />} />
            <Route path="/groups" element={<Groups />} />
            <Route path="/schedules" element={<Schedules />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default AppRoutes;
