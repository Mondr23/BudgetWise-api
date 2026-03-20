import { useRef } from "react"
import { useFrame } from "@react-three/fiber"
import { useGLTF } from "@react-three/drei"
import * as THREE from "three"

export default function Plane() {

    const plane = useRef()
    const { scene } = useGLTF("/models/plane.glb")

    const radius = 2.4

    useFrame(({ clock }) => {

        const t = clock.getElapsedTime()
        const angle = t * 0.25

        // POSITION (nice orbit)
        const x = radius * Math.cos(angle)
        const z = radius * Math.sin(angle) * 0.6 + 1.2
        const y = Math.sin(angle * 0.8) * 0.6

        const current = new THREE.Vector3(x, y, z)
        plane.current.position.copy(current)

        // NEXT POSITION (direction)
        const nextAngle = (t + 0.02) * 0.25

        const next = new THREE.Vector3(
            radius * Math.cos(nextAngle),
            Math.sin(nextAngle * 0.8) * 0.6,
            radius * Math.sin(nextAngle) * 0.6 + 1.2
        )

        // 👉 DIRECTION VECTOR
        const direction = new THREE.Vector3()
            .subVectors(next, current)
            .normalize()

        // 👉 FIX: create rotation without flipping
        const up = new THREE.Vector3(0, 1, 0)
        const right = new THREE.Vector3().crossVectors(up, direction).normalize()
        const correctedUp = new THREE.Vector3().crossVectors(direction, right).normalize()

        const matrix = new THREE.Matrix4().makeBasis(right, correctedUp, direction)
        const quaternion = new THREE.Quaternion().setFromRotationMatrix(matrix)

        plane.current.quaternion.copy(quaternion)

    })

    return (
        <primitive
            ref={plane}
            object={scene}
            scale={0.015}
        />
    )
}