/* ============================================================
   XOOTAY GOX YI — custom.js
   Animation géométrique (Visibilité optimisée pour Light Mode)
   ============================================================ */

   document$.subscribe(function() {
    
    // 1. Nettoyage et création du canvas
    const existingCanvas = document.getElementById('xgy-particles');
    if (existingCanvas) existingCanvas.remove();

    const canvas = document.createElement('canvas');
    canvas.id = 'xgy-particles';
    document.body.insertBefore(canvas, document.body.firstChild);
    
    const ctx = canvas.getContext('2d');
    let particlesArray;

    function setCanvasSize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', setCanvasSize);
    setCanvasSize();

    let mouse = { x: null, y: null, radius: 100 };
    window.addEventListener('mousemove', function(event) {
        mouse.x = event.x; mouse.y = event.y;
    });
    window.addEventListener('mouseout', function() {
        mouse.x = null; mouse.y = null;
    });

    class Particle {
        constructor(x, y, directionX, directionY, size) {
            this.x = x; this.y = y;
            this.directionX = directionX; this.directionY = directionY;
            this.size = size;
        }
        draw(color) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = color;
            ctx.fill();
        }
        update(color) {
            if (this.x > canvas.width || this.x < 0) this.directionX = -this.directionX;
            if (this.y > canvas.height || this.y < 0) this.directionY = -this.directionY;
            
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx*dx + dy*dy);
            if (distance < mouse.radius) {
                this.x -= dx/20;
                this.y -= dy/20;
            }

            this.x += this.directionX;
            this.y += this.directionY;
            this.draw(color);
        }
    }

    function init() {
        particlesArray = [];
        let numberOfParticles = (canvas.height * canvas.width) / 12000; 
        if (numberOfParticles > 100) numberOfParticles = 100; 

        for (let i = 0; i < numberOfParticles; i++) {
            let size = (Math.random() * 2) + 1;
            let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
            let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
            let directionX = (Math.random() * 1) - 0.5; 
            let directionY = (Math.random() * 1) - 0.5;
            particlesArray.push(new Particle(x, y, directionX, directionY, size));
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, innerWidth, innerHeight);

        // Ajustement des couleurs : 0.2 (au lieu de 0.1) pour le mode clair
        const isDarkMode = document.body.getAttribute('data-md-color-scheme') === 'slate';
        const pColor = isDarkMode ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.2)'; 
        const lColor = isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.1)'; 

        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update(pColor);
        }
        connect(lColor);
    }

    function connect(lineColor) {
        for (let a = 0; a < particlesArray.length; a++) {
            for (let b = a; b < particlesArray.length; b++) {
                let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
                             + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                if (distance < (canvas.width / 10) * (canvas.height / 10)) {
                    ctx.strokeStyle = lineColor;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    init();
    animate();
});