import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [marketData, setMarketData] = useState({ items: [], deal_count: 0, total_items: 0 });
  const [filteredItems, setFilteredItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('discount_percent');
  const [sortDirection, setSortDirection] = useState('desc');
  const [filterType, setFilterType] = useState('all');

  const fetchMarketData = () => {
    setLoading(true);
    setError(null);

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
  };

  useEffect(() => {
    fetchMarketData();
  }, []);

  useEffect(() => {
    let filtered = [...marketData.items];

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.market_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Apply type filter
    if (filterType === 'deals') {
      filtered = filtered.filter(item => item.discount_percent > 5);
    } else if (filterType === 'positive') {
      filtered = filtered.filter(item => item.discount_percent > 0);
    } else if (filterType === 'negative') {
      filtered = filtered.filter(item => item.discount_percent <= 0);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aVal = a[sortField];
      let bVal = b[sortField];

      if (sortField === 'market_name') {
        aVal = aVal.toLowerCase();
        bVal = bVal.toLowerCase();
      }

      if (sortDirection === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    setFilteredItems(filtered);
  }, [marketData, searchTerm, sortField, sortDirection, filterType]);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const getSortIndicator = (field) => {
    if (sortField !== field) return ' ↕';
    return sortDirection === 'asc' ? ' ↑' : ' ↓';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">Loading market data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="alert alert-error">
          Error: {error}
        </div>
        <button onClick={fetchMarketData} className="refresh-btn">Retry</button>
      </div>
    );
  }

  const { deal_count, total_items } = marketData;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Market Dashboard</h2>
        <div className="alert alert-info" style={{ marginBottom: '1rem' }}>
          Showing items with value over €40 only (500 items fetched)
        </div>
        <div className="dashboard-stats">
          <div className="stat-card">
            <h3>Total Items (€40+)</h3>
            <p>{total_items}</p>
          </div>
          <div className="stat-card">
            <h3>Potential Deals</h3>
            <p>{deal_count}</p>
          </div>
          <div className="stat-card">
            <h3>Filtered Results</h3>
            <p>{filteredItems.length}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-controls">
        <input
          type="text"
          placeholder="Search items..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Items</option>
          <option value="deals">Deals Only (&gt;5%)</option>
          <option value="positive">Positive Discount</option>
          <option value="negative">Negative Discount</option>
        </select>
        <button onClick={fetchMarketData} className="refresh-btn">
          Refresh Data
        </button>
      </div>

      {filteredItems.length === 0 ? (
        <div className="alert alert-info">
          No items found matching your criteria
        </div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('market_name')}>
                  Market Name{getSortIndicator('market_name')}
                </th>
                <th onClick={() => handleSort('purchase_price')}>
                  Purchase Price{getSortIndicator('purchase_price')}
                </th>
                <th onClick={() => handleSort('market_value')}>
                  Market Value{getSortIndicator('market_value')}
                </th>
                <th onClick={() => handleSort('discount_percent')}>
                  Discount %{getSortIndicator('discount_percent')}
                </th>
                <th onClick={() => handleSort('auction_ends_at')}>
                  Auction Ends{getSortIndicator('auction_ends_at')}
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.map((item, index) => (
                <tr key={index} className={item.discount_percent > 5 ? 'deal-row' : ''}>
                  <td>{item.market_name}</td>
                  <td>${(item.purchase_price / 100).toFixed(2)}</td>
                  <td>${(item.market_value / 100).toFixed(2)}</td>
                  <td className={item.discount_percent > 0 ? 'price-positive' : 'price-negative'}>
                    {item.discount_percent.toFixed(2)}%
                  </td>
                  <td>{new Date(item.auction_ends_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
