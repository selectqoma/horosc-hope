const { useState } = React;

// Language translations
const translations = {
  English: {
    // First page content
    pageTitle: "(brutally) Honest horoscope",
    signCalculator: "Sign Calculator",
    birthChartCalculator: "Birth Chart Calculator",
    enterBirthDate: "Enter your birth date",
    calculateSign: "Calculate Sign",
    calculating: "Calculating...",
    yourSign: "Your Sign",
    signDetails: "Sign Details",
    
    // Navigation
    home: "Home",
    birthChart: "Birth Chart",
    
    // Birth chart page
    enterBirthDetails: "Enter Your Birth Details",
    birthLocation: "Birth Location",
    searchByCity: "Search by City",
    enterCoordinates: "Enter Coordinates",
    latitude: "Latitude",
    longitude: "Longitude",
    selected: "Selected",
    language: "Language",
    calculateRoastChart: "Calculate & Roast Chart",
    generating: "Channeling...",
    generatingRoast: "Interpreting star patterns...",
    waitingForRoast: "Waiting for magic ball's response...",
    ascendant: "Ascendant",
    

    getHoroscopeRoast: "Get Your Honest Horoscope",
    enterSign: "Enter sign (or use calculated sign above)",
    getRoast: "Get Roast",
    loading: "Loading...",
    horoscope: "Horoscope",
    
    // Period options
    today: "Today",
    tomorrow: "Tomorrow",
    yesterday: "Yesterday",
    thisWeek: "This Week",
    thisMonth: "This Month",
    
    // Sign details labels
    element: "Element",
    quality: "Quality",
    ruler: "Ruler",
    dates: "Dates",
    traits: "Traits",
    
    // City search
    searchBirthCity: "Search for your birth city...",
    searching: "Searching...",
    
    // Error messages
    errorCalculatingSign: "Error calculating sign",
    errorFetchingRoast: "Error fetching roast",
    
    // Chart labels
    birthChartWheel: "Birth Chart Wheel",
    house: "House",
    in: "in",
    
    // Roast categories
    love: "Love",
    work: "Work", 
    social: "Social Life",
    overall: "Overall",
    
    // Zodiac signs
    selectSign: "Select a zodiac sign",
    zodiacSigns: {
      aries: "Aries",
      taurus: "Taurus", 
      gemini: "Gemini",
      cancer: "Cancer",
      leo: "Leo",
      virgo: "Virgo",
      libra: "Libra",
      scorpio: "Scorpio",
      sagittarius: "Sagittarius",
      capricorn: "Capricorn",
      aquarius: "Aquarius",
      pisces: "Pisces"
    }
  },
  French: {
    // First page content
    pageTitle: "Horoscope (un peu trop) Honnête",
    signCalculator: "Calculateur de Signe",
    birthChartCalculator: "Calculateur de Thème Astral",
    enterBirthDate: "Entrez votre date de naissance",
    calculateSign: "Calculer le Signe",
    calculating: "Calcul...",
    yourSign: "Votre Signe",
    signDetails: "Détails du Signe",
    
    // Navigation
    home: "Accueil",
    birthChart: "Thème Astral",
    
    // Birth chart page
    enterBirthDetails: "Entrez vos détails de naissance",
    birthLocation: "Lieu de naissance",
    searchByCity: "Rechercher par ville",
    enterCoordinates: "Entrer les coordonnées",
    latitude: "Latitude",
    longitude: "Longitude",
    selected: "Sélectionné",
    language: "Langue",
    calculateRoastChart: "Calculer",
    generating: "Génération...",
    generatingRoast: "Lecture des étoiles...",
    waitingForRoast: "En attente d'une réponse de la boule de cristal...",
    ascendant: "Ascendant",
    
    // Horoscope roast section
    getHoroscopeRoast: "Obtenez votre Horoscope Honnête",
    enterSign: "Entrez le signe (ou utilisez le signe calculé ci-dessus)",
    getRoast: "Calculer",
    loading: "Chargement...",
    horoscope: "Horoscope",
    
    // Period options
    today: "Aujourd'hui",
    tomorrow: "Demain",
    yesterday: "Hier",
    thisWeek: "Cette Semaine",
    thisMonth: "Ce Mois",
    
    // Sign details labels
    element: "Élément",
    quality: "Qualité",
    ruler: "Maître",
    dates: "Dates",
    traits: "Traits",
    
    // City search
    searchBirthCity: "Recherchez votre ville de naissance...",
    searching: "Recherche...",
    
    // Error messages
    errorCalculatingSign: "Erreur de calcul du signe",
    errorFetchingRoast: "Erreur lors de la lecture des étoiles",
    
    // Chart labels
    birthChartWheel: "Roue du Thème Astral",
    house: "Maison",
    in: "en",
    
    // Roast categories
    love: "Amour",
    work: "Travail",
    social: "Vie Sociale", 
    overall: "Global",
    
    // Zodiac signs
    selectSign: "Sélectionnez un signe du zodiaque",
    zodiacSigns: {
      aries: "Bélier",
      taurus: "Taureau", 
      gemini: "Gémeaux",
      cancer: "Cancer",
      leo: "Lion",
      virgo: "Vierge",
      libra: "Balance",
      scorpio: "Scorpion",
      sagittarius: "Sagittaire",
      capricorn: "Capricorne",
      aquarius: "Verseau",
      pisces: "Poissons"
    }
  },
  Russian: {
    // First page content
    pageTitle: "Гороскоп без фильтров",
    signCalculator: "Узнайте свой знак",
    birthChartCalculator: "Посчитайте свою Натальную Карту",
    enterBirthDate: "Введите дату рождения",
    calculateSign: "Рассчитать знак",
    calculating: "Расчет...",
    yourSign: "Ваш Знак",
    signDetails: "Детали Знака",
    
    // Navigation
    home: "Главная",
    birthChart: "Натальная Карта",
    
    // Birth chart page
    enterBirthDetails: "Введите данные о вашем рождении",
    birthLocation: "Место рождения",
    searchByCity: "Поиск по городу",
    enterCoordinates: "Ввести координаты",
    latitude: "Широта",
    longitude: "Долгота",
    selected: "Выбрано",
    language: "Язык",
    calculateRoastChart: "Рассчитать карту",
    generating: "Генерация...",
    generatingRoast: "Чтение звездных знаков...",
    waitingForRoast: "Ожидание ответа от магического шара...",
    ascendant: "Асцендент",
    
    // Horoscope roast section
    getHoroscopeRoast: "Гороскоп без фильтров",
    enterSign: "Введите знак (или используйте рассчитанный знак выше)",
    getRoast: "Скажи мне все как есть",
    loading: "Загрузка...",
    horoscope: "Гороскоп",
    
    // Period options
    today: "Сегодня",
    tomorrow: "Завтра",
    yesterday: "Вчера",
    thisWeek: "На неделю",
    thisMonth: "На месяц",
    
    // Sign details labels
    element: "Элемент",
    quality: "Качество",
    ruler: "Управитель",
    dates: "Даты",
    traits: "Черты",
    
    // City search
    searchBirthCity: "Найдите свой город рождения...",
    searching: "Поиск...",
    
    // Error messages
    errorCalculatingSign: "Ошибка расчета знака",
    errorFetchingRoast: "Ошибка чтения звездных знаков",
    
    // Chart labels
    birthChartWheel: "Натальная Карта",
    house: "Дом",
    in: "в",
    
    // Roast categories
    love: "Любовь",
    work: "Работа",
    social: "Социальная Жизнь",
    overall: "Общее",
    
    // Zodiac signs
    selectSign: "Выберите знак зодиака",
    zodiacSigns: {
      aries: "Овен",
      taurus: "Телец", 
      gemini: "Близнецы",
      cancer: "Рак",
      leo: "Лев",
      virgo: "Дева",
      libra: "Весы",
      scorpio: "Скорпион",
      sagittarius: "Стрелец",
      capricorn: "Козерог",
      aquarius: "Водолей",
      pisces: "Рыбы"
    }
  }
};

