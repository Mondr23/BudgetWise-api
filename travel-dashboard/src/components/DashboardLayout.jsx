import Navbar from "./Navbar"
import Starfield from "./Starfield"

export default function DashboardLayout({children}){

  return(

    <div className="min-h-screen text-white relative">

      <Starfield />

      <Navbar />

      <main className="pt-28 pb-32">

        {children}
      </main>

    </div>

  )

}

