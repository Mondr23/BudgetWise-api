import { Canvas } from "@react-three/fiber"
import { Stars, OrbitControls } from "@react-three/drei"
import Earth from "./Earth"

export default function GlobePanel({ airports }) {

    return (

        <div className="relative w-full h-[700px] mb-24">


            <Canvas camera={{ position: [0, 0, 7] }}>

                <ambientLight intensity={0.8} />
                <pointLight position={[10, 10, 10]} />

                <Stars
                    radius={300}
                    depth={120}
                    count={15000}
                    factor={5}
                    fade
                />

                <Earth airports={airports} />

                <OrbitControls enableZoom={false} />

            </Canvas>

        </div>

    )
}