// Mapping from translated sign names back to English for API calls
const signMapping = {
  // English
  "Aries": "Aries", "Taurus": "Taurus", "Gemini": "Gemini", "Cancer": "Cancer",
  "Leo": "Leo", "Virgo": "Virgo", "Libra": "Libra", "Scorpio": "Scorpio", 
  "Sagittarius": "Sagittarius", "Capricorn": "Capricorn", "Aquarius": "Aquarius", "Pisces": "Pisces",
  // French
  "Bélier": "Aries", "Taureau": "Taurus", "Gémeaux": "Gemini", "Cancer": "Cancer",
  "Lion": "Leo", "Vierge": "Virgo", "Balance": "Libra", "Scorpion": "Scorpio",
  "Sagittaire": "Sagittarius", "Capricorne": "Capricorn", "Verseau": "Aquarius", "Poissons": "Pisces",
  // Russian
  "Овен": "Aries", "Телец": "Taurus", "Близнецы": "Gemini", "Рак": "Cancer",
  "Лев": "Leo", "Дева": "Virgo", "Весы": "Libra", "Скорпион": "Scorpio",
  "Стрелец": "Sagittarius", "Козерог": "Capricorn", "Водолей": "Aquarius", "Рыбы": "Pisces"
};

function Navigation({ currentPage, onPageChange, t }) {
  return React.createElement(
    "nav",
    { className: "navigation" },
    React.createElement(
      "button",
      {
        className: currentPage === "home" ? "nav-btn active" : "nav-btn",
        onClick: () => onPageChange("home")
      },
      t.home
    ),
    React.createElement(
      "button",
      {
        className: currentPage === "birth-chart" ? "nav-btn active" : "nav-btn",
        onClick: () => onPageChange("birth-chart")
      },
      t.birthChart
    )
  );
}

