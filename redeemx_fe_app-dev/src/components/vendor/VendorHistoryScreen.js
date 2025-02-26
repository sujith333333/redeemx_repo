import React, { useEffect, useState } from 'react';
import { Card, Col, Container, Pagination, Row, Table } from 'react-bootstrap';
import { fetchCreditedTransactions, fetchDebitedTransactions, fetchTransactions } from '../../api/vendor';
import '../../styles/VendorHistoryScreen.css';
import Footer from '../common/Footer';

const VendorHistoryScreen = () => {
  const today = new Date().toISOString().split('T')[0]; // Default today
  const [transactions, setTransactions] = useState([]);
  const [startDate, setStartDate] = useState(today);
  const [endDate, setEndDate] = useState(today);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('All');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const itemsPerPage = 6;

  const fetchTransactionByType = async () => {
    try {
      setLoading(true);
      setError(null);
      let start = startDate || today;
      let end = endDate || today;

      if (new Date(start) > new Date(end)) {
        setError('Start date cannot be after end date.');
        setTransactions([]);
        setLoading(false);
        return;
      }

      const offset = (currentPage - 1) * itemsPerPage;
      let response = {};

      switch (filter) {
        case 'Credit':
          response = await fetchCreditedTransactions(startDate, endDate, itemsPerPage, offset);
          break;
        case 'Debit':
          response = await fetchDebitedTransactions(startDate, endDate, itemsPerPage, offset);
          break;
        default:
          response = await fetchTransactions(startDate, endDate, itemsPerPage, offset);
          break;
      }

      setTransactions(response.data || []);
      setTotalRecords(response.total || 0);
    } catch (error) {
      setError('Error fetching transactions.');
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactionByType();
  }, [startDate, endDate, filter, currentPage]);

  const totalPages = Math.ceil(totalRecords / itemsPerPage);

  return (
    <Container fluid className="pt-5 pb-5" style={{ marginTop: '70px' }}>
      <h4 className="text-center" style={{color:"#015295"}}>Transaction History</h4>
      <Row className="mb-1 d-flex justify-content-between align-items-left">
        <Col xs={12} md={6} className="d-flex gap-1 justify-content-left">
          <div className="filter-buttons-left mt-4">
            {['All', 'Credit', 'Debit'].map(type => (
              <span
                key={type}
                className={`filter-option ${filter === type ? 'active' : ''}`}
                onClick={() => setFilter(type)}
              >
                {type}
              </span>
            ))}
          </div>
        </Col>
        <Col xs={12} md={6} className="d-flex flex-column align-items-end">
          <p className="text-left" style={{ textAlign: 'right', marginRight: '100px', color: '#015295' }}>
            <b>Date Range</b>
          </p>
          <div className="d-flex" style={{ gap: '2px' }}>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="filter-input form-control mr-2"
              style={{ width: '150px' }}
            />
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="filter-input form-control"
              style={{ width: '150px' }}
            />
          </div>
        </Col>
      </Row>

      {loading && <p className="text-center">Loading transactions...</p>}
      {error && <p className="text-danger text-center">{error}</p>}
      {!loading && !error && transactions.length === 0 && (
        <p className="text-center" style={{color: "#015295"}}>No transactions found.</p>
      )}

      <Row className="mt-2 d-flex justify-content-center">
        <Col xs={12} md={12}  className="mb-1">
          {/* <Card className="p-2" style={{ maxHeight: '300px', overflowY: 'auto' }}> */}
            <Card.Body>
              <Card.Title className="d-flex justify-content-between align-items-center" style={{color: "#015295"}}>
                Transactions
              </Card.Title>
              <Table striped bordered hover responsive style={{marginTop:"20px"}}>
                <thead>
                  <tr>
                  <th style={{ backgroundColor: '#015295', color: '#fff' }}>ID</th>
                    <th style={{ backgroundColor: '#015295', color: '#fff' }}>Name</th>
                    <th style={{ backgroundColor: '#015295', color: '#fff' }}>Points</th>
                    <th style={{ backgroundColor: '#015295', color: '#fff' }}>Date & Time</th>
                  </tr>
                </thead>
                <tbody>
  {transactions.map((transaction, index) => (
    <tr key={transaction.id || `txn-${index + 1 + (currentPage - 1) * itemsPerPage}`}>
      <td>{index + 1 + (currentPage - 1) * itemsPerPage}</td> {/* Unique ID Calculation */}
      <td>{transaction.user}</td>
      <td className={transaction.points > 0 ? 'text-success' : 'text-danger'}>
        <b>₹ {transaction.points}</b>
      </td>
      <td>{new Date(transaction.date).toLocaleString()}</td>
    </tr>
  ))}
</tbody>

              </Table>
            </Card.Body>
          {/* </Card> */}
        </Col>
      </Row>
      <Row className="mt-3 d-flex justify-content-center">
        <Col xs={12} className="d-flex justify-content-center">
          <Pagination>
           <Pagination.Prev disabled={currentPage === 1} onClick={() => setCurrentPage(currentPage - 1)} />
           {[...Array(totalPages).keys()].map((page) => (
             <Pagination.Item key={page + 1} active={page + 1 === currentPage} onClick={() => setCurrentPage(page + 1)}>
               {page + 1}
              </Pagination.Item>
             ))}
             <Pagination.Next disabled={currentPage === totalPages} onClick={() => setCurrentPage(currentPage + 1)} />
           </Pagination>
         </Col>
       </Row>
      <Footer />
    </Container>
  );
};

export default VendorHistoryScreen;

