import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function Orders() {
  const { isAuthenticated } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) return;

    apiRequest("/orders/")
      .then((data) => {
        const orderList = Array.isArray(data) ? data : data.results || [];
        setOrders(orderList);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div style={{ maxWidth: "500px", margin: "60px auto", textAlign: "center", padding: "20px" }}>
        <h2>Login to view your orders</h2>
        <Link
          to="/login"
          style={{
            display: "inline-block",
            marginTop: "16px",
            background: "#2563eb",
            color: "white",
            textDecoration: "none",
            padding: "10px 24px",
            borderRadius: "8px",
            fontWeight: "600",
          }}
        >
          Login
        </Link>
      </div>
    );
  }

  if (loading) return <p style={{ padding: "40px", textAlign: "center" }}>Loading orders...</p>;
  if (error) return <p style={{ padding: "40px", textAlign: "center", color: "#dc2626" }}>Error: {error}</p>;

  const getStatusColor = (status) => {
    switch (status) {
      case "DELIVERED":
        return { bg: "#dcfce7", color: "#15803d" };
      case "CONFIRMED":
      case "PREPARING":
        return { bg: "#dbeafe", color: "#1d4ed8" };
      case "OUT_FOR_DELIVERY":
        return { bg: "#fef3c7", color: "#b45309" };
      case "CANCELLED":
        return { bg: "#fee2e2", color: "#b91c1c" };
      default:
        return { bg: "#f1f5f9", color: "#475569" };
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "30px 20px" }}>
      <h1 style={{ marginBottom: "24px" }}>My Orders</h1>

      {orders.length === 0 ? (
        <div style={{ textAlign: "center", padding: "50px", background: "#f8fafc", borderRadius: "12px" }}>
          <h3>You haven't placed any orders yet.</h3>
          <Link
            to="/"
            style={{
              display: "inline-block",
              marginTop: "14px",
              background: "#2563eb",
              color: "white",
              textDecoration: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              fontWeight: "600",
            }}
          >
            Order Food
          </Link>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          {orders.map((order) => {
            const badge = getStatusColor(order.status);
            return (
              <div
                key={order.id}
                style={{
                  border: "1px solid #e2e8f0",
                  borderRadius: "12px",
                  padding: "20px",
                  background: "white",
                  boxShadow: "0 2px 4px rgba(0,0,0,0.04)",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
                  <div>
                    <h3 style={{ margin: "0 0 4px 0" }}>Order #{order.id}</h3>
                  </div>
                  <span style={{
                    background: badge.bg,
                    color: badge.color,
                    padding: "4px 12px",
                    borderRadius: "20px",
                    fontSize: "13px",
                    fontWeight: "700",
                  }}>
                    {order.status.replace(/_/g, " ")}
                  </span>
                </div>

                {/* Items in this order */}
                {order.items && order.items.length > 0 && (
                  <div style={{ borderTop: "1px solid #f1f5f9", paddingTop: "12px", marginBottom: "12px" }}>
                    {order.items.map((item) => (
                      <div key={item.id} style={{ display: "flex", justifyContent: "space-between", fontSize: "14px", padding: "4px 0", color: "#475569" }}>
                        <span>
                          {item.quantity}x {item.menu_item}
                        </span>
                        <span>${parseFloat(item.price).toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ borderTop: "1px solid #e2e8f0", paddingTop: "12px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ color: "#64748b", fontSize: "14px" }}>Total Paid / Due</span>
                  <strong style={{ fontSize: "18px", color: "#0f172a" }}>
                    ${parseFloat(order.total).toFixed(2)}
                  </strong>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