function HoroscopePage({ t, selectedLanguage }) {
  const [birthDate, setBirthDate] = useState(() => {
    try {
      return localStorage.getItem("horoscope-birth-date") || "";
    } catch (error) {
      return "";
    }
  });
  const [sign, setSign] = useState(() => {
    try {
      return localStorage.getItem("horoscope-sign") || "";
    } catch (error) {
      return "";
    }
  });
  const [displaySign, setDisplaySign] = useState(() => {
    try {
      return localStorage.getItem("horoscope-display-sign") || "";
    } catch (error) {
      return "";
    }
  });
  const [loading, setLoading] = useState(false);
  const [roast, setRoast] = useState(() => {
    try {
      return localStorage.getItem("horoscope-roast") || "";
    } catch (error) {
      return "";
    }
  });
  const [selectedPeriod, setSelectedPeriod] = useState(() => {
    try {
      return localStorage.getItem("horoscope-period") || "daily";
    } catch (error) {
      return "daily";
    }
  });
  const [signInfo, setSignInfo] = useState(() => {
    try {
      const saved = localStorage.getItem("horoscope-sign-info");
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      return null;
    }
  });

  const periodOptions = [
    { value: "daily", label: t.today },
    { value: "tomorrow", label: t.tomorrow },
    { value: "yesterday", label: t.yesterday },
    { value: "weekly", label: t.thisWeek },
    { value: "monthly", label: t.thisMonth }
  ];

  // Persistence helpers
  const saveBirthDate = (date) => {
    setBirthDate(date);
    try {
      localStorage.setItem("horoscope-birth-date", date);
    } catch (error) {
      console.warn("Could not save birth date:", error);
    }
  };

  const saveSign = (newSign) => {
    setSign(newSign);
    try {
      localStorage.setItem("horoscope-sign", newSign);
    } catch (error) {
      console.warn("Could not save sign:", error);
    }
  };

  const saveDisplaySign = (newDisplaySign) => {
    setDisplaySign(newDisplaySign);
    try {
      localStorage.setItem("horoscope-display-sign", newDisplaySign);
    } catch (error) {
      console.warn("Could not save display sign:", error);
    }
  };

  const handleSignSelection = (selectedDisplaySign) => {
    const apiSign = signMapping[selectedDisplaySign] || selectedDisplaySign;
    saveSign(apiSign);
    saveDisplaySign(selectedDisplaySign);
  };

  const saveSignInfo = (info) => {
    setSignInfo(info);
    try {
      localStorage.setItem("horoscope-sign-info", JSON.stringify(info));
    } catch (error) {
      console.warn("Could not save sign info:", error);
    }
  };

  const saveRoast = (newRoast) => {
    setRoast(newRoast);
    try {
      localStorage.setItem("horoscope-roast", newRoast);
    } catch (error) {
      console.warn("Could not save roast:", error);
    }
  };

  const savePeriod = (period) => {
    setSelectedPeriod(period);
    try {
      localStorage.setItem("horoscope-period", period);
    } catch (error) {
      console.warn("Could not save period:", error);
    }
  };

  const calculateSign = async () => {
    if (!birthDate) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/calculate-sign/${birthDate}`);
      if (!res.ok) throw new Error("Failed to calculate sign");
      const data = await res.json();
      saveSign(data.zodiac_sign);
      saveDisplaySign(data.zodiac_sign); // Use English name as display for calculated signs
      saveSignInfo(data.sign_info);
    } catch (err) {
      saveSign(t.errorCalculatingSign);
      saveSignInfo(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchRoast = async () => {
    if (!sign) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/horoscope/${sign}?period=${selectedPeriod}&language=${selectedLanguage}`);
      if (!res.ok) throw new Error("Failed to fetch roast");
      const data = await res.json();
      saveRoast(data.roast);
    } catch (err) {
      saveRoast(t.errorFetchingRoast);
    } finally {
      setLoading(false);
    }
  };

  // Listen for horoscope refresh events
  React.useEffect(() => {
    const handleHoroscopeRefresh = (event) => {
      setRoast(event.detail);
    };

    const handleHoroscopeReset = () => {
      // Reset input selections
      setSign("");
      setDisplaySign("");
      setSelectedPeriod("daily");
      // Reset outputs
      setRoast(null);
      setSignInfo(null);
      // Reset loading state
      setLoading(false);
    };

    window.addEventListener('horoscopeRefresh', handleHoroscopeRefresh);
    window.addEventListener('horoscopeReset', handleHoroscopeReset);
    return () => {
      window.removeEventListener('horoscopeRefresh', handleHoroscopeRefresh);
      window.removeEventListener('horoscopeReset', handleHoroscopeReset);
    };
  }, []);

  return React.createElement(
    "div",
    { className: "page" },
    React.createElement("h2", null, t.signCalculator),
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("h3", null, t.enterBirthDate),
      React.createElement("input", {
        type: "date",
        value: birthDate,
        onChange: (e) => saveBirthDate(e.target.value),
        placeholder: t.enterBirthDate,
      }),
      React.createElement("button", {
        onClick: calculateSign,
        disabled: loading || !birthDate,
      }, loading ? t.calculating : t.calculateSign)
    ),
    signInfo && React.createElement(
      "div",
      { className: "sign-info" },
      React.createElement("h3", null, t.yourSign),
      React.createElement(
        "div",
        { className: "sign-details" },
        React.createElement("p", null, `${t.element}: ${signInfo.element}`),
        React.createElement("p", null, `${t.quality}: ${signInfo.quality}`),
        React.createElement("p", null, `${t.ruler}: ${signInfo.ruler}`),
        React.createElement("p", null, `${t.dates}: ${signInfo.dates}`),
        React.createElement("p", null, `${t.traits}: ${signInfo.traits.join(", ")}`)
      )
    ),

    // Manual Sign Input Section
    React.createElement(
      "div",
      { className: "form" },
      React.createElement("h3", null, t.getHoroscopeRoast),
      React.createElement(
        "select",
        {
          value: displaySign,
          onChange: (e) => handleSignSelection(e.target.value),
          className: "sign-selector"
        },
        React.createElement("option", { value: "" }, t.selectSign),
        ...Object.entries(t.zodiacSigns).map(([key, signName]) =>
          React.createElement("option", {
            key: key,
            value: signName
          }, signName)
        )
      ),
      React.createElement(
        "select",
        {
          value: selectedPeriod,
          onChange: (e) => savePeriod(e.target.value),
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
        loading ? t.loading : t.getRoast
      )
    ),
    
    loading && React.createElement("p", null, t.loading),
    roast && React.createElement(
      "div",
      { className: "roast-container" },
      React.createElement("h4", null, `${periodOptions.find(p => p.value === selectedPeriod)?.label} ${t.horoscope}`),
      typeof roast === 'string' ? 
        React.createElement("p", { className: "roast" }, roast) :
        React.createElement(
          "div",
          { className: "categorized-roasts" },
          React.createElement(
            "div",
            { className: "roast-category overall-category" },
            React.createElement("h5", null, t.overall),
            React.createElement("p", { className: "roast overall-roast" }, roast.overall)
          ),
          React.createElement(
            "div",
            { className: "roast-category" },
            React.createElement("h5", null, t.love),
            React.createElement("p", { className: "roast" }, roast.love)
          ),
          React.createElement(
            "div",
            { className: "roast-category" },
            React.createElement("h5", null, t.work),
            React.createElement("p", { className: "roast" }, roast.work)
          ),
          React.createElement(
            "div",
            { className: "roast-category" },
            React.createElement("h5", null, t.social),
            React.createElement("p", { className: "roast" }, roast.social)
          )
        )
    )
  );
}

