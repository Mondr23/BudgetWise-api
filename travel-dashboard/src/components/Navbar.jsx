import { Link, useLocation } from "react-router-dom"
import { useState } from "react"

export default function Navbar() {

  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)

  const isDashboard = location.pathname === "/"

  const routes = [
    { path: "/analytics",    label: "Analytics", icon: "📈" },
    { path: "/about-api",    label: "API",        icon: "⚡" },
    { path: "/data-sources", label: "Data",       icon: "🌍" },
  ]

  const sections = [
    { id: "hero",         label: "Home",       icon: "🏠" },
    { id: "finder",       label: "Finder",     icon: "🔍" },
    { id: "summary",      label: "Summary",    icon: "📋" },
    { id: "compare",      label: "Compare",    icon: "⚖️"  },
    { id: "review",       label: "Review",     icon: "⭐" },
    { id: "about",        label: "About",      icon: "⚡" },
    { id: "features",     label: "Features",   icon: "🧠" },
    { id: "datasources",  label: "Sources",    icon: "🌍" },
    { id: "techstack",    label: "Stack",      icon: "🛠️"  },
  ]

  const scrollTo = (id) => {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: "smooth" })
    setMenuOpen(false)
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-black/40 border-b border-cyan-400/10 shadow-[0_0_20px_rgba(0,255,255,0.05)]">

      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 md:px-12 py-4">

        {/* LOGO */}
        <Link to="/" className="flex items-center gap-3 shrink-0">
          <div className="text-cyan-400 font-bold text-xl tracking-widest drop-shadow-[0_0_10px_cyan]">BWT</div>
          <span className="text-gray-400 text-xs hidden md:block">BudgetWise Travel</span>
        </Link>

        {/* DESKTOP MENU */}
        <div className="hidden md:flex items-center gap-1">

          {isDashboard ? (
            // ── On dashboard: show all section scroll links ──
            sections.map((s, i) => (
              <button
                key={i}
                onClick={() => scrollTo(s.id)}
                className="relative group flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-mono
                  uppercase tracking-wider text-gray-400 hover:text-cyan-400
                  hover:bg-cyan-400/5 transition-all duration-300"
              >
                <span className="text-sm">{s.icon}</span>
                {s.label}
                <span className="absolute bottom-0 left-1/2 -translate-x-1/2 h-px w-0 bg-cyan-400
                  group-hover:w-3/4 transition-all duration-300" />
              </button>
            ))
          ) : (
            // ── On other pages: show route links ──
            routes.map((link, i) => {
              const active = location.pathname === link.path
              return (
                <Link key={i} to={link.path}
                  className={`relative flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-mono
                    uppercase tracking-wider transition-all duration-300
                    ${active ? "text-cyan-400 bg-cyan-400/5" : "text-gray-400 hover:text-cyan-400 hover:bg-cyan-400/5"}`}>
                  <span>{link.icon}</span>
                  {link.label}
                  {active && <span className="absolute bottom-0 left-1/2 -translate-x-1/2 h-px w-3/4 bg-cyan-400" />}
                </Link>
              )
            })
          )}

          {/* Always show Dashboard link when not on dashboard */}
          {!isDashboard && (
            <Link to="/"
              className="ml-4 flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono uppercase tracking-wider
                bg-cyan-400/10 border border-cyan-400/30 text-cyan-400
                hover:bg-cyan-400/20 hover:border-cyan-400 transition-all duration-300">
              📊 Dashboard
            </Link>
          )}
        </div>

        {/* MOBILE HAMBURGER */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden text-cyan-400 text-2xl w-10 h-10 flex items-center justify-center
            rounded-xl border border-cyan-400/20 hover:border-cyan-400/50 hover:bg-cyan-400/5 transition-all duration-300"
        >
          {menuOpen ? "✕" : "☰"}
        </button>
      </div>

      {/* MOBILE MENU */}
      {menuOpen && (
        <div className="md:hidden bg-black/95 border-t border-cyan-400/20 backdrop-blur-xl">
          <div className="max-h-[70vh] overflow-y-auto py-4 px-6 space-y-1">

            {isDashboard ? (
              <>
                <p className="text-[10px] font-mono text-gray-600 uppercase tracking-widest px-3 pb-2">Sections</p>
                {sections.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => scrollTo(s.id)}
                    className="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-mono
                      text-gray-300 hover:text-cyan-400 hover:bg-cyan-400/5 transition-all duration-300 text-left"
                  >
                    <span>{s.icon}</span>
                    {s.label}
                  </button>
                ))}
              </>
            ) : (
              <>
                <Link to="/" onClick={() => setMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-mono text-cyan-400 hover:bg-cyan-400/5 transition-all duration-300">
                  📊 Dashboard
                </Link>
                {routes.map((link, i) => (
                  <Link key={i} to={link.path} onClick={() => setMenuOpen(false)}
                    className={`flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-mono transition-all duration-300
                      ${location.pathname === link.path ? "text-cyan-400 bg-cyan-400/5" : "text-gray-300 hover:text-cyan-400 hover:bg-cyan-400/5"}`}>
                    <span>{link.icon}</span>
                    {link.label}
                  </Link>
                ))}
              </>
            )}

          </div>
        </div>
      )}

    </nav>
  )
}
