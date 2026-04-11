// import { useState } from "react";
// import { useNavigate } from "react-router-dom";

// function Login() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const navigate = useNavigate();

//   const handleLogin = () => {
//     console.log(email, password);
//     navigate("/hotels");
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "100px" }}>
//       <h2>Login</h2>

//       <div>
//         <input
//           placeholder="Email"
//           onChange={(e) => setEmail(e.target.value)}
//         />
//       </div>

//       <div>
//         <input
//           type="password"
//           placeholder="Password"
//           onChange={(e) => setPassword(e.target.value)}
//         />
//       </div>

//       <button onClick={handleLogin}>Login</button>
//     </div>
//   );
// }

// export default Login;











import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; 


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

 







const handleLogin = async () => {
  try {
    const res = await api.post("/auth/login", {
      email,
      password,
    });

    console.log("LOGIN RESPONSE:", res.data);

    // ✅ SAVE TOKEN (MOST IMPORTANT FIX)
    localStorage.setItem("token", res.data.access_token);

    alert("Login successful!");

    navigate("/hotels");

  } catch (err) {
    console.log(err);
    alert("Login failed");
  }
};







  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Welcome Back 👋</h2>
        <p style={styles.subtitle}>Login to continue booking hotels</p>

        <input
          style={styles.input}
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={handleLogin}>
          Login
        </button>

        <p style={styles.footerText}>
          Don’t have an account?{" "}
          <span
            style={styles.link}
            onClick={() => navigate("/register")}
          >
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    fontFamily: "Arial, sans-serif",
  },

  card: {
    background: "white",
    padding: "40px",
    borderRadius: "15px",
    width: "320px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
    textAlign: "center",
  },

  title: {
    marginBottom: "5px",
    color: "#333",
  },

  subtitle: {
    fontSize: "12px",
    color: "gray",
    marginBottom: "20px",
  },

  input: {
    width: "100%",
    padding: "12px",
    margin: "10px 0",
    border: "1px solid #ddd",
    borderRadius: "8px",
    outline: "none",
    fontSize: "14px",
  },

  button: {
    width: "100%",
    padding: "12px",
    background: "#667eea",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginTop: "10px",
    fontSize: "15px",
    transition: "0.3s",
  },

  footerText: {
    marginTop: "15px",
    fontSize: "12px",
    color: "gray",
  },

  link: {
    color: "#667eea",
    cursor: "pointer",
    fontWeight: "bold",
  },
};

export default Login;