 // İstatistik sayı animasyonu
        function animateStats() {
            const statNumbers = document.querySelectorAll('.stat-number');
            const animationDuration = 2000;
            const frameDuration = 1000 / 60;
            const totalFrames = Math.round(animationDuration / frameDuration);
            
            statNumbers.forEach(stat => {
                const target = parseInt(stat.getAttribute('data-count'));
                const easeOutQuad = t => t * (2 - t);
                
                let frame = 0;
                const countTo = target;
                
                const counter = setInterval(() => {
                    frame++;
                    const progress = easeOutQuad(frame / totalFrames);
                    const currentCount = Math.round(countTo * progress);
                    
                    if (parseInt(stat.innerHTML) !== currentCount) {
                        stat.innerHTML = currentCount;
                    }
                    
                    if (frame === totalFrames) {
                        clearInterval(counter);
                    }
                }, frameDuration);
            });
        }
        
        // Sayfada göründüğünde animasyonu başlat
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(document.querySelector('.stats-container'));
        
        // Aktif menü linkini vurgula
        const currentPage = location.pathname.split('/').pop();
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPage) {
                link.classList.add('active');
            }
        });