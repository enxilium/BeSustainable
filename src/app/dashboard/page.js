'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { ArrowLeft, Info } from 'lucide-react';


export default function AboutPage() {
  const [selectedItem, setSelectedItem] = useState(null);
  

  // Mock data - replace with actual data in your app
  const savedMoney = 1250.75;
  const items = [
    { id: 1, name: 'Old Textbook', description: 'Computer Science 101 textbook from last semester.' },
    { id: 2, name: 'Unused Headphones', description: 'Brand new headphones, still in the box.' },
    { id: 3, name: 'Vintage Jacket', description: 'Leather jacket from the 90s, great condition.' },
  ];

  return (
    <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden mx-4">
      <main className="relative flex flex-col gap-8 items-center text-center w-full max-w-md">
        <Image
          className="dark:invert"
          src="/ecocloset_logo.png"
          alt="ECOCLOSET logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-5xl sm:text-5xl">About ECOCLOSET</h1>
        
        <div className="bg-green-100 rounded-lg p-4 w-full">
          <h2 className="text-2xl font-bold text-green-800">Total Savings</h2>
          <p className="text-4xl font-bold text-green-600">${savedMoney.toFixed(2)}</p>
        </div>
        
        <div className="w-full">
          <h3 className="text-xl font-bold mb-4">Your Items</h3>
          <ul className="space-y-4">
            {items.map((item) => (
              <li key={item.id} className="bg-white rounded-lg shadow-md p-4 flex justify-between items-center">
                <span>{item.name}</span>
                <button
                  onClick={() => setSelectedItem(item)}
                  className="bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
                >
                  <Info size={20} />
                </button>
              </li>
            ))}
          </ul>
        </div>
        
        {selectedItem && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg p-6 max-w-sm w-full">
              <h4 className="text-xl font-bold mb-2">{selectedItem.name}</h4>
              <p className="mb-4">{selectedItem.description}</p>
              <button
                onClick={() => setSelectedItem(null)}
                className="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
              >
                Close
              </button>
            </div>
          </div>
        )}
        
        <button
          className="bg-green-500 text-white py-2 px-4 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center"
        >
          <ArrowLeft size={20} className="mr-2" />
          Back to Home
        </button>
      </main>
    </div>
  );
}