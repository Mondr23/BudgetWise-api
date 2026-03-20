import { useEffect, useState, useRef } from "react"
import axios from "axios"
import { motion, AnimatePresence } from "framer-motion"
import { SiFastapi, SiPostgresql, SiReact, SiVite, SiPython, SiThreedotjs } from "react-icons/si"

import DashboardLayout from "../components/DashboardLayout"
import GlobePanel from "../components/GlobePanel"

// ─── Reusable primitives ──────────────────────────────────────────────────────

const GlassInput = ({ label, ...props }) => {
  const [focused, setFocused] = useState(false)
  const hasValue = props.value !== "" && props.value !== undefined
  return (
    <div className="relative group">
      <label className={`absolute left-4 transition-all duration-300 pointer-events-none z-10 font-mono text-xs tracking-widest uppercase
        ${focused || hasValue ? "-top-2.5 text-cyan-400 text-[10px]" : "top-1/2 -translate-y-1/2 text-gray-500 text-sm"}`}>
        {label}
      </label>
      <input
        {...props}
        onFocus={e => { setFocused(true); props.onFocus?.(e) }}
        onBlur={e => { setFocused(false); props.onBlur?.(e) }}
        className="w-full bg-white/[0.04] border border-white/10 text-white rounded-2xl px-4 pt-5 pb-3 text-sm
          backdrop-blur-md outline-none transition-all duration-300
          focus:border-cyan-400/60 focus:bg-white/[0.07] focus:shadow-[0_0_20px_rgba(34,211,238,0.12)]
          hover:border-white/20 placeholder-transparent"
      />
      <div className={`absolute inset-0 rounded-2xl pointer-events-none transition-opacity duration-300
        bg-gradient-to-br from-cyan-400/5 to-purple-500/5 ${focused ? "opacity-100" : "opacity-0"}`} />
    </div>
  )
}

const GlassSelect = ({ label, children, ...props }) => (
  <div className="relative group">
    <label className="absolute left-4 -top-2.5 text-cyan-400 text-[10px] font-mono tracking-widest uppercase z-10">{label}</label>
    <select {...props} className="w-full bg-white/[0.04] border border-white/10 text-white rounded-2xl px-4 pt-5 pb-3 text-sm
      backdrop-blur-md outline-none transition-all duration-300 appearance-none cursor-pointer
      focus:border-cyan-400/60 focus:bg-white/[0.07] focus:shadow-[0_0_20px_rgba(34,211,238,0.12)] hover:border-white/20">
      {children}
    </select>
    <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-cyan-400/60 text-xs">▾</div>
  </div>
)

const NeonButton = ({ children, onClick, variant = "cyan", className = "" }) => {
  const variants = {
    cyan:   "from-cyan-500/20 to-cyan-400/10 border-cyan-400/40 text-cyan-300 hover:border-cyan-400 hover:shadow-[0_0_24px_rgba(34,211,238,0.35)]",
    purple: "from-purple-500/20 to-purple-400/10 border-purple-400/40 text-purple-300 hover:border-purple-400 hover:shadow-[0_0_24px_rgba(168,85,247,0.35)]",
    solid:  "from-cyan-500/80 to-cyan-400/60 border-cyan-300/60 text-white hover:from-cyan-400/90 hover:shadow-[0_0_32px_rgba(34,211,238,0.5)]",
  }
  return (
    <motion.button onClick={onClick} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
      className={`relative overflow-hidden bg-gradient-to-br ${variants[variant]} border rounded-2xl
        px-6 py-4 font-mono text-sm tracking-wider uppercase backdrop-blur-md transition-all duration-300 w-full ${className}`}>
      <span className="relative z-10">{children}</span>
      <motion.div className="absolute inset-0 bg-white/5" initial={{ x: "-100%" }} whileHover={{ x: "100%" }} transition={{ duration: 0.5 }} />
    </motion.button>
  )
}

