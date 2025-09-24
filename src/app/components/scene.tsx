// src/app/Scene.tsx
"use client"

import { Canvas, useThree } from "@react-three/fiber"
import { Stars, OrbitControls, useGLTF } from "@react-three/drei"
import { useRef, useEffect } from "react"
import { useFrame } from "@react-three/fiber"
import gsap from "gsap"
import * as THREE from "three"

// Planet
function Planet({ modelPath, scale }: { modelPath: string; scale: number }) {
    const planetRef = useRef<THREE.Object3D>(null!)
    const { scene } = useGLTF(modelPath)

    // Spin around Y-axis
    useFrame(() => {
        if (planetRef.current) {
            planetRef.current.rotation.y += 0.0009
        }
    })

    return <primitive ref={planetRef} object={scene} scale={scale} />
}
// Sun
function Sun({ modelPath, scale }: { modelPath: string; scale: number }) {
    const sunRef = useRef<THREE.Object3D>(null!)
    const { scene } = useGLTF(modelPath)

    useFrame(() => {
        if (sunRef.current) {
            sunRef.current.rotation.y += 0.001
        }
    })

    return (
        <group position={[10, 0, 50]} scale={scale}>
            <primitive ref={sunRef} object={scene} />
            <pointLight intensity={3000} color="white" />
        </group>
    )
}

// Camera zoom animation
function CameraZoom() {
    const { camera } = useThree()
    useEffect(() => {
        camera.position.set(0, 0, 20)
        gsap.to(camera.position, { z: 5, duration: 5, ease: "power2.inOut" })
    }, [camera])
    return null
}

export default function Scene({
    planetModel,
    sunModel,
}: {
    planetModel: { path: string; scale: number }
    sunModel: { path: string; scale: number }
}) {
    return (
        <Canvas camera={{ position: [0, 0, 20], fov: 60 }}>
            {/* Background stars */}
            <Stars radius={100} depth={50} count={5000} factor={4} fade />

            {/* Lighting */}
            <ambientLight intensity={0.8} />

            {/* Sun + Planet */}
            <Sun modelPath={sunModel.path} scale={sunModel.scale} />
            <Planet modelPath={planetModel.path} scale={planetModel.scale} />

            {/* Zoom animation after selection */}
            <CameraZoom />

            {/* Controls */}
            <OrbitControls
                enableZoom
                minDistance={2}
                maxDistance={50}
                enablePan={false}
            />
        </Canvas>
    )
}
