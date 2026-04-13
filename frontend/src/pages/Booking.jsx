// import { useState } from "react";
// import { useParams, useNavigate } from "react-router-dom";
// import api from "../services/api";

// function Booking() {
//   const { roomId } = useParams();
//   const navigate = useNavigate();

//   const [checkIn, setCheckIn] = useState("");
//   const [checkOut, setCheckOut] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");

//   const handleBooking = async () => {
//     setLoading(true);
//     setMessage("");

//     try {
//       const token = localStorage.getItem("token");

//       const res = await api.post(
//         `/bookings/book-room-proc`,
//         null, // no body (your backend uses query params)
//         {
//           params: {
//             room_id: roomId,
//             check_in: checkIn,
//             check_out: checkOut,
//           },
//           headers: {
//             Authorization: `Bearer ${token}`,
//           },
//         }
//       );

//       setMessage(res.data.message);

//       setTimeout(() => {
//         navigate("/history");
//       }, 1500);
//     } catch (err) {
//       console.log(err);

//       setMessage(
//         err.response?.data?.detail || "Booking failed"
//       );
//     }

//     setLoading(false);
//   };

//   return (
//     <div style={styles.container}>
//       <div style={styles.card}>
//         <h2>🏨 Book Room</h2>

//         <p>Room ID: {roomId}</p>

//         <input
//           type="date"
//           style={styles.input}
//           onChange={(e) => setCheckIn(e.target.value)}
//         />

//         <input
//           type="date"
//           style={styles.input}
//           onChange={(e) => setCheckOut(e.target.value)}
//         />

//         <button
//           style={styles.button}
//           onClick={handleBooking}
//           disabled={loading}
//         >
//           {loading ? "Booking..." : "Confirm Booking"}
//         </button>

//         {message && <p style={styles.message}>{message}</p>}

//         <p
//           style={{ cursor: "pointer", color: "blue" }}
//           onClick={() => navigate("/hotels")}
//         >
//           ← Back to Hotels
//         </p>
//       </div>
//     </div>
//   );
// }

// const styles = {
//   container: {
//     display: "flex",
//     justifyContent: "center",
//     alignItems: "center",
//     height: "100vh",
//     background: "#f4f6f8",
//   },
//   card: {
//     padding: "30px",
//     background: "white",
//     borderRadius: "10px",
//     width: "320px",
//     boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
//     textAlign: "center",
//   },
//   input: {
//     width: "100%",
//     padding: "10px",
//     margin: "10px 0",
//   },
//   button: {
//     width: "100%",
//     padding: "10px",
//     background: "green",
//     color: "white",
//     border: "none",
//     cursor: "pointer",
//   },
//   message: {
//     marginTop: "10px",
//     color: "red",
//   },
// };

// export default Booking;










import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

