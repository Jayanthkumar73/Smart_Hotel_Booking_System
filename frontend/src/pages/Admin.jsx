// import { useEffect, useState } from "react";
// import api from "../services/api";

// function Admin() {
//   const [hotels, setHotels] = useState([]);
//   const [rooms, setRooms] = useState([]);

//   useEffect(() => {
//     fetchHotels();
//     fetchRooms();
//   }, []);

//   const fetchHotels = async () => {
//     try {
//       const res = await api.get("/admin/hotels");
//       setHotels(res.data);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const fetchRooms = async () => {
//     try {
//       const res = await api.get("/admin/rooms");
//       setRooms(res.data);
//     } catch (err) {
//       console.log(err);
//     }
//   };

//   const deleteHotel = async (id) => {
//     await api.delete(`/admin/hotels/${id}`);
//     fetchHotels();
//   };

//   const deleteRoom = async (id) => {
//     await api.delete(`/admin/rooms/${id}`);
//     fetchRooms();
//   };

//   return (
//     <div style={styles.container}>
//       <h2>👑 Admin Dashboard</h2>

//       {/* HOTELS */}
//       <h3>🏨 Hotels</h3>
//       <table style={styles.table}>
//         <thead>
//           <tr>
//             <th>ID</th>
//             <th>Name</th>
//             <th>City</th>
//             <th>Action</th>
//           </tr>
//         </thead>

//         <tbody>
//           {hotels.map((h) => (
//             <tr key={h.hotel_id}>
//               <td>{h.hotel_id}</td>
//               <td>{h.name}</td>
//               <td>{h.city}</td>
//               <td>
//                 <button
//                   style={styles.deleteBtn}
//                   onClick={() => deleteHotel(h.hotel_id)}
//                 >
//                   Delete
//                 </button>
//               </td>
//             </tr>
//           ))}
//         </tbody>
//       </table>

//       {/* ROOMS */}
//       <h3 style={{ marginTop: "30px" }}>🛏️ Rooms</h3>

//       <table style={styles.table}>
//         <thead>
//           <tr>
//             <th>ID</th>
//             <th>Hotel ID</th>
//             <th>Type</th>
//             <th>Price</th>
//             <th>Action</th>
//           </tr>
//         </thead>

//         <tbody>
//           {rooms.map((r) => (
//             <tr key={r.room_id}>
//               <td>{r.room_id}</td>
//               <td>{r.hotel_id}</td>
//               <td>{r.room_type}</td>
//               <td>{r.price}</td>
//               <td>
//                 <button
//                   style={styles.deleteBtn}
//                   onClick={() => deleteRoom(r.room_id)}
//                 >
//                   Delete
//                 </button>
//               </td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// const styles = {
//   container: {
//     padding: "30px",
//     background: "#f4f6f8",
//     minHeight: "100vh",
//   },

//   table: {
//     width: "100%",
//     background: "white",
//     borderCollapse: "collapse",
//     marginTop: "10px",
//   },

//   deleteBtn: {
//     background: "red",
//     color: "white",
//     border: "none",
//     padding: "5px 10px",
//     cursor: "pointer",
//   },
// };

// export default Admin;












import { useEffect, useState } from "react";
import api from "../services/api";

function Admin() {
  const [hotels, setHotels] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    await Promise.all([fetchHotels(), fetchRooms()]);
    setLoading(false);
  };

  const fetchHotels = async () => {
    try {
      const res = await api.get("/admin/hotels");
      setHotels(res.data);
    } catch (err) {
      console.log("Hotels error:", err);
    }
  };

  const fetchRooms = async () => {
    try {
      const res = await api.get("/admin/rooms");
      setRooms(res.data);
    } catch (err) {
      console.log("Rooms error:", err);
    }
  };

  const deleteHotel = async (id) => {
    try {
      await api.delete(`/admin/hotels/${id}`);
      setHotels((prev) => prev.filter((h) => h.hotel_id !== id));
    } catch (err) {
      console.log("Delete hotel error:", err);
      alert("Failed to delete hotel");
    }
  };

  const deleteRoom = async (id) => {
    try {
      await api.delete(`/admin/rooms/${id}`);
      setRooms((prev) => prev.filter((r) => r.room_id !== id));
    } catch (err) {
      console.log("Delete room error:", err);
      alert("Failed to delete room");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>👑 Admin Dashboard</h2>

      {loading ? (
        <p>Loading admin data...</p>
      ) : (
        <>
          {/* HOTELS */}
          <h3>🏨 Hotels</h3>

          <table style={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>City</th>
                <th>Rating</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {hotels.map((h) => (
                <tr key={h.hotel_id}>
                  <td>{h.hotel_id}</td>
                  <td>{h.name}</td>
                  <td>{h.city}</td>
                  <td>{h.rating}</td>
                  <td>
                    <button
                      style={styles.deleteBtn}
                      onClick={() => deleteHotel(h.hotel_id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* ROOMS */}
          <h3 style={{ marginTop: "30px" }}>🛏️ Rooms</h3>

          <table style={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Hotel ID</th>
                <th>Type</th>
                <th>Price</th>
                <th>Capacity</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {rooms.map((r) => (
                <tr key={r.room_id}>
                  <td>{r.room_id}</td>
                  <td>{r.hotel_id}</td>
                  <td>{r.room_type}</td>
                  <td>{r.price}</td>
                  <td>{r.capacity}</td>
                  <td>
                    <button
                      style={styles.deleteBtn}
                      onClick={() => deleteRoom(r.room_id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    padding: "30px",
    background: "#f4f6f8",
    minHeight: "100vh",
  },

  title: {
    textAlign: "center",
    marginBottom: "20px",
  },

  table: {
    width: "100%",
    background: "white",
    borderCollapse: "collapse",
    marginTop: "10px",
  },

  deleteBtn: {
    background: "red",
    color: "white",
    border: "none",
    padding: "6px 12px",
    cursor: "pointer",
    borderRadius: "5px",
  },
};

export default Admin;