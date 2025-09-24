// src/app/page.js
"use client"

import { Canvas, useThree, useFrame} from '@react-three/fiber'
import { Stars, useGLTF, OrbitControls } from '@react-three/drei'
import { useEffect, useRef } from 'react'
import gsap from 'gsap'


function Planet() {
  const { scene } = useGLTF('/models/smaller.glb')
  return <primitive object={scene} scale={0.5} />
}

function Sun() {
  return (
    <mesh position={[10, 10, 10]}>
      <sphereGeometry args={[2, 32, 32]} />
      {/* Use meshStandardMaterial for emissive glow */}
      <meshStandardMaterial color="orange" emissive="yellow" emissiveIntensity={2} />
      <pointLight intensity={10} color="white" />
    </mesh>
  )
}


// Camera zoom animation
function CameraZoom() {
  const { camera } = useThree()
  useEffect(() => {
    camera.position.set(0, 0, 20)
    gsap.to(camera.position, { z: 5, duration: 5, ease: 'power2.inOut' })
  }, [camera])
  return null
}

export default function Home() {
  return (
    <div className="w-screen h-screen">
      <Canvas camera={{ position: [0, 0, 20], fov: 60 }}>
        {/* Stars background */}
        <Stars radius={100} depth={50} count={5000} factor={4} fade />

        {/* Add a Sun light */}
        <pointLight
          position={[10, 10, 10]}   // Sun position
          intensity={500}             // brightness
          color="white"
        />

        {/* Optional: soft ambient light so shadows aren’t fully black */}
        <ambientLight intensity={1} />

        {/* Planet */}
        <Planet />
        <Sun />

        {/* Camera animation */}
        <CameraZoom />

        {/* Orbit controls */}
        <OrbitControls 
          enableZoom={true}
          minDistance={2}
          maxDistance={50}
          enablePan={false}
        />
      </Canvas>
    </div>
  )
}