function CitySearch({ onCitySelect, t }) {
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
      placeholder: t.searchBirthCity,
      className: "city-search-input"
    }),
    loading && React.createElement("p", { className: "search-loading" }, t.searching),
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

function BirthChartPage({ t, selectedLanguage }) {
  const [birthDate, setBirthDate] = useState(() => {
    try {
      return localStorage.getItem("chart-birth-date") || "";
    } catch (error) {
      return "";
    }
  });
  const [birthTime, setBirthTime] = useState(() => {
    try {
      return localStorage.getItem("chart-birth-time") || "";
    } catch (error) {
      return "";
    }
  });
  const [selectedCity, setSelectedCity] = useState(() => {
    try {
      const saved = localStorage.getItem("chart-selected-city");
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      return null;
    }
  });
  const [latitude, setLatitude] = useState(() => {
    try {
      return localStorage.getItem("chart-latitude") || "";
    } catch (error) {
      return "";
    }
  });
  const [longitude, setLongitude] = useState(() => {
    try {
      return localStorage.getItem("chart-longitude") || "";
    } catch (error) {
      return "";
    }
  });
  const [birthChart, setBirthChart] = useState(() => {
    try {
      const saved = localStorage.getItem("chart-birth-chart");
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      return null;
    }
  });
  const [chartImageUrl, setChartImageUrl] = useState(() => {
    try {
      return localStorage.getItem("chart-image-url") || "";
    } catch (error) {
      return "";
    }
  });
  const [placementRoasts, setPlacementRoasts] = useState(() => {
    try {
      const saved = localStorage.getItem("chart-placement-roasts");
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      return null;
    }
  });
  const [loading, setLoading] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [useCitySearch, setUseCitySearch] = useState(() => {
    try {
      const saved = localStorage.getItem("chart-use-city-search");
      return saved ? JSON.parse(saved) : true;
    } catch (error) {
      return true;
    }
  });

  // Get current translations
  const tCurrent = translations[selectedLanguage];

  // Mock data for initial display
  const mockChartUrl = "http://localhost:8000/birth-chart/plot?birth_date=1990-06-15&birth_time=12:00&latitude=40.7128&longitude=-74.0060&t=mock";

  const mockPlacements = [
    { symbol: "☉", name: "Sun", sign: "Gemini", degrees: "24.3°" },
    { symbol: "☽", name: "Moon", sign: "Cancer", degrees: "8.7°" },
    { symbol: "☿", name: "Mercury", sign: "Gemini", degrees: "15.2°" },
    { symbol: "♀", name: "Venus", sign: "Taurus", degrees: "12.8°" },
    { symbol: "♂", name: "Mars", sign: "Leo", degrees: "3.4°" },
    { symbol: "♃", name: "Jupiter", sign: "Cancer", degrees: "22.1°" },
    { symbol: "♄", name: "Saturn", sign: "Capricorn", degrees: "18.9°" },
    { symbol: "♅", name: "Uranus", sign: "Capricorn", degrees: "7.6°" },
    { symbol: "♆", name: "Neptune", sign: "Capricorn", degrees: "14.2°" },
    { symbol: "♇", name: "Pluto", sign: "Scorpio", degrees: "11.8°" }
  ];

  const languages = [
    { value: "English", label: "English" },
    { value: "French", label: "Français" },
    { value: "Russian", label: "Русский" }
  ];

  // Chart persistence helpers
  const saveChartBirthDate = (date) => {
    setBirthDate(date);
    try {
      localStorage.setItem("chart-birth-date", date);
    } catch (error) {
      console.warn("Could not save chart birth date:", error);
    }
  };

  const saveChartBirthTime = (time) => {
    setBirthTime(time);
    try {
      localStorage.setItem("chart-birth-time", time);
    } catch (error) {
      console.warn("Could not save chart birth time:", error);
    }
  };

  const saveChartSelectedCity = (city) => {
    setSelectedCity(city);
    try {
      localStorage.setItem("chart-selected-city", JSON.stringify(city));
    } catch (error) {
      console.warn("Could not save selected city:", error);
    }
  };

  const saveChartLatitude = (lat) => {
    setLatitude(lat);
    try {
      localStorage.setItem("chart-latitude", lat);
    } catch (error) {
      console.warn("Could not save latitude:", error);
    }
  };

  const saveChartLongitude = (lng) => {
    setLongitude(lng);
    try {
      localStorage.setItem("chart-longitude", lng);
    } catch (error) {
      console.warn("Could not save longitude:", error);
    }
  };

  const saveChartBirthChart = (chart) => {
    setBirthChart(chart);
    try {
      localStorage.setItem("chart-birth-chart", JSON.stringify(chart));
    } catch (error) {
      console.warn("Could not save birth chart:", error);
    }
  };

  const saveChartImageUrl = (url) => {
    setChartImageUrl(url);
    try {
      localStorage.setItem("chart-image-url", url);
    } catch (error) {
      console.warn("Could not save chart image URL:", error);
    }
  };

  const saveChartPlacementRoasts = (roasts) => {
    setPlacementRoasts(roasts);
    try {
      localStorage.setItem("chart-placement-roasts", JSON.stringify(roasts));
    } catch (error) {
      console.warn("Could not save placement roasts:", error);
    }
  };

  const saveUseCitySearch = (useCity) => {
    setUseCitySearch(useCity);
    try {
      localStorage.setItem("chart-use-city-search", JSON.stringify(useCity));
    } catch (error) {
      console.warn("Could not save city search preference:", error);
    }
  };

  const handleCitySelect = (city) => {
    saveChartSelectedCity(city);
    saveChartLatitude(city.latitude);
    saveChartLongitude(city.longitude);
  };

  const calculateBirthChart = async () => {
    if (!birthDate || !birthTime || !latitude || !longitude) return;
    setCalculating(true);
    saveChartPlacementRoasts(null);
    try {
      const res = await fetch(`http://localhost:8000/birth-chart?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}`);
      if (!res.ok) throw new Error("Failed to calculate birth chart");
      const data = await res.json();
      saveChartBirthChart(data);
      const imageUrl = `http://localhost:8000/birth-chart/plot?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}&t=${new Date().getTime()}`;
      saveChartImageUrl(imageUrl);
    } catch (err) {
      saveChartBirthChart(null);
      saveChartImageUrl("");
    } finally {
      setCalculating(false);
    }
  };

  const getPlacementRoasts = async () => {
    if (!birthDate || !birthTime || !latitude || !longitude) return;
    setLoading(true);
    saveChartBirthChart(null);
    saveChartImageUrl("");
    saveChartPlacementRoasts({});
    
    try {
      // First get the birth chart
      const chartRes = await fetch(`http://localhost:8000/birth-chart?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}`);
      if (!chartRes.ok) throw new Error("Failed to get birth chart");
      const chartData = await chartRes.json();
      saveChartBirthChart(chartData);
      
      // Generate chart image URL
      const imageUrl = `http://localhost:8000/birth-chart/plot?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}&t=${new Date().getTime()}`;
      saveChartImageUrl(imageUrl);
      
      // Now stream the roasts with language parameter
      const roastRes = await fetch(`http://localhost:8000/birth-chart/roast-placements?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}&language=${selectedLanguage}`);
      if (!roastRes.ok) throw new Error("Failed to get roasts");
      
      const reader = roastRes.body.getReader();
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.complete) {
                // All roasts are done
                saveChartPlacementRoasts(data.all_roasts);
                setLoading(false);
                return;
              } else if (data.planet && data.roast) {
                // Update roasts as they come in
                setPlacementRoasts(prev => {
                  const newRoasts = {
                    ...prev,
                    [data.planet]: data.roast
                  };
                  // Save to localStorage
                  try {
                    localStorage.setItem("chart-placement-roasts", JSON.stringify(newRoasts));
                  } catch (error) {
                    console.warn("Could not save placement roasts:", error);
                  }
                  return newRoasts;
                });
              }
            } catch (e) {
              console.error('Error parsing stream data:', e);
            }
          }
        }
      }
      
    } catch (err) {
      console.error("Failed to get placement roasts:", err);
      setLoading(false);
    }
  };

  // Listen for chart roasts refresh events
  React.useEffect(() => {
    const handleChartRoastsRefresh = (event) => {
      setPlacementRoasts(event.detail);
    };

    const handleChartReset = () => {
      // Reset input fields
      setBirthDate("");
      setBirthTime("");
      setSelectedCity(null);
      setLatitude("");
      setLongitude("");
      setUseCitySearch(true);
      // Reset output data
      setBirthChart(null);
      setChartImageUrl("");
      setPlacementRoasts({});
      // Reset loading states
      setCalculating(false);
      setLoading(false);
    };

    window.addEventListener('chartRoastsRefresh', handleChartRoastsRefresh);
    window.addEventListener('chartReset', handleChartReset);
    return () => {
      window.removeEventListener('chartRoastsRefresh', handleChartRoastsRefresh);
      window.removeEventListener('chartReset', handleChartReset);
    };
  }, []);

  // Main render
  return React.createElement(
    "div",
    { className: "page" },
    
    React.createElement(
      "div",
      { className: "chart-layout-container" },
      
      // --- Left Column: Inputs ---
      React.createElement(
        "div",
        { className: "input-column" },
        React.createElement("h3", null, tCurrent.enterBirthDetails),
        React.createElement("input", { type: "date", value: birthDate, onChange: (e) => saveChartBirthDate(e.target.value) }),
        React.createElement("input", { type: "time", value: birthTime, onChange: (e) => saveChartBirthTime(e.target.value) }),
        
        React.createElement(
          "div", { className: "location-section" },
          React.createElement("h4", null, tCurrent.birthLocation),
          React.createElement("div", { className: "location-toggle" },
            React.createElement("button", { type: "button", className: useCitySearch ? "toggle-btn active" : "toggle-btn", onClick: () => saveUseCitySearch(true) }, tCurrent.searchByCity),
            React.createElement("button", { type: "button", className: !useCitySearch ? "toggle-btn active" : "toggle-btn", onClick: () => saveUseCitySearch(false) }, tCurrent.enterCoordinates)
          ),
          useCitySearch ? React.createElement(CitySearch, { onCitySelect: handleCitySelect, t: tCurrent }) : React.createElement(
            "div", { className: "coordinates-inputs" },
            React.createElement("input", { type: "number", step: "any", value: latitude, onChange: (e) => saveChartLatitude(e.target.value), placeholder: tCurrent.latitude }),
            React.createElement("input", { type: "number", step: "any", value: longitude, onChange: (e) => saveChartLongitude(e.target.value), placeholder: tCurrent.longitude })
          ),
          selectedCity && React.createElement("div", { className: "selected-city" },
            React.createElement("p", null, `${tCurrent.selected}: ${selectedCity.display_name}`)
          )
        ),
        
        React.createElement("button", { onClick: getPlacementRoasts, disabled: loading || calculating || !birthDate || !birthTime || !latitude || !longitude },
          loading ? tCurrent.generating : tCurrent.calculateRoastChart
        )
      ),

      // --- Right Column: Chart Image ---
      React.createElement(
        "div",
        { className: "chart-column" },
        React.createElement(
          "div",
          { className: "chart-image-container" },
          React.createElement("img", { 
            src: chartImageUrl || mockChartUrl, 
            alt: tCurrent.birthChartWheel, 
            className: "chart-image" 
          })
        ),
        (calculating || loading) && React.createElement("div", { className: "chart-placeholder" }, React.createElement("p", null, tCurrent.calculating))
      )
    ),

    // --- Horizontal Row: Key Placements (2 rows of 5) ---
    React.createElement(
      "div",
      { className: "placements-row" },
      birthChart ? 
        // Real placements - split into 2 rows of 5
        React.createElement(
          "div",
          { className: "placements-grid" },
          // First row
          React.createElement(
            "div",
            { className: "placements-row-1" },
            Object.entries(birthChart.planets || {}).slice(0, 5).map(([planet, data]) =>
              React.createElement(
                "div", { key: planet, className: "planet-placement" },
                React.createElement("span", { className: "planet-symbol" }, data.symbol),
                React.createElement("span", { className: "planet-sign" }, data.sign),
                React.createElement("span", { className: "planet-degrees" }, `${data.sign_degrees.toFixed(1)}°`)
              )
            )
          ),
          // Second row
          React.createElement(
            "div",
            { className: "placements-row-2" },
            Object.entries(birthChart.planets || {}).slice(5, 10).map(([planet, data]) =>
              React.createElement(
                "div", { key: planet, className: "planet-placement" },
                React.createElement("span", { className: "planet-symbol" }, data.symbol),
                React.createElement("span", { className: "planet-sign" }, data.sign),
                React.createElement("span", { className: "planet-degrees" }, `${data.sign_degrees.toFixed(1)}°`)
              )
            )
          )
        )
      :
        // Mock placements - split into 2 rows of 5
        React.createElement(
          "div",
          { className: "placements-grid" },
          // First row
          React.createElement(
            "div",
            { className: "placements-row-1" },
            mockPlacements.slice(0, 5).map((placement, index) =>
              React.createElement(
                "div", { key: index, className: "planet-placement mock" },
                React.createElement("span", { className: "planet-symbol" }, placement.symbol),
                React.createElement("span", { className: "planet-sign" }, placement.sign),
                React.createElement("span", { className: "planet-degrees" }, placement.degrees)
              )
            )
          ),
          // Second row
          React.createElement(
            "div",
            { className: "placements-row-2" },
            mockPlacements.slice(5, 10).map((placement, index) =>
              React.createElement(
                "div", { key: index + 5, className: "planet-placement mock" },
                React.createElement("span", { className: "planet-symbol" }, placement.symbol),
                React.createElement("span", { className: "planet-sign" }, placement.sign),
                React.createElement("span", { className: "planet-degrees" }, placement.degrees)
              )
            )
          )
        ),
      birthChart && birthChart.ascendant && React.createElement(
        "div", { className: "ascendant-info" },
        React.createElement("h4", null, tCurrent.ascendant),
        React.createElement("p", null, `${birthChart.ascendant.sign} - ${birthChart.ascendant.formatted}`)
      )
    ),

    // --- Below: Detailed Roasts ---
    (loading || Object.keys(placementRoasts || {}).length > 0) && React.createElement(
      "div",
      { className: "placement-roasts-container" },
      
      // Overall Synthesis (First)
      placementRoasts?.overall_synthesis && React.createElement(
        "div", { key: "overall_synthesis", className: "roast-item synthesis-item" },
        React.createElement("h4", { className: "roast-title synthesis-title" }, tCurrent.overall),
        React.createElement("p", { className: "roast-text synthesis-roast" }, placementRoasts.overall_synthesis)
      ),
      
      // Individual Planet Roasts
      birthChart && Object.entries(birthChart.planets || {}).map(([planet, planetData]) => {
        const roast = placementRoasts?.[planet];
        const isGenerating = loading && !roast;
        
        return React.createElement(
          "div", { key: planet, className: "roast-item" },
          React.createElement("h4", { className: "roast-title" }, 
            React.createElement("span", { className: "planet-symbol" }, planetData.symbol),
            `${planetData.name} ${tCurrent.in} ${planetData.sign} (${planetData.house}${selectedLanguage === "English" ? "th" : ""} ${tCurrent.house})`
          ),
          isGenerating ? 
            React.createElement("p", { className: "roast-text loading-roast" }, tCurrent.generatingRoast) :
            React.createElement("p", { className: "roast-text" }, roast || tCurrent.waitingForRoast)
        );
      })
    )
  );
}