const DestinationCard = ({ item, reviews }) => {
  const avgRating = reviews?.length
    ? (reviews.reduce((s, r) => s + r.value_rating, 0) / reviews.length).toFixed(1)
    : null
  return (
    <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -6, scale: 1.01 }} transition={{ duration: 0.4, ease: "easeOut" }}
      className="relative group rounded-3xl overflow-hidden backdrop-blur-xl border border-white/10
        hover:border-cyan-400/40 bg-gradient-to-br from-white/[0.05] to-white/[0.02]
        transition-all duration-500 hover:shadow-[0_8px_40px_rgba(34,211,238,0.12)]">
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-400/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="p-6 space-y-3">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-xl font-semibold text-white tracking-tight">{item.city}</h3>
            <p className="text-xs font-mono text-cyan-400/70 tracking-widest mt-0.5 uppercase">{item.country_code}</p>
          </div>
          {avgRating && (
            <div className="flex items-center gap-1.5 bg-yellow-400/10 border border-yellow-400/20 rounded-xl px-3 py-1.5">
              <span className="text-yellow-400 text-xs">★</span>
              <span className="text-yellow-300 text-sm font-mono font-semibold">{avgRating}</span>
            </div>
          )}
        </div>
        <div className="h-px bg-white/5" />
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white/[0.03] rounded-xl p-3">
            <p className="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-1">Est. Cost</p>
            <p className="text-cyan-300 font-mono font-semibold text-sm">💸 {item.estimated_trip_cost}</p>
          </div>
          <div className="bg-white/[0.03] rounded-xl p-3">
            <p className="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-1">Weather</p>
            <p className="text-sky-300 text-sm font-mono">🌤 {item.weather}</p>
          </div>
        </div>
        {reviews?.length > 0 && (
          <p className="text-xs text-gray-500 font-mono">{reviews.length} traveller review{reviews.length !== 1 ? "s" : ""}</p>
        )}
      </div>
    </motion.div>
  )
}

const SectionHeading = ({ children, sub }) => (
  <div className="text-center mb-12 space-y-2">
    <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
      className="text-4xl font-bold bg-gradient-to-r from-cyan-300 via-white to-purple-300 bg-clip-text text-transparent tracking-tight">
      {children}
    </motion.h2>
    {sub && (
      <motion.p initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} transition={{ duration: 0.6, delay: 0.2 }}
        className="text-sm font-mono text-gray-500 tracking-widest uppercase">
        {sub}
      </motion.p>
    )}
  </div>
)

const StarRating = ({ rating, setRating }) => (
  <div className="flex gap-3 text-3xl cursor-pointer justify-center">
    {[1, 2, 3, 4, 5].map(star => (
      <motion.span key={star} onClick={() => setRating(star)} whileHover={{ scale: 1.3 }} whileTap={{ scale: 0.9 }}
        className={`transition-all duration-200 select-none ${star <= rating ? "text-yellow-400 drop-shadow-[0_0_8px_rgba(250,204,21,0.7)]" : "text-gray-600 hover:text-gray-400"}`}>
        ★
      </motion.span>
    ))}
  </div>
)

const DataPill = ({ label, value, color = "cyan" }) => {
  const colors = { cyan: "border-cyan-400/20 bg-cyan-400/5 text-cyan-300", purple: "border-purple-400/20 bg-purple-400/5 text-purple-300", sky: "border-sky-400/20 bg-sky-400/5 text-sky-300" }
  return (
    <div className={`border rounded-2xl p-4 backdrop-blur-sm ${colors[color]}`}>
      <p className="text-[10px] font-mono text-gray-500 uppercase tracking-widest mb-1">{label}</p>
      <p className="font-mono font-semibold text-sm">{value}</p>
    </div>
  )
}

const GlassCard = ({ children, className = "" }) => (
  <div className={`group relative bg-white/[0.04] border border-white/10 rounded-3xl backdrop-blur-xl
    hover:border-cyan-400/40 transition-all duration-500 hover:shadow-[0_8px_40px_rgba(34,211,238,0.1)] ${className}`}>
    <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-400/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-t-3xl" />
    {children}
  </div>
)

// ─── Static data ──────────────────────────────────────────────────────────────

const TECHNOLOGIES = [
  { icon: <SiFastapi color="#009688" />,    name: "FastAPI"    },
  { icon: <SiPostgresql color="#336791" />, name: "PostgreSQL" },
  { icon: <SiReact color="#61DAFB" />,      name: "React"      },
  { icon: <SiVite color="#FFD62E" />,       name: "Vite"       },
  { icon: <SiThreedotjs color="#ffffff" />, name: "Three.js"   },
  { icon: <SiPython color="#3776AB" />,     name: "Python"     },
]

