import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import MenuCard from "../components/MenuCard";

export default function Home() {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch categories once on mount
  useEffect(() => {
    apiRequest("/categories/")
      .then((data) => {
        const catList = Array.isArray(data) ? data : data.results || [];
        setCategories(catList);
      })
      .catch((err) => console.error("Could not fetch categories:", err));
  }, []);

  // Fetch menu items with search/filter
  useEffect(() => {
    setLoading(true);
    let url = "/menu-items/";
    const params = [];
    if (searchTerm) params.push(`search=${encodeURIComponent(searchTerm)}`);
    if (params.length > 0) url += `?${params.join("&")}`;

    apiRequest(url)
      .then((data) => {
        const results = Array.isArray(data) ? data : data.results || [];
        setItems(results);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [searchTerm]);

  // Filter items by selected category locally
  const filteredItems = items.filter((item) => {
    if (selectedCategory === "All") return true;
    return item.category === selectedCategory;
  });

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "30px 20px" }}>
      {/* Hero Banner */}
      <div style={{
        background: "linear-gradient(135deg, #1e293b, #0f172a)",
        color: "white",
        borderRadius: "16px",
        padding: "36px 30px",
        marginBottom: "36px",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}>
        <h1 style={{ margin: 0, fontSize: "32px", fontWeight: "800" }}>Delicious Food, Delivered Fast</h1>
        <p style={{ margin: 0, color: "#94a3b8", fontSize: "16px", maxWidth: "600px" }}>
          Explore our Mediterranean and artisanal menu prepared fresh by top chefs.
        </p>

        {/* Search Bar */}
        <div style={{ marginTop: "16px", maxWidth: "450px" }}>
          <input
            type="text"
            placeholder="Search pizza, pasta, drinks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: "100%",
              padding: "12px 16px",
              borderRadius: "8px",
              border: "none",
              fontSize: "15px",
              outline: "none",
              boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
            }}
          />
        </div>
      </div>

      {/* Category Filter Pills */}
      <div style={{ display: "flex", gap: "10px", overflowX: "auto", paddingBottom: "16px", marginBottom: "20px" }}>
        <button
          onClick={() => setSelectedCategory("All")}
          style={{
            padding: "8px 18px",
            borderRadius: "20px",
            border: "1px solid",
            borderColor: selectedCategory === "All" ? "#2563eb" : "#cbd5e1",
            background: selectedCategory === "All" ? "#2563eb" : "#f8fafc",
            color: selectedCategory === "All" ? "white" : "#334155",
            fontWeight: "600",
            fontSize: "14px",
            cursor: "pointer",
          }}
        >
          All
        </button>

        {categories.map((cat) => (
          <button
            key={cat.id || cat.slug}
            onClick={() => setSelectedCategory(cat.title)}
            style={{
              padding: "8px 18px",
              borderRadius: "20px",
              border: "1px solid",
              borderColor: selectedCategory === cat.title ? "#2563eb" : "#cbd5e1",
              background: selectedCategory === cat.title ? "#2563eb" : "#f8fafc",
              color: selectedCategory === cat.title ? "white" : "#334155",
              fontWeight: "600",
              fontSize: "14px",
              cursor: "pointer",
              whiteSpace: "nowrap",
            }}
          >
            {cat.title}
          </button>
        ))}
      </div>

      {/* Loading & Error States */}
      {loading && <p style={{ color: "#64748b", fontSize: "16px" }}>Loading menu items...</p>}
      {error && <p style={{ color: "#dc2626", fontSize: "16px" }}>Error: {error}</p>}

      {/* Menu Grid */}
      {!loading && !error && filteredItems.length === 0 && (
        <div style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
          <h3>No menu items found.</h3>
          <p>Try clearing your search or selecting another category.</p>
        </div>
      )}

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
        gap: "24px",
      }}>
        {filteredItems.map((item) => (
          <MenuCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}