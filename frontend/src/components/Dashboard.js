import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [marketData, setMarketData] = useState({ items: [], deal_count: 0, total_items: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const headers = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    fetch('http://localhost:8000/api/market', { headers })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch market data');
        }
        return response.json();
      })
      .then(data => {
        console.log('Market data received:', data);
        setMarketData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching market data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div><h2>Dashboard</h2><p>Loading market data...</p></div>;
  }

  if (error) {
    return <div><h2>Dashboard</h2><p>Error: {error}</p></div>;
  }

  const { items, deal_count, total_items } = marketData;

  return (
    <div>
      <h2>Dashboard</h2>
      <div>
        <p>Total Items: {total_items} | Potential Deals: {deal_count}</p>
      </div>
      <h3>CS:GO Market Data</h3>
      {items.length === 0 ? (
        <p>No market data available</p>
      ) : (
        <table border="1" cellPadding="5" style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              <th>Market Name</th>
              <th>Purchase Price</th>
              <th>Market Value</th>
              <th>Discount %</th>
              <th>Auction Ends At</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={index} style={{ backgroundColor: item.discount_percent > 5 ? '#90EE90' : 'white' }}>
                <td>{item.market_name}</td>
                <td>${(item.purchase_price / 100).toFixed(2)}</td>
                <td>${(item.market_value / 100).toFixed(2)}</td>
                <td style={{ color: item.discount_percent > 0 ? 'green' : 'red' }}>
                  {item.discount_percent.toFixed(2)}%
                </td>
                <td>{new Date(item.auction_ends_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Dashboard;
