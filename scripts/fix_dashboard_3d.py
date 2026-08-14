import re

with open("generate_dashboard.py", "r") as f:
    text = f.read()

# 1. Inject Three.js script in the <head>
threejs_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
text = text.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>', 
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>\n        ' + threejs_script)

# 2. Replace the old header with the new 3D container
old_header_regex = r'<header class="mb-10 text-center">.*?</header>'
new_header = """<header class="mb-6 text-center relative">
                <!-- 3D Azam Core Container -->
                <div id="azam-core-container" class="w-full h-48 md:h-64 mx-auto cursor-pointer" style="max-width: 400px; touch-action: none;"></div>
                
                <div class="inline-block relative z-10 -mt-6 pointer-events-none">
                    <h1 class="text-5xl sm:text-6xl md:text-8xl font-hero tracking-widest text-white uppercase italic transform -skew-x-6 drop-shadow-2xl">
                        <span class="gold-text">AZAM!</span> RADAR
                    </h1>
                </div>
            </header>"""
text = re.sub(old_header_regex, new_header, text, flags=re.DOTALL)

# 3. Inject the Three.js logic before the closing </body> tag
threejs_logic = """
        // 3D Azam Core Logic
        const container = document.getElementById('azam-core-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "high-performance" });
        
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // Draw dynamic lightning bolt
        const shape = new THREE.Shape();
        shape.moveTo( 0, 9 );     
        shape.lineTo( -6, -2 );   
        shape.lineTo( -1, -2 );   
        shape.lineTo( -4, -10 );   
        shape.lineTo( 6, 0 );     
        shape.lineTo( 1, 0 );     
        shape.lineTo( 0, 9 );     

        const extrudeSettings = { 
            depth: 2.5, 
            bevelEnabled: true, 
            bevelSegments: 4, 
            steps: 2, 
            bevelSize: 0.6, 
            bevelThickness: 0.6 
        };
        const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        geometry.center(); 

        const material = new THREE.MeshStandardMaterial({ 
            color: 0xFFC107, 
            emissive: 0x331000,
            emissiveIntensity: 0.6,
            metalness: 0.9, 
            roughness: 0.1,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1
        });
        
        const bolt = new THREE.Mesh(geometry, material);
        scene.add(bolt);

        // Cinematic Lighting
        const light = new THREE.PointLight(0xffffff, 1.5, 100);
        light.position.set(10, 15, 20);
        scene.add(light);
        
        const fillLight = new THREE.PointLight(0xFF4500, 1.2, 100);
        fillLight.position.set(-15, -10, -10);
        scene.add(fillLight);

        const ambientLight = new THREE.AmbientLight(0xffaa00, 0.4);
        scene.add(ambientLight);

        camera.position.z = 32;

        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX - window.innerWidth / 2);
            mouseY = (e.clientY - window.innerHeight / 2);
        });

        // Touch support for mobile
        document.addEventListener('touchmove', (e) => {
            if(e.touches.length > 0) {
                mouseX = (e.touches[0].clientX - window.innerWidth / 2);
                mouseY = (e.touches[0].clientY - window.innerHeight / 2);
            }
        });

        function animate() {
            requestAnimationFrame(animate);
            targetX = mouseX * 0.002;
            targetY = mouseY * 0.002;

            bolt.rotation.y += 0.015; // Base spin
            
            // Magnetic tilt towards mouse (parallax)
            bolt.rotation.x += (targetY - bolt.rotation.x) * 0.05;
            bolt.rotation.z = (targetX - bolt.rotation.z) * 0.05;

            // Subtle pulsing float
            bolt.position.y = Math.sin(Date.now() * 0.002) * 1.5;

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            if(container) {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }
        });
        """

text = text.replace('</script>\n    </body></html>', threejs_logic + '\n        </script>\n    </body></html>')

with open("generate_dashboard.py", "w") as f:
    f.write(text)

