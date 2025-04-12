document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.form-tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            document.querySelectorAll('.form-tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // Remove active class from all content
            document.querySelectorAll('.form-tab-content').forEach(c => {
                c.classList.remove('active');
            });
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const target = tab.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });
    
    // Activate first tab by default
    if (tabs.length > 0) {
        tabs[0].click();
    }
});
