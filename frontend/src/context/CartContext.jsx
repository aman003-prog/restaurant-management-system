import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { apiRequest } from "../api/client";
import { useAuth } from "./AuthContext";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const { isAuthenticated } = useAuth();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCart = useCallback(async () => {
    if (!isAuthenticated) {
      setCartItems([]);
      return;
    }
    setLoading(true);
    try {
      const data = await apiRequest("/cart/");
      const items = Array.isArray(data) ? data : data.results || [];
      setCartItems(items);
    } catch (err) {
      console.error("Failed to fetch cart:", err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const addToCart = async (menuItemId, quantity = 1) => {
    if (!isAuthenticated) {
      throw new Error("Please log in to add items to your cart.");
    }
    await apiRequest("/cart/", {
      method: "POST",
      body: JSON.stringify({
        menu_item: menuItemId,
        quantity,
      }),
    });
    await fetchCart();
  };

  const removeFromCart = async (cartItemId) => {
    await apiRequest(`/cart/${cartItemId}/`, {
      method: "DELETE",
    });
    await fetchCart();
  };

  const clearCart = async () => {
    await apiRequest("/cart/", {
      method: "DELETE",
    });
    setCartItems([]);
  };

  const cartCount = cartItems.reduce((sum, item) => sum + (item.quantity || 1), 0);
  const cartTotal = cartItems.reduce((sum, item) => sum + parseFloat(item.price || 0), 0);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        loading,
        cartCount,
        cartTotal,
        fetchCart,
        addToCart,
        removeFromCart,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error("useCart must be used within a CartProvider");
  return context;
}
