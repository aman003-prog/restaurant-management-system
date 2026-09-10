import { useState } from "react";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function MenuCard({ item }) {
  const { addToCart } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [quantity, setQuantity] = useState(1);
  const [btnState, setBtnState] = useState("idle"); // idle | adding | added

  const imageUrl = item.item_image
    ? item.item_image.startsWith("http")
      ? item.item_image
      : `http://localhost:8000${item.item_image}`
    : "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80";

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }
    setBtnState("adding");
    try {
      await addToCart(item.id, quantity);
      setBtnState("added");
      setTimeout(() => setBtnState("idle"), 1500);
    } catch (err) {
      alert(err.message);
      setBtnState("idle");
    }
  };

  return (
    <div style={{
      border: "1px solid #e2e8f0",
      borderRadius: "12px",
      overflow: "hidden",
      backgroundColor: "#fff",
      boxShadow: "0 4px 6px -1px rgba(0,0,0,0.07)",
      display: "flex",
      flexDirection: "column",
      transition: "transform 0.15s ease, box-shadow 0.15s ease",
    }}>
      <div style={{ position: "relative", width: "100%", height: "180px", overflow: "hidden" }}>
        <img
          src={imageUrl}
          alt={item.title}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
        <span style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          background: "rgba(15, 23, 42, 0.75)",
          color: "white",
          padding: "3px 8px",
          borderRadius: "6px",
          fontSize: "12px",
          fontWeight: "500",
          backdropFilter: "blur(4px)",
        }}>
          {item.category || "General"}
        </span>
      </div>

      <div style={{ padding: "16px", display: "flex", flexDirection: "column", flexGrow: 1 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "8px" }}>
          <h3 style={{ margin: 0, fontSize: "17px", fontWeight: "600", color: "#0f172a" }}>{item.title}</h3>
          <span style={{ fontSize: "18px", fontWeight: "700", color: "#16a34a" }}>
            ${parseFloat(item.price).toFixed(2)}
          </span>
        </div>

        <p style={{ color: "#64748b", fontSize: "13px", lineHeight: "1.4", margin: "0 0 14px 0", flexGrow: 1 }}>
          {item.description}
        </p>

        {/* Quantity and Add to Cart Button */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "auto" }}>
          <div style={{ display: "flex", alignItems: "center", border: "1px solid #cbd5e1", borderRadius: "6px" }}>
            <button
              onClick={() => setQuantity((q) => Math.max(1, q - 1))}
              style={{ padding: "6px 10px", border: "none", background: "none", cursor: "pointer", fontWeight: "bold" }}
            >
              -
            </button>
            <span style={{ padding: "0 8px", fontSize: "14px", fontWeight: "600" }}>{quantity}</span>
            <button
              onClick={() => setQuantity((q) => q + 1)}
              style={{ padding: "6px 10px", border: "none", background: "none", cursor: "pointer", fontWeight: "bold" }}
            >
              +
            </button>
          </div>

          <button
            onClick={handleAddToCart}
            disabled={btnState === "adding"}
            style={{
              flexGrow: 1,
              background: btnState === "added" ? "#16a34a" : "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "6px",
              padding: "9px 12px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: "pointer",
              transition: "background 0.2s ease",
            }}
          >
            {btnState === "adding" ? "Adding..." : btnState === "added" ? "✓ Added!" : "Add to Cart"}
          </button>
        </div>
      </div>
    </div>
  );
}