const FEATURES = [
  { icon: "💸", title: "Budget-Based Recommendations", desc: "Find destinations tailored to your budget with intelligent cost estimation." },
  { icon: "🌤️", title: "Weather-Aware Travel",          desc: "Choose destinations based on real-time weather conditions that match your preferences." },
  { icon: "⭐", title: "Real User Reviews",              desc: "Explore authentic traveler experiences and ratings to guide better decisions." },
  { icon: "🧠", title: "Smart Travel Intelligence",      desc: "Combines cost, weather, and user data into one powerful recommendation system." },
  { icon: "⚖️", title: "City Comparison Engine",        desc: "Compare destinations side-by-side across cost, climate, and ratings." },
  { icon: "📊", title: "Data-Driven Insights",           desc: "Powered by real datasets and analytics to support smarter travel planning." },
]

const DATASETS = [
//   { icon: "✈️", title: "OpenFlights Airports Database", desc: "Provides global airport data including airport locations, IATA codes and airline connectivity used to model the global airport network.",  link: "https://www.kaggle.com/datasets/divyanshrai/openflights-airports-database-2017" },
  { icon: "🌦️", title: "Global Weather Repository",      desc: "Contains worldwide weather and temperature information used to analyse climate conditions for travel destinations.",                           link: "https://www.kaggle.com/datasets/salhirahma/global-weather-repository" },
  { icon: "🌍", title: "World Bank Tourism Dataset",      desc: "Provides international tourism arrival statistics used to identify the most visited travel destinations globally.",                              link: "https://data360.worldbank.org/en/indicator/WB_WDI_ST_INT_ARVL?view=datatable" },
  { icon: "💰", title: "Travel Trip Records Dataset",     desc: "Contains travel cost and trip data used to analyse affordable destinations and build travel value analytics.",                                   link: "https://www.kaggle.com/datasets/muqaddasejaz/travel-trip-records-dataset" },
]

