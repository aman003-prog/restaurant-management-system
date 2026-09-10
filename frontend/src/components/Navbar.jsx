import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { cartCount } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header style={{
      background: "#0f172a",
      color: "white",
      padding: "14px 28px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
      position: "sticky",
      top: 0,
      zIndex: 100,
    }}>
      {/* Brand Logo / Home */}
      <Link to="/" style={{ textDecoration: "none", color: "white", display: "flex", alignItems: "center", gap: "10px" }}>
        <span style={{ fontSize: "24px" }}>🍽️</span>
        <span style={{ fontSize: "20px", fontWeight: "700", letterSpacing: "-0.5px" }}>Little Lemon</span>
      </Link>

      {/* Navigation Links */}
      <nav style={{ display: "flex", alignItems: "center", gap: "24px" }}>
        <Link to="/" style={{ color: "#e2e8f0", textDecoration: "none", fontWeight: "500", fontSize: "15px" }}>
          Menu
        </Link>

        {isAuthenticated && (
          <Link to="/orders" style={{ color: "#e2e8f0", textDecoration: "none", fontWeight: "500", fontSize: "15px" }}>
            My Orders
          </Link>
        )}

        {/* Cart Link with Badge */}
        <Link to="/cart" style={{
          color: "white",
          textDecoration: "none",
          position: "relative",
          display: "flex",
          alignItems: "center",
          gap: "6px",
          background: "#1e293b",
          padding: "6px 14px",
          borderRadius: "20px",
          fontSize: "14px",
          fontWeight: "600",
        }}>
          🛒 Cart
          {cartCount > 0 && (
            <span style={{
              background: "#e11d48",
              color: "white",
              fontSize: "12px",
              borderRadius: "50%",
              padding: "2px 7px",
              fontWeight: "700",
            }}>
              {cartCount}
            </span>
          )}
        </Link>

        {/* Auth status */}
        {isAuthenticated ? (
          <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
            <span style={{ color: "#94a3b8", fontSize: "14px" }}>
              Hi, <strong style={{ color: "#f8fafc" }}>{user?.username || "User"}</strong>
            </span>
            <button
              onClick={handleLogout}
              style={{
                background: "#dc2626",
                color: "white",
                border: "none",
                borderRadius: "6px",
                padding: "6px 12px",
                fontSize: "13px",
                fontWeight: "600",
                cursor: "pointer",
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            style={{
              background: "#2563eb",
              color: "white",
              textDecoration: "none",
              padding: "7px 16px",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: "600",
            }}
          >
            Login
          </Link>
        )}
      </nav>
    </header>
  );
}
