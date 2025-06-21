const { useState } = React;

function App() {
  const [sign, setSign] = useState("");
  const [roast, setRoast] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRoast = async () => {
    if (!sign) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/horoscope/${sign}/daily`);
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setRoast(data.roast);
    } catch (err) {
      setRoast("Error fetching horoscope");
    } finally {
      setLoading(false);
    }
  };

  return React.createElement(
    "div",
    { className: "container" },
    React.createElement("h1", null, "HoroscHope"),
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("input", {
        value: sign,
        onChange: (e) => setSign(e.target.value),
        placeholder: "Enter sign",
      }),
      React.createElement(
        "button",
        { onClick: fetchRoast, disabled: loading },
        "Get Roast"
      )
    ),
    loading && React.createElement("p", null, "Loading..."),
    roast && React.createElement("p", { className: "roast" }, roast)
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  React.createElement(App)
);
