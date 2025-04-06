// This file contains the JavaScript code for the user interface, handling user interactions and dynamic content updates.

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-upload-form');
    const fileInput = document.getElementById('resume');
    const fileUploadDiv = document.querySelector('.file-upload');
    const removeButton = document.querySelector('.remove-file');

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        if (this.files.length > 0) {
            fileUploadDiv.classList.add('has-file');
        } else {
            fileUploadDiv.classList.remove('has-file');
        }
    });

    // Handle file removal
    removeButton.addEventListener('click', function(e) {
        fileInput.value = '';
        fileUploadDiv.classList.remove('has-file');
        const resultsSection = document.getElementById('results');
        resultsSection.style.opacity = '0';
        resultsSection.classList.remove('visible');
    });

    if (!form) return;

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const loadingSpinner = document.getElementById('loading-spinner');
        const resultsSection = document.getElementById('results');
        const suggestions = document.getElementById('suggestions');
        
        // Show loading state
        loadingSpinner.style.display = 'block';
        resultsSection.style.opacity = '0';
        
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            loadingSpinner.style.display = 'none';
            
            // Format and display results
            let resultsHtml = `
                <div class="score-section">
                    <h3>Resume Score: ${data.score}%</h3>
                </div>`;
            
            if (data.details.strengths.length > 0) {
                resultsHtml += `
                    <div class="strengths">
                        <h4>Strengths:</h4>
                        <ul>${data.details.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
                    </div>`;
            }
            
            if (data.details.improvements.length > 0) {
                resultsHtml += `
                    <div class="improvements">
                        <h4>Suggested Improvements:</h4>
                        <ul>${data.details.improvements.map(i => `<li>${i}</li>`).join('')}</ul>
                    </div>`;
            }
            
            if (data.details.missing_elements.length > 0) {
                resultsHtml += `
                    <div class="missing">
                        <h4>Missing Elements:</h4>
                        <ul>${data.details.missing_elements.map(m => `<li>${m}</li>`).join('')}</ul>
                    </div>`;
            }
            
            suggestions.innerHTML = resultsHtml;
            resultsSection.style.opacity = '1';
            resultsSection.classList.add('visible');
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.style.display = 'none';
            suggestions.innerHTML = '<p class="error">An error occurred while analyzing the resume. Please try again.</p>';
            resultsSection.classList.add('visible');
        });
    });
});

// Function to reset the form
document.getElementById('resetButton').addEventListener('click', function() {
    document.getElementById('resumeForm').reset();
    document.getElementById('results').innerText = '';
});