function App() {
  const [currentPage, setCurrentPage] = useState(() => {
    // Load current page from localStorage or default to home
    try {
      return localStorage.getItem("horoscope-current-page") || "home";
    } catch (error) {
      return "home";
    }
  });
  const [selectedLanguage, setSelectedLanguage] = useState(() => {
    // Load language from localStorage or default to English
    try {
      return localStorage.getItem("horoscope-language") || "English";
    } catch (error) {
      return "English";
    }
  });
  
  // Get current translations
  const t = translations[selectedLanguage];

  const languages = [
    { value: "English", label: "English" },
    { value: "French", label: "Français" },
    { value: "Russian", label: "Русский" }
  ];

  // Handle page change and persist to localStorage
  const handlePageChange = (newPage) => {
    const previousPage = currentPage;
    setCurrentPage(newPage);
    try {
      localStorage.setItem("horoscope-current-page", newPage);
    } catch (error) {
      console.warn("Could not save current page to localStorage:", error);
    }
    
    // Trigger refresh when switching pages
    if (previousPage !== newPage) {
      // Use a small delay to ensure page has switched
      setTimeout(() => {
        triggerPageSwitchRefresh(newPage);
      }, 100);
    }
  };

  // Function to reset/clear data when switching pages
  const triggerPageSwitchRefresh = (newPage) => {
    if (newPage === "home") {
      // Clear horoscope inputs and outputs
      try {
        // Clear input selections
        localStorage.removeItem("horoscope-sign");
        localStorage.removeItem("horoscope-display-sign");
        localStorage.removeItem("horoscope-period");
        // Clear outputs
        localStorage.removeItem("horoscope-roast");
        localStorage.removeItem("horoscope-sign-info");
        // Trigger a reset by dispatching a custom event
        window.dispatchEvent(new CustomEvent('horoscopeReset'));
      } catch (error) {
        console.warn("Could not clear horoscope data:", error);
      }
    } else if (newPage === "birth-chart") {
      // Clear birth chart inputs and outputs
      try {
        // Clear input fields
        localStorage.removeItem("chart-birth-date");
        localStorage.removeItem("chart-birth-time");
        localStorage.removeItem("chart-selected-city");
        localStorage.removeItem("chart-latitude");
        localStorage.removeItem("chart-longitude");
        localStorage.removeItem("chart-use-city-search");
        // Clear output data
        localStorage.removeItem("chart-birth-chart");
        localStorage.removeItem("chart-image-url");
        localStorage.removeItem("chart-placement-roasts");
        // Trigger a reset by dispatching a custom event
        window.dispatchEvent(new CustomEvent('chartReset'));
      } catch (error) {
        console.warn("Could not clear birth chart data:", error);
      }
    }
  };

  // Handle language change and persist to localStorage
  const handleLanguageChange = (newLanguage) => {
    const previousLanguage = selectedLanguage;
    setSelectedLanguage(newLanguage);
    try {
      localStorage.setItem("horoscope-language", newLanguage);
    } catch (error) {
      console.warn("Could not save language preference to localStorage:", error);
    }
    
    // Trigger refresh of any existing data when language changes
    if (previousLanguage !== newLanguage) {
      // Use a small delay to ensure state has updated
      setTimeout(() => {
        triggerLanguageRefresh(newLanguage);
      }, 100);
    }
  };

  // Function to refresh data when language changes
  const triggerLanguageRefresh = (newLanguage) => {
    // Refresh horoscope roast if there's a sign selected
    const currentSign = localStorage.getItem("horoscope-sign");
    const currentPeriod = localStorage.getItem("horoscope-period") || "daily";
    if (currentSign) {
      refreshHoroscopeRoast(currentSign, currentPeriod, newLanguage);
    }
    
    // Refresh birth chart roasts if there's chart data
    const chartData = localStorage.getItem("chart-birth-chart");
    if (chartData) {
      try {
        const chart = JSON.parse(chartData);
        const birthDate = localStorage.getItem("chart-birth-date");
        const birthTime = localStorage.getItem("chart-birth-time");
        const latitude = localStorage.getItem("chart-latitude");
        const longitude = localStorage.getItem("chart-longitude");
        
        if (birthDate && birthTime && latitude && longitude) {
          refreshBirthChartRoasts(birthDate, birthTime, latitude, longitude, newLanguage);
        }
      } catch (error) {
        console.warn("Could not parse chart data for refresh:", error);
      }
    }
  };

  // Function to refresh horoscope roast
  const refreshHoroscopeRoast = async (sign, period, language) => {
    try {
      const res = await fetch(`http://localhost:8000/horoscope/${sign}?period=${period}&language=${language}`);
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("horoscope-roast", JSON.stringify(data.roast));
        // Trigger a re-render by dispatching a custom event
        window.dispatchEvent(new CustomEvent('horoscopeRefresh', { detail: data.roast }));
      }
    } catch (error) {
      console.warn("Could not refresh horoscope roast:", error);
    }
  };

  // Function to refresh birth chart roasts
  const refreshBirthChartRoasts = async (birthDate, birthTime, latitude, longitude, language) => {
    try {
      const res = await fetch(`http://localhost:8000/birth-chart/roast-placements?birth_date=${birthDate}&birth_time=${birthTime}&latitude=${latitude}&longitude=${longitude}&language=${language}`);
      if (res.ok) {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let newRoasts = {};
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.complete) {
                  localStorage.setItem("chart-placement-roasts", JSON.stringify(data.all_roasts));
                  window.dispatchEvent(new CustomEvent('chartRoastsRefresh', { detail: data.all_roasts }));
                  return;
                } else if (data.planet && data.roast) {
                  newRoasts[data.planet] = data.roast;
                  localStorage.setItem("chart-placement-roasts", JSON.stringify(newRoasts));
                  window.dispatchEvent(new CustomEvent('chartRoastsRefresh', { detail: newRoasts }));
                }
              } catch (e) {
                console.error('Error parsing refresh stream data:', e);
              }
            }
          }
        }
      }
    } catch (error) {
      console.warn("Could not refresh birth chart roasts:", error);
    }
  };

  // Load preferences on component mount
  React.useEffect(() => {
    try {
      const savedLanguage = localStorage.getItem("horoscope-language");
      if (savedLanguage && translations[savedLanguage]) {
        setSelectedLanguage(savedLanguage);
      }
      
      const savedPage = localStorage.getItem("horoscope-current-page");
      if (savedPage && (savedPage === "home" || savedPage === "birth-chart")) {
        setCurrentPage(savedPage);
      }
    } catch (error) {
      console.warn("Could not load preferences from localStorage:", error);
    }
  }, []);

  return React.createElement(
    "div",
    { className: "container" },
    
    // Language selector at the very top
    React.createElement(
      "div",
      { className: "top-language-selector" },
      React.createElement(
        "select", 
        { 
          value: selectedLanguage, 
          onChange: (e) => handleLanguageChange(e.target.value),
          className: "global-language-selector"
        },
        languages.map(lang => 
          React.createElement("option", { key: lang.value, value: lang.value }, lang.label)
        )
      )
    ),
    
    React.createElement("h1", null, t.pageTitle),
    React.createElement(Navigation, { currentPage, onPageChange: handlePageChange, t }),
    
    currentPage === "home" && React.createElement(HoroscopePage, { t, selectedLanguage }),
    currentPage === "birth-chart" && React.createElement(BirthChartPage, { t, selectedLanguage })
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  React.createElement(App)
);
