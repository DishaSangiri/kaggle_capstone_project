import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';
import { useReality } from '../context/RealityContext';

const EvolvingSphere: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);
  const { planetState } = useReality();

  // Slow rotation for ambient planetary visual effect
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.12;
      meshRef.current.rotation.x = state.clock.getElapsedTime() * 0.04;
    }
  });

  // Extract biome values to dynamically adjust planet visuals
  const forest = planetState?.forest_health ?? 0.5;
  const ocean = planetState?.ocean_health ?? 0.5;
  const focus = planetState?.focus_health ?? 0.5;
  const finance = planetState?.finance_health ?? 0.5;

  const color = new THREE.Color();
  // Formulate a dynamic RGB mapping using biome parameters
  color.setRGB(
    focus * 0.7 + finance * 0.3,
    forest * 0.7 + finance * 0.2,
    ocean * 0.8 + focus * 0.1
  );

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[2.8, 64, 64]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.45}
        roughness={0.45}
        metalness={0.65}
      />
    </mesh>
  );
};

export const PlanetContainer: React.FC = () => {
  return (
    <div className="w-full h-full relative min-h-[300px] md:min-h-[450px]">
      <Canvas camera={{ position: [0, 0, 5], fov: 38 }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[8, 8, 8]} intensity={2.2} />
        <directionalLight position={[-6, -6, -6]} intensity={1.0} color="#4f46e5" />
        
        {/* Render planet sphere mesh */}
        <EvolvingSphere />
        
        {/* Sky box stars simulation */}
        <Stars radius={100} depth={50} count={5000} factor={5} saturation={0} fade speed={1.2} />
        
        {/* Dynamic camera orbit manipulation */}
        <OrbitControls enableZoom={true} enablePan={false} autoRotate autoRotateSpeed={0.4} />
      </Canvas>
      
      {/* Holographic HUD UI overlay */}
      <div className="absolute bottom-4 left-4 p-3 glass-panel rounded-lg flex flex-col gap-1 pointer-events-none select-none animate-float">
        <h3 className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Reality Coordinates</h3>
        <p className="text-[10px] text-gray-400">System Mode: Multi-Agent Simulation</p>
      </div>
    </div>
  );
};

export default PlanetContainer;
