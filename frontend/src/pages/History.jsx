// import { useEffect, useState } from "react";
// import api from "../services/api";
// import { useNavigate } from "react-router-dom";

// function History() {
//   const [bookings, setBookings] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const navigate = useNavigate();

//   useEffect(() => {
//     fetchHistory();
//   }, []);

//   const fetchHistory = async () => {
//     try {
//       const token = localStorage.getItem("token");

//       const res = await api.get("/bookings/my-bookings", {
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       });

//       setBookings(res.data);
//     } catch (err) {
//       console.log(err);
//     }

//     setLoading(false);
//   };

//   return (
//     <div style={styles.container}>
//       <h2 style={styles.title}>📜 My Booking History</h2>

//       {loading ? (
//         <p>Loading...</p>
//       ) : bookings.length === 0 ? (
//         <p>No bookings found.</p>
//       ) : (
//         <div style={styles.grid}>
//           {bookings.map((b) => (
//             <div key={b.booking_id} style={styles.card}>
//               <h3>Booking #{b.booking_id}</h3>

//               <p><b>🏨 Hotel:</b> {b.hotel_name}</p>
//               <p><b>🛏 Room ID:</b> {b.room_id}</p>
//               <p><b>📅 Check-in:</b> {b.check_in}</p>
//               <p><b>📅 Check-out:</b> {b.check_out}</p>

//               <p>
//                 <b>Status:</b>{" "}
//                 <span
//                   style={{
//                     color:
//                       b.status === "CONFIRMED"
//                         ? "green"
//                         : b.status === "CANCELLED"
//                         ? "red"
//                         : "orange",
//                   }}
//                 >
//                   {b.status}
//                 </span>
//               </p>
//             </div>
//           ))}
//         </div>
//       )}

//       <button style={styles.button} onClick={() => navigate("/hotels")}>
//         ← Back to Hotels
//       </button>
//     </div>
//   );
// }

// const styles = {
//   container: {
//     padding: "30px",
//     minHeight: "100vh",
//     background: "#f4f6f8",
//   },

//   title: {
//     textAlign: "center",
//     marginBottom: "20px",
//   },

//   grid: {
//     display: "grid",
//     gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
//     gap: "20px",
//   },

//   card: {
//     background: "white",
//     padding: "20px",
//     borderRadius: "10px",
//     boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
//   },

//   button: {
//     marginTop: "20px",
//     padding: "10px 20px",
//     background: "black",
//     color: "white",
//     border: "none",
//     cursor: "pointer",
//     display: "block",
//     marginLeft: "auto",
//     marginRight: "auto",
//   },
// };

// export default History;













