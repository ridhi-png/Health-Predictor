// Health Predictor Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initializeBootstrapComponents();
    
    // Initialize symptom search functionality
    initializeSymptomSearch();
    
    // Initialize severity sliders
    initializeSeveritySliders();
    
    // Add form validation
    initializeFormValidation();
});

/**
 * Initialize Bootstrap components like tooltips, popovers, etc.
 */
function initializeBootstrapComponents() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add Bootstrap classes to form elements
    const formControls = document.querySelectorAll('input:not([type="checkbox"]), select, textarea');
    formControls.forEach(function(element) {
        if (!element.classList.contains('form-control')) {
            element.classList.add('form-control');
        }
    });
    
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(element) {
        if (!element.classList.contains('form-check-input')) {
            element.classList.add('form-check-input');
        }
    });
}

/**
 * Initialize symptom search functionality
 */
function initializeSymptomSearch() {
    const symptomSearchInput = document.getElementById('symptom-search');
    const bodyPartFilter = document.getElementById('body-part-filter');
    
    if (symptomSearchInput) {
        symptomSearchInput.addEventListener('input', filterSymptoms);
    }
    
    if (bodyPartFilter) {
        bodyPartFilter.addEventListener('change', filterSymptoms);
    }
    
    // Initial filter application
    if (symptomSearchInput || bodyPartFilter) {
        filterSymptoms();
    }
    
    // Symptom search API functionality
    const apiSearchInput = document.getElementById('api-symptom-search');
    if (apiSearchInput) {
        apiSearchInput.addEventListener('input', debounce(searchSymptomsAPI, 300));
    }
}

/**
 * Filter symptoms based on search input and body part selection
 */
function filterSymptoms() {
    const searchInput = document.getElementById('symptom-search');
    const bodyPartFilter = document.getElementById('body-part-filter');
    
    if (!searchInput && !bodyPartFilter) return;
    
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const bodyPart = bodyPartFilter ? bodyPartFilter.value : '';
    
    // Get all symptom groups
    const symptomGroups = document.querySelectorAll('.symptom-group');
    
    symptomGroups.forEach(function(group) {
        const groupBodyPart = group.getAttribute('data-body-part');
        let groupVisible = false;
        
        // Skip filtering if body part doesn't match (unless 'all' is selected)
        if (bodyPart && bodyPart !== 'all' && groupBodyPart !== bodyPart) {
            group.style.display = 'none';
            return;
        }
        
        // Get all symptom checkboxes in this group
        const symptoms = group.querySelectorAll('.symptom-checkbox');
        
        symptoms.forEach(function(symptom) {
            const symptomText = symptom.textContent.toLowerCase();
            
            if (searchTerm === '' || symptomText.includes(searchTerm)) {
                symptom.style.display = '';
                groupVisible = true;
            } else {
                symptom.style.display = 'none';
            }
        });
        
        // Show/hide the entire group based on if any symptoms are visible
        group.style.display = groupVisible ? '' : 'none';
    });
    
    // Update the count of visible symptoms
    updateVisibleSymptomCount();
}

/**
 * Update the count of visible symptoms
 */
function updateVisibleSymptomCount() {
    const visibleSymptoms = document.querySelectorAll('.symptom-checkbox:not([style*="display: none"])');
    const countElement = document.getElementById('visible-symptom-count');
    
    if (countElement) {
        countElement.textContent = visibleSymptoms.length;
    }
}

/**
 * Search symptoms using the API
 */
