import { useRef } from "react"
import { useFrame, useLoader } from "@react-three/fiber"
import * as THREE from "three"
import Plane from "./Plane"

function Satellite() {

    const satellite = useRef()

    useFrame(({ clock }) => {

        const t = clock.getElapsedTime()

        const radius = 3.2

        satellite.current.position.x = Math.cos(t * 0.5) * radius
        satellite.current.position.z = Math.sin(t * 0.5) * radius
        satellite.current.position.y = Math.sin(t * 0.3)

        satellite.current.rotation.y += 0.05

    })

    return (

        <mesh ref={satellite}>

            <boxGeometry args={[0.1, 0.1, 0.3]} />

            <meshStandardMaterial
                color="#22d3ee"
                emissive="#22d3ee"
                emissiveIntensity={2}
            />

        </mesh>

    )

}

export default function Earth({ airports }) {

    const mesh = useRef()

    const texture = useLoader(
        THREE.TextureLoader,
        "/earth.jpg"
    )

    useFrame(() => {
        if (mesh.current) {
            mesh.current.rotation.y += 0.0008
        }
    })

    return (

        <group ref={mesh}>



            {/* EARTH SPHERE */}

            <mesh>

                <sphereGeometry args={[2, 64, 64]} />

                <meshStandardMaterial map={texture} />

            </mesh>
            {/* <Satellite /> */}

            {/* ✈️ PLANE */}
            <Plane />

            {/* AIRPORT MARKERS */}

            {airports.map((airport, i) => {

                if (!airport.latitude || !airport.longitude) return null

                const lat = airport.latitude * Math.PI / 180
                const lon = airport.longitude * Math.PI / 180

                const r = 2

                const x = r * Math.cos(lat) * Math.sin(lon)
                const y = r * Math.sin(lat)
                const z = r * Math.cos(lat) * Math.cos(lon)

                return (

                    <mesh key={i} position={[x, y, z]}>

                        <sphereGeometry args={[0.035, 8, 8]} />

                        <meshStandardMaterial
                            color="#22d3ee"
                            emissive="#22d3ee"
                            emissiveIntensity={1.5}
                        />

                    </mesh>

                )

            })}

        </group>

    )

}