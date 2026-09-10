import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({
    username: "",
    email: "",
    phone_number: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isRegister) {
        await register(form);
      } else {
        await login(form.username, form.password);
      }
      navigate("/");
    } catch (err) {
      setError(err.message || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "420px", margin: "60px auto", padding: "30px", background: "white", borderRadius: "14px", border: "1px solid #e2e8f0", boxShadow: "0 4px 12px rgba(0,0,0,0.06)" }}>
      {/* Toggle between Login and Register */}
      <div style={{ display: "flex", borderBottom: "1px solid #e2e8f0", marginBottom: "24px" }}>
        <button
          onClick={() => { setIsRegister(false); setError(null); }}
          style={{
            flex: 1,
            padding: "10px",
            border: "none",
            background: "none",
            borderBottom: !isRegister ? "2px solid #2563eb" : "none",
            color: !isRegister ? "#2563eb" : "#64748b",
            fontWeight: "700",
            fontSize: "15px",
            cursor: "pointer",
          }}
        >
          Login
        </button>
        <button
          onClick={() => { setIsRegister(true); setError(null); }}
          style={{
            flex: 1,
            padding: "10px",
            border: "none",
            background: "none",
            borderBottom: isRegister ? "2px solid #2563eb" : "none",
            color: isRegister ? "#2563eb" : "#64748b",
            fontWeight: "700",
            fontSize: "15px",
            cursor: "pointer",
          }}
        >
          Create Account
        </button>
      </div>

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        <div>
          <label style={{ display: "block", marginBottom: "6px", fontSize: "14px", fontWeight: "600" }}>Username</label>
          <input
            type="text"
            name="username"
            required
            value={form.username}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
          />
        </div>

        {isRegister && (
          <>
            <div>
              <label style={{ display: "block", marginBottom: "6px", fontSize: "14px", fontWeight: "600" }}>Email</label>
              <input
                type="email"
                name="email"
                required
                value={form.email}
                onChange={handleChange}
                style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "6px", fontSize: "14px", fontWeight: "600" }}>Phone Number</label>
              <input
                type="text"
                name="phone_number"
                value={form.phone_number}
                onChange={handleChange}
                placeholder="Optional"
                style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
              />
            </div>
          </>
        )}

        <div>
          <label style={{ display: "block", marginBottom: "6px", fontSize: "14px", fontWeight: "600" }}>Password</label>
          <input
            type="password"
            name="password"
            required
            value={form.password}
            onChange={handleChange}
            style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
          />
        </div>

        {isRegister && (
          <div>
            <label style={{ display: "block", marginBottom: "6px", fontSize: "14px", fontWeight: "600" }}>Confirm Password</label>
            <input
              type="password"
              name="password_confirm"
              required
              value={form.password_confirm}
              onChange={handleChange}
              style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #cbd5e1", boxSizing: "border-box" }}
            />
          </div>
        )}

        {error && (
          <p style={{ color: "#dc2626", fontSize: "13px", margin: 0 }}>
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "8px",
            padding: "12px",
            fontSize: "15px",
            fontWeight: "700",
            cursor: "pointer",
            marginTop: "8px",
          }}
        >
          {loading ? "Processing..." : isRegister ? "Sign Up" : "Sign In"}
        </button>
      </form>
    </div>
  );
}
