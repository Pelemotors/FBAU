import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">דשבורד</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-xl font-semibold mb-4">סטטוס פייסבוק</h2>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>לא מחובר</span>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-xl font-semibold mb-4">פוסטים אחרונים</h2>
          <p className="text-gray-600">אין פוסטים עדיין</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <h2 className="text-xl font-semibold mb-4">תזמונים קרובים</h2>
          <p className="text-gray-600">אין תזמונים עדיין</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
