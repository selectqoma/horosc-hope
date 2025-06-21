const { useState } = React;

function Navigation({ currentPage, onPageChange }) {
  return React.createElement(
    "nav",
    { className: "navigation" },
    React.createElement(
      "button",
      {
        className: currentPage === "horoscope" ? "nav-btn active" : "nav-btn",
        onClick: () => onPageChange("horoscope")
      },
      "Horoscopes"
    ),
    React.createElement(
      "button",
      {
        className: currentPage === "birth-chart" ? "nav-btn active" : "nav-btn",
        onClick: () => onPageChange("birth-chart")
      },
      "Birth Chart"
    )
  );
}

function HoroscopePage() {
  const [birthDate, setBirthDate] = useState("");
  const [sign, setSign] = useState("");
  const [calculatedSign, setCalculatedSign] = useState("");
  const [signInfo, setSignInfo] = useState(null);
  const [roast, setRoast] = useState("");
  const [loading, setLoading] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState("daily");

  const calculateSign = async () => {
    if (!birthDate) return;
    setCalculating(true);
    try {
      const res = await fetch(`http://localhost:8000/calculate-sign/${birthDate}`);
      if (!res.ok) throw new Error("Failed to calculate sign");
      const data = await res.json();
      setCalculatedSign(data.zodiac_sign);
      setSignInfo(data.sign_info);
      setSign(data.zodiac_sign); // Auto-fill the sign input
    } catch (err) {
      setCalculatedSign("Error calculating sign");
      setSignInfo(null);
    } finally {
      setCalculating(false);
    }
  };

  const fetchRoast = async () => {
    if (!sign) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/horoscope/${sign}?period=${selectedPeriod}`);
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setRoast(data.roast);
    } catch (err) {
      setRoast("Error fetching horoscope");
    } finally {
      setLoading(false);
    }
  };

  const periodOptions = [
    { value: "daily", label: "Today" },
    { value: "yesterday", label: "Yesterday" },
    { value: "tomorrow", label: "Tomorrow" },
    { value: "weekly", label: "This Week" },
    { value: "monthly", label: "This Month" }
  ];

  return React.createElement(
    "div",
    { className: "page" },
    React.createElement("h2", null, "Daily Horoscopes"),
    
    // Date of Birth Section
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("h3", null, "Calculate Your Zodiac Sign"),
      React.createElement("input", {
        type: "date",
        value: birthDate,
        onChange: (e) => setBirthDate(e.target.value),
        placeholder: "Enter your birth date",
      }),
      React.createElement(
        "button",
        { onClick: calculateSign, disabled: calculating || !birthDate },
        calculating ? "Calculating..." : "Calculate Sign"
      )
    ),

    // Display calculated sign info
    calculatedSign && !calculatedSign.includes("Error") && React.createElement(
      "div",
      { className: "sign-info" },
      React.createElement("h3", null, `Your Sign: ${signInfo?.name || calculatedSign}`),
      signInfo && React.createElement(
        "div",
        { className: "sign-details" },
        React.createElement("p", null, `Element: ${signInfo.element}`),
        React.createElement("p", null, `Quality: ${signInfo.quality}`),
        React.createElement("p", null, `Ruler: ${signInfo.ruler}`),
        React.createElement("p", null, `Dates: ${signInfo.dates}`),
        React.createElement("p", null, `Traits: ${signInfo.traits.join(", ")}`)
      )
    ),

    // Manual Sign Input Section
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("h3", null, "Get Your Horoscope Roast"),
      React.createElement("input", {
        value: sign,
        onChange: (e) => setSign(e.target.value),
        placeholder: "Enter sign (or use calculated sign above)",
      }),
      React.createElement(
        "select",
        {
          value: selectedPeriod,
          onChange: (e) => setSelectedPeriod(e.target.value),
          className: "period-selector"
        },
        ...periodOptions.map(option =>
          React.createElement("option", {
            key: option.value,
            value: option.value
          }, option.label)
        )
      ),
      React.createElement(
        "button",
        { onClick: fetchRoast, disabled: loading || !sign },
        loading ? "Loading..." : "Get Roast"
      )
    ),
    
    loading && React.createElement("p", null, "Loading..."),
    roast && React.createElement(
      "div",
      { className: "roast-container" },
      React.createElement("h4", null, `${periodOptions.find(p => p.value === selectedPeriod)?.label} Horoscope`),
      React.createElement("p", { className: "roast" }, roast)
    )
  );
}

function CitySearch({ onCitySelect }) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const abortRef = React.useRef(null);
  const debounceRef = React.useRef(null);

  const searchCities = (searchQuery) => {
    if (abortRef.current) {
      abortRef.current.abort();
    }
    if (searchQuery.length < 2) {
      setSuggestions([]);
      setLoading(false);
      return;
    }
    setLoading(true);
    const controller = new AbortController();
    abortRef.current = controller;
    fetch(`http://localhost:8000/search-cities?query=${encodeURIComponent(searchQuery)}&limit=5`, {
      signal: controller.signal
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to search cities");
        return res.json();
      })
      .then(data => {
        setSuggestions(data.suggestions || []);
      })
      .catch(err => {
        if (err.name !== "AbortError") setSuggestions([]);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    setShowSuggestions(value.length >= 2);
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    debounceRef.current = setTimeout(() => {
      searchCities(value);
    }, 200);
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion.display_name);
    setSuggestions([]);
    setShowSuggestions(false);
    onCitySelect(suggestion);
  };

  React.useEffect(() => {
    return () => {
      if (abortRef.current) abortRef.current.abort();
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  return React.createElement(
    "div",
    { className: "city-search-container" },
    React.createElement("input", {
      type: "text",
      value: query,
      onChange: handleInputChange,
      placeholder: "Search for your birth city...",
      className: "city-search-input"
    }),
    loading && React.createElement("p", { className: "search-loading" }, "Searching..."),
    showSuggestions && suggestions.length > 0 && React.createElement(
      "div",
      { className: "suggestions-list" },
      ...suggestions.map((suggestion, index) =>
        React.createElement(
          "div",
          {
            key: index,
            className: "suggestion-item",
            onClick: () => handleSuggestionClick(suggestion)
          },
          suggestion.display_name
        )
      )
    )
  );
}

function BirthChartPage() {
  const [birthDate, setBirthDate] = useState("");
  const [birthTime, setBirthTime] = useState("");
  const [selectedCity, setSelectedCity] = useState(null);
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [birthChart, setBirthChart] = useState(null);
  const [roast, setRoast] = useState("");
  const [loading, setLoading] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [useCitySearch, setUseCitySearch] = useState(true);

  const handleCitySelect = (city) => {
    setSelectedCity(city);
    setLatitude(city.latitude.toString());
    setLongitude(city.longitude.toString());
  };

  const calculateBirthChart = async () => {
    if (!birthDate || !birthTime || !latitude || !longitude) return;
    setCalculating(true);
    try {
      const res = await fetch(`http://localhost:8000/birth-chart?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}`);
      if (!res.ok) throw new Error("Failed to calculate birth chart");
      const data = await res.json();
      setBirthChart(data);
    } catch (err) {
      setBirthChart(null);
    } finally {
      setCalculating(false);
    }
  };

  const getBirthChartRoast = async () => {
    if (!birthDate || !birthTime || !latitude || !longitude) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/birth-chart/roast?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}`);
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      setBirthChart(data.birth_chart);
      setRoast(data.roast);
    } catch (err) {
      setRoast("Error generating birth chart roast");
    } finally {
      setLoading(false);
    }
  };

  return React.createElement(
    "div",
    { className: "page" },
    React.createElement("h2", null, "Birth Chart Calculator"),
    
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("h3", null, "Enter Your Birth Details"),
      React.createElement("input", {
        type: "date",
        value: birthDate,
        onChange: (e) => setBirthDate(e.target.value),
        placeholder: "Birth Date",
      }),
      React.createElement("input", {
        type: "time",
        value: birthTime,
        onChange: (e) => setBirthTime(e.target.value),
        placeholder: "Birth Time",
      }),
      
      // Location input section
      React.createElement(
        "div",
        { className: "location-section" },
        React.createElement("h4", null, "Birth Location"),
        React.createElement(
          "div",
          { className: "location-toggle" },
          React.createElement(
            "button",
            {
              type: "button",
              className: useCitySearch ? "toggle-btn active" : "toggle-btn",
              onClick: () => setUseCitySearch(true)
            },
            "Search by City"
          ),
          React.createElement(
            "button",
            {
              type: "button",
              className: !useCitySearch ? "toggle-btn active" : "toggle-btn",
              onClick: () => setUseCitySearch(false)
            },
            "Enter Coordinates"
          )
        ),
        
        useCitySearch ? React.createElement(CitySearch, { onCitySelect: handleCitySelect }) : React.createElement(
          "div",
          { className: "coordinates-inputs" },
          React.createElement("input", {
            type: "number",
            step: "any",
            value: latitude,
            onChange: (e) => setLatitude(e.target.value),
            placeholder: "Latitude (e.g., 40.7128)",
          }),
          React.createElement("input", {
            type: "number",
            step: "any",
            value: longitude,
            onChange: (e) => setLongitude(e.target.value),
            placeholder: "Longitude (e.g., -74.0060)",
          })
        ),
        
        selectedCity && React.createElement(
          "div",
          { className: "selected-city" },
          React.createElement("p", null, `Selected: ${selectedCity.display_name}`),
          React.createElement("p", null, `Coordinates: ${selectedCity.latitude}, ${selectedCity.longitude}`)
        )
      ),
      
      React.createElement(
        "button",
        { onClick: calculateBirthChart, disabled: calculating || !birthDate || !birthTime || !latitude || !longitude },
        calculating ? "Calculating..." : "Calculate Birth Chart"
      ),
      React.createElement(
        "button",
        { onClick: getBirthChartRoast, disabled: loading || !birthDate || !birthTime || !latitude || !longitude },
        loading ? "Generating Roast..." : "Get Roasted Birth Chart"
      )
    ),

    // Display birth chart
    birthChart && React.createElement(
      "div",
      { className: "birth-chart-container" },
      React.createElement("h3", null, "Your Birth Chart"),
      React.createElement(
        "div",
        { className: "birth-chart-details" },
        React.createElement("h4", null, "Key Placements"),
        ...Object.entries(birthChart.planets || {}).map(([planet, data]) =>
          React.createElement(
            "div",
            { key: planet, className: "planet-placement" },
            React.createElement("span", { className: "planet-symbol" }, data.symbol),
            React.createElement("span", { className: "planet-name" }, planet),
            React.createElement("span", { className: "planet-sign" }, `${data.sign} ${data.sign_symbol}`),
            React.createElement("span", { className: "planet-degrees" }, data.formatted)
          )
        )
      ),
      birthChart.ascendant && React.createElement(
        "div",
        { className: "ascendant-info" },
        React.createElement("h4", null, "Ascendant (Rising Sign)"),
        React.createElement("p", null, `${birthChart.ascendant.sign} ${birthChart.ascendant.sign_symbol} - ${birthChart.ascendant.formatted}`)
      )
    ),
    
    loading && React.createElement("p", null, "Loading..."),
    roast && React.createElement(
      "div",
      { className: "roast-container" },
      React.createElement("h4", null, "Your Birth Chart Roast"),
      React.createElement("p", { className: "roast" }, roast)
    )
  );
}

function App() {
  const [currentPage, setCurrentPage] = useState("horoscope");

  return React.createElement(
    "div",
    { className: "container" },
    React.createElement("h1", null, "HoroscHope"),
    React.createElement(Navigation, { currentPage, onPageChange: setCurrentPage }),
    currentPage === "horoscope" 
      ? React.createElement(HoroscopePage)
      : React.createElement(BirthChartPage)
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  React.createElement(App)
);