function searchSymptomsAPI() {
    const searchInput = document.getElementById('api-symptom-search');
    const resultsContainer = document.getElementById('api-search-results');
    
    if (!searchInput || !resultsContainer) return;
    
    const searchTerm = searchInput.value.trim();
    
    if (searchTerm.length < 2) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    // Show loading indicator
    resultsContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    
    // Make API request
    fetch(`/api/symptoms/search/?q=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = '';
            
            if (data.length === 0) {
                resultsContainer.innerHTML = '<div class="alert alert-info">No symptoms found matching your search.</div>';
                return;
            }
            
            const list = document.createElement('ul');
            list.className = 'list-group';
            
            data.forEach(symptom => {
                const item = document.createElement('li');
                item.className = 'list-group-item d-flex justify-content-between align-items-center';
                item.innerHTML = `
                    <div>
                        <strong>${symptom.name}</strong>
                        <span class="badge bg-secondary ms-2">${symptom.body_part}</span>
                    </div>
                    <button class="btn btn-sm btn-outline-primary add-symptom-btn" data-id="${symptom.id}">Add</button>
                `;
                list.appendChild(item);
            });
            
            resultsContainer.appendChild(list);
            
            // Add event listeners to the Add buttons
            document.querySelectorAll('.add-symptom-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const symptomId = this.getAttribute('data-id');
                    addSymptomToSelection(symptomId);
                });
            });
        })
        .catch(error => {
            console.error('Error searching symptoms:', error);
            resultsContainer.innerHTML = '<div class="alert alert-danger">Error searching symptoms. Please try again.</div>';
        });
}

/**
 * Add a symptom to the selection
 */
function addSymptomToSelection(symptomId) {
    const selectedSymptomsContainer = document.getElementById('selected-symptoms');
    const selectedSymptomInput = document.getElementById('selected-symptom-ids');
    
    if (!selectedSymptomsContainer || !selectedSymptomInput) return;
    
    // Get current selected symptom IDs
    let selectedIds = selectedSymptomInput.value ? selectedSymptomInput.value.split(',') : [];
    
    // Check if symptom is already selected
    if (selectedIds.includes(symptomId)) {
        return;
    }
    
    // Add the symptom ID to the hidden input
    selectedIds.push(symptomId);
    selectedSymptomInput.value = selectedIds.join(',');
    
    // Make API request to get symptom details
    fetch(`/api/symptoms/${symptomId}/`)
        .then(response => response.json())
        .then(symptom => {
            // Create a badge for the selected symptom
            const badge = document.createElement('span');
            badge.className = 'badge bg-primary me-2 mb-2 selected-symptom';
            badge.setAttribute('data-id', symptom.id);
            badge.innerHTML = `
                ${symptom.name}
                <button type="button" class="btn-close btn-close-white ms-2" aria-label="Remove"></button>
            `;
            
            selectedSymptomsContainer.appendChild(badge);
            
            // Add event listener to the remove button
            badge.querySelector('.btn-close').addEventListener('click', function() {
                removeSymptomFromSelection(symptom.id);
                badge.remove();
            });
        })
        .catch(error => {
            console.error('Error getting symptom details:', error);
        });
}

/**
 * Remove a symptom from the selection
 */
function removeSymptomFromSelection(symptomId) {
    const selectedSymptomInput = document.getElementById('selected-symptom-ids');
    
    if (!selectedSymptomInput) return;
    
    // Get current selected symptom IDs
    let selectedIds = selectedSymptomInput.value ? selectedSymptomInput.value.split(',') : [];
    
    // Remove the symptom ID
    selectedIds = selectedIds.filter(id => id !== symptomId.toString());
    selectedSymptomInput.value = selectedIds.join(',');
}

/**
 * Initialize severity sliders
 */
function initializeSeveritySliders() {
    const severitySliders = document.querySelectorAll('.severity-slider');
    
    severitySliders.forEach(function(slider) {
        const valueDisplay = document.getElementById(slider.getAttribute('data-value-display'));
        
        if (valueDisplay) {
            // Update the display value when the slider changes
            slider.addEventListener('input', function() {
                updateSeverityDisplay(this.value, valueDisplay);
            });
            
            // Initialize with current value
            updateSeverityDisplay(slider.value, valueDisplay);
        }
    });
}

/**
 * Update the severity display with appropriate color coding
 */
function updateSeverityDisplay(value, displayElement) {
    displayElement.textContent = value;
    
    // Remove existing color classes
    displayElement.classList.remove('severity-mild', 'severity-moderate', 'severity-severe');
    
    // Add appropriate color class based on severity
    if (value <= 3) {
        displayElement.classList.add('severity-mild');
    } else if (value <= 6) {
        displayElement.classList.add('severity-moderate');
    } else {
        displayElement.classList.add('severity-severe');
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Debounce function to limit how often a function is called
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

/**
 * Show a toast notification
 */
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    
    // Initialize and show the toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove the toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}