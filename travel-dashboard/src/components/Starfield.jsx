import { Canvas } from "@react-three/fiber"
import { Stars } from "@react-three/drei"

export default function Starfield() {

    return (

        <div className="fixed inset-0 -z-10">

            <Canvas>

                <Stars
                    radius={200}
                    depth={100}
                    count={12000}
                    factor={4}
                    fade
                />

            </Canvas>

        </div>

    )

}