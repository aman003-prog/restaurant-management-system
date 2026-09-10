import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { apiRequest } from "../api/client";

export default function Cart() {
  const { cartItems, loading, cartTotal, removeFromCart, clearCart, fetchCart } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [couponCode, setCouponCode] = useState("");
  const [discountInfo, setDiscountInfo] = useState(null);
  const [couponError, setCouponError] = useState(null);
  const [couponLoading, setCouponLoading] = useState(false);
  const [orderPlacing, setOrderPlacing] = useState(false);

  if (!isAuthenticated) {
    return (
      <div style={{ maxWidth: "600px", margin: "60px auto", textAlign: "center", padding: "20px" }}>
        <h2>Please log in to view your cart</h2>
        <p style={{ color: "#64748b", margin: "16px 0 24px" }}>
          You need an active account to manage your cart and place orders.
        </p>
        <Link
          to="/login"
          style={{
            background: "#2563eb",
            color: "white",
            textDecoration: "none",
            padding: "10px 24px",
            borderRadius: "8px",
            fontWeight: "600",
          }}
        >
          Go to Login
        </Link>
      </div>
    );
  }

  const handleApplyCoupon = async (e) => {
    e.preventDefault();
    if (!couponCode.trim()) return;

    setCouponLoading(true);
    setCouponError(null);
    try {
      const res = await apiRequest("/coupons/apply/", {
        method: "POST",
        body: JSON.stringify({ code: couponCode.trim() }),
      });
      setDiscountInfo(res);
    } catch (err) {
      setCouponError(err.message || "Invalid or expired coupon.");
      setDiscountInfo(null);
    } finally {
      setCouponLoading(false);
    }
  };

  const handlePlaceOrder = async () => {
    setOrderPlacing(true);
    try {
      const payload = {};
      if (discountInfo?.coupon_code) {
        payload.coupon_code = discountInfo.coupon_code;
      }

      await apiRequest("/orders/", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      await fetchCart();
      alert("🎉 Order placed successfully!");
      navigate("/orders");
    } catch (err) {
      alert(`Could not place order: ${err.message}`);
    } finally {
      setOrderPlacing(false);
    }
  };

  const finalTotal = discountInfo ? discountInfo.final_total : cartTotal;

  if (loading) return <p style={{ padding: "40px", textAlign: "center" }}>Loading your cart...</p>;

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "30px 20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
        <h1 style={{ margin: 0 }}>Shopping Cart</h1>
        {cartItems.length > 0 && (
          <button
            onClick={clearCart}
            style={{
              background: "none",
              border: "1px solid #ef4444",
              color: "#ef4444",
              padding: "6px 14px",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "13px",
            }}
          >
            Clear Cart
          </button>
        )}
      </div>

      {cartItems.length === 0 ? (
        <div style={{ textAlign: "center", padding: "60px 20px", background: "#f8fafc", borderRadius: "12px" }}>
          <h2>Your cart is currently empty</h2>
          <p style={{ color: "#64748b", marginBottom: "24px" }}>Hungry? Browse our menu and add your favorite dishes!</p>
          <Link
            to="/"
            style={{
              background: "#2563eb",
              color: "white",
              textDecoration: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              fontWeight: "600",
            }}
          >
            Browse Menu
          </Link>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: "30px" }}>
          {/* Cart Item List */}
          <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            {cartItems.map((item) => (
              <div
                key={item.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "16px",
                  border: "1px solid #e2e8f0",
                  borderRadius: "10px",
                  background: "white",
                }}
              >
                <div>
                  <h4 style={{ margin: "0 0 4px 0", fontSize: "16px" }}>
                    {typeof item.menu_item === "object" ? item.menu_item.title : `Item #${item.menu_item}`}
                  </h4>
                  <p style={{ margin: 0, color: "#64748b", fontSize: "14px" }}>
                    Qty: <strong>{item.quantity}</strong> × ${parseFloat(item.unit_price).toFixed(2)}
                  </p>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                  <span style={{ fontWeight: "700", fontSize: "16px" }}>
                    ${parseFloat(item.price).toFixed(2)}
                  </span>
                  <button
                    onClick={() => removeFromCart(item.id)}
                    style={{
                      background: "none",
                      border: "none",
                      color: "#94a3b8",
                      fontSize: "18px",
                      cursor: "pointer",
                    }}
                    title="Remove item"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Order Summary & Coupon */}
          <div style={{
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            borderRadius: "12px",
            padding: "24px",
            height: "fit-content",
          }}>
            <h3 style={{ margin: "0 0 16px 0" }}>Order Summary</h3>

            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", fontSize: "15px" }}>
              <span style={{ color: "#64748b" }}>Subtotal</span>
              <span style={{ fontWeight: "600" }}>${cartTotal.toFixed(2)}</span>
            </div>

            {discountInfo && (
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px", color: "#16a34a" }}>
                <span>Coupon ({discountInfo.coupon_code})</span>
                <span>-${parseFloat(discountInfo.discount_amount).toFixed(2)}</span>
              </div>
            )}

            <hr style={{ margin: "16px 0", borderColor: "#e2e8f0" }} />

            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "20px", fontSize: "18px" }}>
              <strong>Total</strong>
              <strong style={{ color: "#0f172a" }}>${parseFloat(finalTotal).toFixed(2)}</strong>
            </div>

            {/* Coupon input */}
            <form onSubmit={handleApplyCoupon} style={{ display: "flex", gap: "8px", marginBottom: "14px" }}>
              <input
                type="text"
                placeholder="Coupon code"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value)}
                style={{
                  flexGrow: 1,
                  padding: "8px 12px",
                  borderRadius: "6px",
                  border: "1px solid #cbd5e1",
                  textTransform: "uppercase",
                }}
              />
              <button
                type="submit"
                disabled={couponLoading}
                style={{
                  background: "#334155",
                  color: "white",
                  border: "none",
                  borderRadius: "6px",
                  padding: "8px 12px",
                  cursor: "pointer",
                  fontWeight: "600",
                }}
              >
                {couponLoading ? "..." : "Apply"}
              </button>
            </form>

            {couponError && <p style={{ color: "#dc2626", fontSize: "13px", margin: "0 0 14px 0" }}>{couponError}</p>}
            {discountInfo && (
              <p style={{ color: "#16a34a", fontSize: "13px", margin: "0 0 14px 0" }}>
                ✓ Coupon applied successfully!
              </p>
            )}

            <button
              onClick={handlePlaceOrder}
              disabled={orderPlacing}
              style={{
                width: "100%",
                background: "#16a34a",
                color: "white",
                border: "none",
                borderRadius: "8px",
                padding: "12px",
                fontSize: "16px",
                fontWeight: "700",
                cursor: "pointer",
              }}
            >
              {orderPlacing ? "Processing..." : "Place Order Now"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