// ─── MAIN COMPONENT ───────────────────────────────────────────────────────────
export default function Dashboard() {

  const [budget, setBudget]                 = useState(1000)
  const [days, setDays]                     = useState(5)
  const [weather, setWeather]               = useState("")
  const [weatherOptions, setWeatherOptions] = useState([])
  const [results, setResults]               = useState([])
  const [loading, setLoading]               = useState(false)
  const [reviewsMap, setReviewsMap]         = useState({})

  const [summaryCity, setSummaryCity] = useState("")
  const [summary, setSummary]         = useState(null)

  const [city1, setCity1]     = useState("")
  const [city2, setCity2]     = useState("")
  const [compare, setCompare] = useState(null)

  const [reviewCity, setReviewCity]       = useState("")
  const [reviewName, setReviewName]       = useState("")
  const [reviewSpent, setReviewSpent]     = useState("")
  const [reviewDays, setReviewDays]       = useState("")
  const [reviewRating, setReviewRating]   = useState(0)
  const [reviewComment, setReviewComment] = useState("")
  const [reviewMessage, setReviewMessage] = useState("")

  const containerRef = useRef(null)

  useEffect(() => {
    axios.get("https://budgetwise-api-6tzv.onrender.com/weather/")
      .then(res => {
        const unique = [...new Set(res.data.map(w => w.condition).filter(Boolean))]
        setWeatherOptions(unique)
      })
      .catch(() => setWeatherOptions([]))
  }, [])

  const handleSearch = async () => {
    setLoading(true); setResults([]); setReviewsMap({})
    try {
      const res = await axios.get("https://budgetwise-api-6tzv.onrender.com/recommendations/best-destination", { params: { budget, days, weather_pref: weather } })
      const destinations = res.data?.recommended_destinations || []
      setResults(destinations)
      const cities = await axios.get("https://budgetwise-api-6tzv.onrender.com/cities/")
      const reviewPromises = destinations.map(async (item) => {
        const cityObj = cities.data.find(c => c.city_name.toLowerCase() === item.city.toLowerCase())
        if (!cityObj) return [item.city, []]
        try {
          const r = await axios.get(`https://budgetwise-api-6tzv.onrender.com/reviews/city/${cityObj.city_id}`)
          return [item.city, r.data.reviews || []]
        } catch { return [item.city, []] }
      })
      const arr = await Promise.all(reviewPromises)
      setReviewsMap(Object.fromEntries(arr))
    } catch { setResults([]) }
    setLoading(false)
  }

  const getSummary = async () => {
    setSummary(null)
    try {
      const res = await axios.get("https://budgetwise-api-6tzv.onrender.com/destinations/summary", { params: { city: summaryCity } })
      const data = res.data

      // Fetch reviews for this city
      try {
        const cities = await axios.get("https://budgetwise-api-6tzv.onrender.com/cities/")
        const cityObj = cities.data.find(c => c.city_name.toLowerCase() === summaryCity.toLowerCase())
        if (cityObj) {
          const rev = await axios.get(`https://budgetwise-api-6tzv.onrender.com/reviews/city/${cityObj.city_id}`)
          data._reviews = rev.data.reviews || []
        } else {
          data._reviews = []
        }
      } catch {
        data._reviews = []
      }

      setSummary(data)
    } catch { setSummary("error") }
  }

  const getCompare = async () => {
    setCompare(null)
    try {
      const res = await axios.get("https://budgetwise-api-6tzv.onrender.com/compare/cities", { params: { city1, city2 } })
      setCompare(res.data)
    } catch { setCompare("error") }
  }

  const submitReview = async () => {
    setReviewMessage("")
    try {
      const cities = await axios.get("https://budgetwise-api-6tzv.onrender.com/cities/")
      const cityObj = cities.data.find(c => c.city_name.toLowerCase() === reviewCity.toLowerCase())
      if (!cityObj) { setReviewMessage("❌ City not found"); return }
      await axios.post("https://budgetwise-api-6tzv.onrender.com/reviews/", null, {
        params: { city_id: cityObj.city_id, user_name: reviewName, money_spent: reviewSpent, trip_days: reviewDays, value_rating: reviewRating, comment: reviewComment }
      })
      handleSearch()
      setReviewMessage("✅ Review submitted!")
    } catch { setReviewMessage("❌ Failed to submit") }
  }

  const fadeUp = {
    hidden: { opacity: 0, y: 50 },
    show:   { opacity: 1, y: 0, transition: { duration: 0.7, ease: [0.22, 1, 0.36, 1] } }
  }

  const snap = { scrollSnapAlign: "start" }

  return (
    <DashboardLayout>
      <style>{`
        .snap-scroll-container { scrollbar-width: none; -ms-overflow-style: none; scroll-behavior: smooth; }
        .snap-scroll-container::-webkit-scrollbar { display: none; }
        * { -webkit-font-smoothing: antialiased; }
      `}</style>

      <div ref={containerRef} className="snap-scroll-container h-screen overflow-y-scroll scroll-smooth" style={{ scrollSnapType: "y mandatory" }}>

        {/* ── HERO ── */}
        <section id="hero" style={snap} className="min-h-screen flex flex-col justify-center relative overflow-hidden">
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-[120px]" />
            <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-500/10 rounded-full blur-[120px]" />
          </div>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1 }}>
            <div className="text-center mb-10 space-y-4 relative z-10">
              <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.2 }}
                className="inline-flex items-center gap-2 bg-cyan-400/10 border border-cyan-400/20 rounded-full px-4 py-1.5 mb-4">
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                <span className="font-mono text-xs text-cyan-400 tracking-widest uppercase">Travel Intelligence System</span>
              </motion.div>
              <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, delay: 0.3 }}
                className="text-6xl md:text-7xl font-bold tracking-tight">
                <span className="bg-gradient-to-r from-white via-cyan-100 to-white bg-clip-text text-transparent">Travel smarter,</span>
                <br />
                <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">not harder.</span>
              </motion.h1>
              <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8, delay: 0.5 }}
                className="text-gray-400 font-mono text-sm tracking-widest uppercase">
                Spend less · vibe more · explore beyond
              </motion.p>
            </div>
            <div className="mb-10"><GlobePanel airports={[]} /></div>
          </motion.div>
        </section>

        {/* ── FINDER ── */}
        <section id="finder" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute -top-60 right-0 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[140px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-6xl mx-auto px-6 py-16">
            <SectionHeading sub="AI-powered matching">Smart Destination Finder</SectionHeading>
            <div className="grid md:grid-cols-4 gap-4 mb-10">
              <GlassInput label="Budget (£)" type="number" value={budget} onChange={e => setBudget(e.target.value)} />
              <GlassInput label="Days" type="number" value={days} onChange={e => setDays(e.target.value)} />
              <GlassSelect label="Weather Pref" value={weather} onChange={e => setWeather(e.target.value)}>
                <option value="">Any Weather</option>
                {weatherOptions.map((w, i) => <option key={i}>{w}</option>)}
              </GlassSelect>
              <NeonButton onClick={handleSearch} variant="solid">{loading ? "Scanning..." : "Find My Trip →"}</NeonButton>
            </div>
            <AnimatePresence>
              {loading && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex items-center justify-center gap-3 py-12">
                  <div className="flex gap-1.5">
                    {[0,1,2].map(i => (
                      <motion.div key={i} className="w-2 h-2 rounded-full bg-cyan-400"
                        animate={{ y: [0, -10, 0] }} transition={{ duration: 0.8, delay: i * 0.15, repeat: Infinity }} />
                    ))}
                  </div>
                  <span className="font-mono text-sm text-gray-400 tracking-widest">Scanning destinations</span>
                </motion.div>
              )}
            </AnimatePresence>
            {results.length > 0 && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} className="grid md:grid-cols-3 gap-6">
                {results.map((item, i) => (
                  <motion.div key={i} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
                    <DestinationCard item={item} reviews={reviewsMap[item.city] || []} />
                  </motion.div>
                ))}
              </motion.div>
            )}
          </motion.div>
        </section>

        {/* ── SUMMARY ── */}
        <section id="summary" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-[120px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-3xl mx-auto px-6 py-16 max-h-screen overflow-y-auto" style={{ scrollbarWidth: "none" }}>
            <SectionHeading sub="Deep dive any city">Destination Summary</SectionHeading>
            <div className="flex gap-3 mb-10">
              <div className="flex-1">
                <GlassInput label="City name" type="text" value={summaryCity} onChange={e => setSummaryCity(e.target.value)} onKeyDown={e => e.key === "Enter" && getSummary()} />
              </div>
              <div className="w-40"><NeonButton onClick={getSummary} variant="cyan">Search</NeonButton></div>
            </div>
            <AnimatePresence>
              {summary && summary !== "error" && (
                <motion.div initial={{ opacity: 0, y: 20, scale: 0.98 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.5 }}
                  className="space-y-6">

                  {/* ── City info card ── */}
                  <div className="bg-white/[0.03] border border-white/10 rounded-3xl p-8 backdrop-blur-xl space-y-6
                    hover:border-cyan-400/20 transition-all duration-500 hover:shadow-[0_0_40px_rgba(34,211,238,0.06)]">
                    <div className="flex items-center justify-between">
                      <h3 className="text-2xl font-bold text-white">{summaryCity}</h3>
                      <span className="font-mono text-xs text-cyan-400 border border-cyan-400/30 rounded-full px-3 py-1 bg-cyan-400/5">{summary.country_code}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <DataPill label="Daily Cost" value={summary.daily_cost} color="cyan" />
                      <DataPill label="Weather"    value={summary.weather}    color="sky" />
                      <DataPill label="Tourism"    value={summary.tourism}    color="purple" />
                    </div>
                  </div>

                  {/* ── Reviews for this city ── */}
                  {summary._reviews?.length > 0 && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between px-1">
                        <p className="text-xs font-mono text-gray-500 uppercase tracking-widest">Traveller Reviews</p>
                        <div className="flex items-center gap-1.5 bg-yellow-400/10 border border-yellow-400/20 rounded-xl px-3 py-1">
                          <span className="text-yellow-400 text-xs">★</span>
                          <span className="text-yellow-300 text-sm font-mono font-semibold">
                            {(summary._reviews.reduce((s, r) => s + r.value_rating, 0) / summary._reviews.length).toFixed(1)}
                          </span>
                          <span className="text-gray-500 text-xs font-mono">/ 5</span>
                        </div>
                      </div>
                      {summary._reviews.map((r, i) => (
                        <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                          className="bg-white/[0.03] border border-white/10 rounded-2xl p-5 backdrop-blur-md
                            hover:border-purple-400/20 transition-all duration-300">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <p className="text-white text-sm font-semibold">{r.user_name}</p>
                              <p className="text-gray-500 text-xs font-mono mt-0.5">
                                💸 £{r.money_spent} · {r.trip_days} days
                              </p>
                            </div>
                            <div className="flex gap-0.5">
                              {[1,2,3,4,5].map(s => (
                                <span key={s} className={`text-sm ${s <= r.value_rating ? "text-yellow-400" : "text-gray-700"}`}>★</span>
                              ))}
                            </div>
                          </div>
                          {r.comment && (
                            <p className="text-gray-400 text-sm leading-relaxed border-t border-white/5 pt-3 mt-2 italic">
                              "{r.comment}"
                            </p>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {summary._reviews?.length === 0 && (
                    <p className="text-center text-gray-600 font-mono text-xs tracking-widest uppercase py-4">
                      No reviews yet for this city
                    </p>
                  )}
                </motion.div>
              )}
              {summary === "error" && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-red-400 font-mono text-sm text-center">⚠ City not found or server error</motion.p>
              )}
            </AnimatePresence>
          </motion.div>
        </section>

        {/* ── COMPARE ── */}
        <section id="compare" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[150px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-4xl mx-auto px-6 py-16">
            <SectionHeading sub="Head to head analysis">Compare Cities</SectionHeading>
            <div className="grid md:grid-cols-3 gap-4 mb-10">
              <GlassInput label="City one" type="text" value={city1} onChange={e => setCity1(e.target.value)} />
              <GlassInput label="City two" type="text" value={city2} onChange={e => setCity2(e.target.value)} />
              <NeonButton onClick={getCompare} variant="purple">Compare →</NeonButton>
            </div>
            <AnimatePresence>
              {compare && compare !== "error" && (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="grid md:grid-cols-2 gap-6">
                  {[{ label: city1, data: compare.city1 }, { label: city2, data: compare.city2 }].map((col, i) => (
                    <div key={i} className={`border rounded-3xl p-6 backdrop-blur-xl space-y-4 transition-all duration-500
                      ${i === 0 ? "border-cyan-400/20 bg-cyan-400/[0.03] hover:shadow-[0_0_30px_rgba(34,211,238,0.08)]"
                               : "border-purple-400/20 bg-purple-400/[0.03] hover:shadow-[0_0_30px_rgba(168,85,247,0.08)]"}`}>
                      <h3 className={`text-xl font-bold ${i === 0 ? "text-cyan-300" : "text-purple-300"}`}>{col.label}</h3>
                      {col.data && Object.entries(col.data).map(([k, v]) => (
                        <div key={k} className="flex justify-between items-center border-b border-white/5 pb-2">
                          <span className="text-xs font-mono text-gray-500 uppercase tracking-wider">{k.replace(/_/g, " ")}</span>
                          <span className="text-sm text-white font-mono">{String(v ?? "N/A")}</span>
                        </div>
                      ))}
                    </div>
                  ))}
                </motion.div>
              )}
              {compare === "error" && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-red-400 font-mono text-sm text-center">⚠ Could not load comparison</motion.p>
              )}
            </AnimatePresence>
          </motion.div>
        </section>

        {/* ── REVIEW ── */}
        <section id="review" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-500/5 rounded-full blur-[150px]" />
          </div>
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-2xl mx-auto px-6 py-16">
            <SectionHeading sub="Help fellow travellers">Share Your Experience</SectionHeading>
            <div className="bg-white/[0.03] border border-white/10 rounded-3xl p-8 backdrop-blur-xl space-y-5 hover:border-purple-400/20 transition-all duration-500">
              <div className="grid md:grid-cols-2 gap-4">
                <GlassInput label="City" type="text" value={reviewCity} onChange={e => setReviewCity(e.target.value)} />
                <GlassInput label="Your name" type="text" value={reviewName} onChange={e => setReviewName(e.target.value)} />
                <GlassInput label="Amount spent (£)" type="number" value={reviewSpent} onChange={e => setReviewSpent(e.target.value)} />
                <GlassInput label="Trip length (days)" type="number" value={reviewDays} onChange={e => setReviewDays(e.target.value)} />
              </div>
              <div>
                <p className="text-xs font-mono text-gray-500 uppercase tracking-widest mb-3">Value Rating</p>
                <StarRating rating={reviewRating} setRating={setReviewRating} />
              </div>
              <GlassInput label="Your comment" type="text" value={reviewComment} onChange={e => setReviewComment(e.target.value)} />
              <NeonButton onClick={submitReview} variant="purple">Submit Review</NeonButton>
              <AnimatePresence>
                {reviewMessage && (
                  <motion.p initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                    className={`text-sm font-mono text-center ${reviewMessage.startsWith("✅") ? "text-emerald-400" : "text-red-400"}`}>
                    {reviewMessage}
                  </motion.p>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </section>

        {/* ── ABOUT ── */}
        <section id="about" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[150px] pointer-events-none" />
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-[120px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-4xl mx-auto px-6 py-16 text-center">
            <SectionHeading sub="Powered by intelligence">BudgetWise Travel</SectionHeading>
            <p className="text-gray-400 max-w-2xl mx-auto text-base leading-relaxed mb-12">
              A data-driven travel API that helps users discover the best destinations based on budget,
              weather preferences, and real user experiences. It combines cost data, climate insights,
              and reviews into one intelligent system.
            </p>
            <a href="https://budgetwise-api-6tzv.onrender.com/docs#/" target="_blank" rel="noopener noreferrer"
              className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-cyan-500/80 to-cyan-400/60
                border border-cyan-300/40 rounded-2xl text-white font-mono text-sm tracking-widest uppercase
                hover:shadow-[0_0_32px_rgba(34,211,238,0.5)] hover:border-cyan-300 transition-all duration-300">
              Open API Docs <span className="text-lg">→</span>
            </a>
          </motion.div>
        </section>

        {/* ── FEATURES ── */}
        <section id="features" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute top-0 left-0 w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-[120px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-6xl mx-auto px-6 py-16">
            <SectionHeading sub="What makes us smart">Smart Travel Intelligence Features</SectionHeading>
            <div className="grid md:grid-cols-3 gap-6">
              {FEATURES.map((f, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.08, duration: 0.5 }} whileHover={{ y: -4, scale: 1.01 }}>
                  <GlassCard className="p-7 h-full">
                    <div className="text-4xl mb-4">{f.icon}</div>
                    <h3 className="text-white font-semibold text-lg mb-2 tracking-tight">{f.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* ── DATA SOURCES ── */}
        <section id="datasources" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-cyan-500/5 rounded-full blur-[120px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-6xl mx-auto px-6 py-16">
            <SectionHeading sub="Powering our intelligence">Data Sources</SectionHeading>
            <p className="text-center text-gray-400 font-mono text-sm max-w-2xl mx-auto mb-12">
              Integrating multiple datasets to analyse global travel patterns, airport networks, tourism statistics and weather conditions.
            </p>
            <div className="grid md:grid-cols-2 gap-6">
              {DATASETS.map((d, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1, duration: 0.5 }} whileHover={{ y: -4, scale: 1.01 }}>
                  <GlassCard className="p-8">
                    <div className="text-4xl mb-4">{d.icon}</div>
                    <h3 className="text-lg font-semibold text-white mb-2 tracking-tight">{d.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed mb-6">{d.desc}</p>
                    <a href={d.link} target="_blank" rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 font-mono text-xs text-cyan-400 tracking-widest uppercase hover:text-cyan-300 transition-colors duration-200">
                      View Dataset <span className="text-base">→</span>
                    </a>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* ── API STACK ── */}
        <section id="techstack" style={snap} className="min-h-screen flex items-center relative overflow-hidden">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-500/5 rounded-full blur-[160px] pointer-events-none" />
          <motion.div variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="w-full max-w-5xl mx-auto px-6 py-16">
            <SectionHeading sub="Built with">Technology Stack</SectionHeading>
            <div className="grid grid-cols-3 md:grid-cols-6 gap-5">
              {TECHNOLOGIES.map((tech, i) => (
                <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.08, duration: 0.4 }} whileHover={{ y: -6, scale: 1.08 }}>
                  <GlassCard className="p-6 text-center">
                    <div className="text-4xl mb-3 flex justify-center">{tech.icon}</div>
                    <p className="text-gray-300 text-sm font-mono">{tech.name}</p>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>

      </div>
    </DashboardLayout>
  )
}
