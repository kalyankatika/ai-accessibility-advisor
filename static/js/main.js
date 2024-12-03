document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const analyzeForm = document.getElementById('analyzeForm');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            const urlsInput = document.getElementById('urls');
            const urls = urlsInput.value.trim().split('\n').filter(url => url.trim());
            
            if (urls.length === 0) {
                e.preventDefault();
                alert('Please enter at least one valid URL');
                return;
            }
            
            if (urls.length > 10) {
                e.preventDefault();
                alert('Maximum 10 URLs allowed for batch processing');
                return;
            }
            
            // Validate URLs
            const invalidUrls = urls.filter(url => {
                try {
                    const parsed = new URL(url);
                    return !parsed.protocol || !parsed.host;
                } catch {
                    return true;
                }
            });
            
            if (invalidUrls.length > 0) {
                e.preventDefault();
                alert(`Invalid URL format detected:\n${invalidUrls.join('\n')}`);
                return;
            }
            
            // Add loading state
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing ${urls.length} URLs...`;
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