function Booking() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [bookingDetails, setBookingDetails] = useState(null);

  const handleBooking = async () => {
    setLoading(true);
    setMessage("");

    // ✅ basic validation
    if (!checkIn || !checkOut) {
      setMessage("Please select check-in and check-out dates");
      setLoading(false);
      return;
    }

    try {
      const res = await api.post(
        "/bookings/book-room-proc",
        null,
        {
          params: {
            room_id: roomId,
            check_in: checkIn,
            check_out: checkOut,
          },
        }
      );

      setMessage(res.data.message || "Booking successful!");
      
      // Fetch payment details after booking
      const bookingsRes = await api.get("/bookings/my-bookings");
      if (bookingsRes.data && bookingsRes.data.length > 0) {
        const latestBooking = bookingsRes.data[bookingsRes.data.length - 1];
        setBookingDetails(latestBooking);
        setBookingSuccess(true);
      }

    } catch (err) {
      console.log(err);
      setMessage(
        err.response?.data?.detail || "Booking failed"
      );
    }

    setLoading(false);
  };

  // Calculate nights for payment display
  const calculateNights = () => {
    if (!checkIn || !checkOut) return 0;
    const inDate = new Date(checkIn);
    const outDate = new Date(checkOut);
    const diffTime = Math.abs(outDate - inDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getPaymentStatusColor = (status) => {
    if (status === "SUCCESS") return "green";
    if (status === "FAILED") return "red";
    return "orange";
  };

  // Success screen
  if (bookingSuccess && bookingDetails) {
    return (
      <div style={styles.container}>
        <div style={styles.successCard}>
          <div style={styles.successIcon}>✓</div>
          <h2 style={styles.successTitle}>Booking Confirmed!</h2>

          <div style={styles.bookingDetailsBox}>
            <h3>Booking Details</h3>
            <p><b>Booking ID:</b> #{bookingDetails.booking_id}</p>
            <p><b>Hotel:</b> {bookingDetails.hotel_name}</p>
            <p><b>Check-in:</b> {bookingDetails.check_in}</p>
            <p><b>Check-out:</b> {bookingDetails.check_out}</p>
            <p><b>Nights:</b> {calculateNights()}</p>
          </div>

          {bookingDetails.payment && (
            <div style={styles.paymentDetailsBox}>
              <h3>Payment Details</h3>
              <p><b>Payment ID:</b> #{bookingDetails.payment.payment_id}</p>
              <p><b>Total Amount:</b> <span style={styles.paymentAmount}>₹{bookingDetails.payment.amount.toFixed(2)}</span></p>
              <p><b>Status:</b> <span style={{ color: getPaymentStatusColor(bookingDetails.payment.status), fontWeight: "bold" }}>
                {bookingDetails.payment.status}
              </span></p>

              {bookingDetails.payment.status === "SUCCESS" && (
                <div style={styles.confirmationMessage}>
                  ✓ Payment Successful. Your booking has been confirmed.
                </div>
              )}
            </div>
          )}

          <div style={styles.actionButtons}>
            <button
              style={styles.historyBtn}
              onClick={() => navigate("/history")}
            >
              View Booking History
            </button>

            <button
              style={styles.hotelBtn}
              onClick={() => navigate("/hotels")}
            >
              Back to Hotels
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2>🏨 Book Room</h2>

        <p style={styles.roomIdText}>Room ID: {roomId}</p>

        <input
          type="date"
          style={styles.input}
          value={checkIn}
          onChange={(e) => setCheckIn(e.target.value)}
        />

        <input
          type="date"
          style={styles.input}
          value={checkOut}
          onChange={(e) => setCheckOut(e.target.value)}
        />

        {checkIn && checkOut && (
          <div style={styles.pricePreview}>
            <p style={styles.nightsText}>Nights: {calculateNights()}</p>
          </div>
        )}

        <button
          style={styles.button}
          onClick={handleBooking}
          disabled={loading}
        >
          {loading ? "Booking..." : "Confirm Booking"}
        </button>

        {message && (
          <p style={styles.message}>
            {message.includes("failed") || message.includes("Failed")
              ? "❌ " + message
              : "✓ " + message}
          </p>
        )}

        <p
          style={{ cursor: "pointer", color: "blue" }}
          onClick={() => navigate("/hotels")}
        >
          ← Back to Hotels
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    padding: "20px",
  },

  card: {
    padding: "40px",
    background: "white",
    borderRadius: "12px",
    width: "100%",
    maxWidth: "400px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
    textAlign: "center",
  },

  successCard: {
    padding: "40px",
    background: "white",
    borderRadius: "12px",
    width: "100%",
    maxWidth: "500px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
  },

  successIcon: {
    fontSize: "60px",
    color: "#4caf50",
    marginBottom: "20px",
  },

  successTitle: {
    color: "#2e7d32",
    marginBottom: "25px",
    fontSize: "24px",
  },

  bookingDetailsBox: {
    background: "#f5f5f5",
    padding: "20px",
    borderRadius: "8px",
    marginBottom: "20px",
    textAlign: "left",
    borderLeft: "4px solid #2196f3",
  },

  paymentDetailsBox: {
    background: "#e8f5e9",
    padding: "20px",
    borderRadius: "8px",
    marginBottom: "20px",
    textAlign: "left",
    borderLeft: "4px solid #4caf50",
  },

  paymentAmount: {
    fontSize: "20px",
    fontWeight: "bold",
    color: "#2e7d32",
  },

  confirmationMessage: {
    marginTop: "15px",
    padding: "10px",
    backgroundColor: "#c8e6c9",
    borderRadius: "4px",
    color: "#2e7d32",
    fontWeight: "bold",
  },

  actionButtons: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },

  historyBtn: {
    width: "100%",
    padding: "12px",
    background: "#2196f3",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "14px",
  },

  hotelBtn: {
    width: "100%",
    padding: "12px",
    background: "#666",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "14px",
  },

  roomIdText: {
    color: "#666",
    marginBottom: "20px",
    fontWeight: "bold",
  },

  input: {
    width: "100%",
    padding: "12px",
    margin: "12px 0",
    border: "1px solid #ddd",
    borderRadius: "6px",
    outline: "none",
    fontSize: "14px",
    boxSizing: "border-box",
  },

  pricePreview: {
    background: "#fff3e0",
    padding: "15px",
    borderRadius: "6px",
    marginBottom: "15px",
    border: "1px solid #ffcc80",
  },

  nightsText: {
    margin: "0",
    color: "#f57c00",
    fontWeight: "bold",
  },

  button: {
    width: "100%",
    padding: "12px",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    marginTop: "15px",
    fontSize: "15px",
    fontWeight: "bold",
    transition: "opacity 0.3s",
  },

  message: {
    marginTop: "15px",
    color: "red",
    fontSize: "14px",
    padding: "10px",
    backgroundColor: "#ffebee",
    borderRadius: "4px",
  },
};

export default Booking;