import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function History() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState(null);
  const [selectedPayment, setSelectedPayment] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await api.get("/bookings/my-bookings");
      setBookings(res.data);
    } catch (err) {
      console.log("Error fetching history:", err);
    }
    setLoading(false);
  };

  const cancelBooking = async (bookingId) => {
    try {
      setCancellingId(bookingId);

      await api.put(`/bookings/cancel/${bookingId}`);

      // 🔥 Update UI instantly (no refresh needed)
      setBookings((prev) =>
        prev.map((b) =>
          b.booking_id === bookingId
            ? { ...b, status: "CANCELLED" }
            : b
        )
      );
    } catch (err) {
      console.log("Cancel error:", err);
      alert("Failed to cancel booking");
    }

    setCancellingId(null);
  };

  // Get payment status color
  const getPaymentStatusColor = (status) => {
    if (status === "SUCCESS") return "green";
    if (status === "FAILED") return "red";
    return "orange";
  };

  // Calculate nights
  const calculateNights = (checkIn, checkOut) => {
    const inDate = new Date(checkIn);
    const outDate = new Date(checkOut);
    const diffTime = Math.abs(outDate - inDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📜 My Booking & Payment History</h2>

      {loading ? (
        <p>Loading...</p>
      ) : bookings.length === 0 ? (
        <p>No bookings found.</p>
      ) : (
        <div style={styles.grid}>
          {bookings.map((b) => {
            const nights = calculateNights(b.check_in, b.check_out);
            return (
              <div key={b.booking_id} style={styles.card}>
                <div style={styles.cardHeader}>
                  <h3>Booking #{b.booking_id}</h3>
                  <span style={{ ...styles.statusBadge, color: b.status === "CONFIRMED" ? "green" : "red" }}>
                    {b.status}
                  </span>
                </div>

                <div style={styles.cardContent}>
                  <p><b>🏨 Hotel:</b> {b.hotel_name}</p>
                  <p><b>🛏 Room ID:</b> {b.room_id}</p>
                  <p><b>📅 Check-in:</b> {b.check_in}</p>
                  <p><b>📅 Check-out:</b> {b.check_out}</p>
                  <p><b>🌙 Nights:</b> {nights}</p>

                  {/* PAYMENT SECTION */}
                  <div style={styles.paymentSection}>
                    <h4 style={styles.paymentTitle}>💳 Payment Details</h4>
                    {b.payment ? (
                      <div>
                        <p><b>Payment ID:</b> #{b.payment.payment_id}</p>
                        <p><b>Amount:</b> <span style={styles.amount}>₹{b.payment.amount.toFixed(2)}</span></p>
                        <p>
                          <b>Payment Status:</b>{" "}
                          <span style={{ ...styles.paymentStatus, color: getPaymentStatusColor(b.payment.status) }}>
                            {b.payment.status}
                          </span>
                        </p>
                        {b.payment.status === "FAILED" && (
                          <div style={styles.warningBox}>
                            ⚠️ Payment failed. Please retry payment.
                          </div>
                        )}
                      </div>
                    ) : (
                      <p style={{ color: "gray" }}>No payment information available</p>
                    )}
                  </div>
                </div>

                <div style={styles.cardActions}>
                  {b.status === "CONFIRMED" && (
                    <button
                      style={styles.cancelBtn}
                      disabled={cancellingId === b.booking_id}
                      onClick={() => cancelBooking(b.booking_id)}
                    >
                      {cancellingId === b.booking_id
                        ? "Cancelling..."
                        : "Cancel Booking"}
                    </button>
                  )}
                  
                  {b.payment && (
                    <button
                      style={styles.detailsBtn}
                      onClick={() => setSelectedPayment(b)}
                    >
                      View Payment Details
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* PAYMENT DETAIL MODAL */}
      {selectedPayment && (
        <div style={styles.modal}>
          <div style={styles.modalContent}>
            <div style={styles.modalHeader}>
              <h2>Payment Invoice</h2>
              <button
                style={styles.closeBtn}
                onClick={() => setSelectedPayment(null)}
              >
                ✕
              </button>
            </div>

            <div style={styles.invoiceContent}>
              <div style={styles.invoiceSection}>
                <h4>Booking Information</h4>
                <p><b>Booking ID:</b> {selectedPayment.booking_id}</p>
                <p><b>Hotel:</b> {selectedPayment.hotel_name}</p>
                <p><b>Check-in:</b> {selectedPayment.check_in}</p>
                <p><b>Check-out:</b> {selectedPayment.check_out}</p>
                <p><b>Nights:</b> {calculateNights(selectedPayment.check_in, selectedPayment.check_out)}</p>
              </div>

              <div style={styles.invoiceSection}>
                <h4>Payment Information</h4>
                <p><b>Payment ID:</b> {selectedPayment.payment.payment_id}</p>
                <p><b>Total Amount:</b> <span style={styles.largeAmount}>₹{selectedPayment.payment.amount.toFixed(2)}</span></p>
                <p><b>Status:</b> <span style={{ color: getPaymentStatusColor(selectedPayment.payment.status), fontWeight: "bold", fontSize: "16px" }}>
                  {selectedPayment.payment.status}
                </span></p>
              </div>

              {selectedPayment.payment.status === "FAILED" && (
                <div style={styles.failedBox}>
                  <p><b>⚠️ Payment Failed</b></p>
                  <p>Please contact support or retry the payment.</p>
                </div>
              )}

              {selectedPayment.payment.status === "SUCCESS" && (
                <div style={styles.successBox}>
                  <p><b>✓ Payment Successful</b></p>
                  <p>Your booking has been confirmed.</p>
                </div>
              )}

              <button
                style={styles.closeModalBtn}
                onClick={() => setSelectedPayment(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      <button style={styles.button} onClick={() => navigate("/hotels")}>
        ← Back to Hotels
      </button>
    </div>
  );
}

const styles = {
  container: {
    padding: "30px",
    minHeight: "100vh",
    background: "#f4f6f8",
  },

  title: {
    textAlign: "center",
    marginBottom: "30px",
    color: "#333",
    fontSize: "28px",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))",
    gap: "25px",
    marginBottom: "30px",
  },

  card: {
    background: "white",
    padding: "25px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
    border: "1px solid #e0e0e0",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "15px",
    borderBottom: "2px solid #f0f0f0",
    paddingBottom: "10px",
  },

  statusBadge: {
    padding: "5px 12px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "bold",
    backgroundColor: "#e8f5e9",
  },

  cardContent: {
    marginBottom: "15px",
  },

  paymentSection: {
    marginTop: "20px",
    padding: "15px",
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    border: "1px solid #e3f2fd",
  },

  paymentTitle: {
    marginTop: "0",
    marginBottom: "12px",
    color: "#1976d2",
    fontSize: "14px",
  },

  paymentStatus: {
    fontWeight: "bold",
    padding: "4px 8px",
    borderRadius: "4px",
    fontSize: "14px",
  },

  amount: {
    fontSize: "18px",
    fontWeight: "bold",
    color: "#2e7d32",
  },

  warningBox: {
    marginTop: "10px",
    padding: "10px",
    backgroundColor: "#fff3e0",
    borderLeft: "4px solid #ff9800",
    borderRadius: "4px",
    color: "#e65100",
    fontSize: "13px",
  },

  cardActions: {
    display: "flex",
    gap: "10px",
    flexDirection: "column",
  },

  cancelBtn: {
    marginTop: "10px",
    padding: "10px",
    width: "100%",
    background: "red",
    color: "white",
    border: "none",
    cursor: "pointer",
    borderRadius: "6px",
    fontWeight: "bold",
    transition: "0.3s",
  },

  detailsBtn: {
    marginTop: "10px",
    padding: "10px",
    width: "100%",
    background: "#1976d2",
    color: "white",
    border: "none",
    cursor: "pointer",
    borderRadius: "6px",
    fontWeight: "bold",
    transition: "0.3s",
  },

  button: {
    marginTop: "20px",
    padding: "12px 25px",
    background: "black",
    color: "white",
    border: "none",
    cursor: "pointer",
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    borderRadius: "6px",
    fontWeight: "bold",
  },

  // MODAL STYLES
  modal: {
    position: "fixed",
    top: "0",
    left: "0",
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: "1000",
  },

  modalContent: {
    background: "white",
    padding: "30px",
    borderRadius: "12px",
    maxWidth: "500px",
    width: "90%",
    maxHeight: "80vh",
    overflowY: "auto",
    boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
  },

  modalHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "25px",
    borderBottom: "2px solid #f0f0f0",
    paddingBottom: "15px",
  },

  closeBtn: {
    background: "transparent",
    border: "none",
    fontSize: "24px",
    cursor: "pointer",
    color: "#999",
  },

  invoiceContent: {
    marginBottom: "20px",
  },

  invoiceSection: {
    marginBottom: "25px",
    paddingBottom: "20px",
    borderBottom: "1px solid #e0e0e0",
  },

  largeAmount: {
    fontSize: "24px",
    fontWeight: "bold",
    color: "#2e7d32",
  },

  successBox: {
    marginTop: "20px",
    padding: "15px",
    backgroundColor: "#e8f5e9",
    borderLeft: "4px solid #4caf50",
    borderRadius: "4px",
    color: "#2e7d32",
  },

  failedBox: {
    marginTop: "20px",
    padding: "15px",
    backgroundColor: "#ffebee",
    borderLeft: "4px solid #f44336",
    borderRadius: "4px",
    color: "#c62828",
  },

  closeModalBtn: {
    width: "100%",
    padding: "12px",
    marginTop: "20px",
    background: "#333",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold",
  },
};

export default History;