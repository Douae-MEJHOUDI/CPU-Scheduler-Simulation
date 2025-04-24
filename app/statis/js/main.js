
document.addEventListener('DOMContentLoaded', function() {
    
    enhanceFormValidation();
    
    setupDynamicFormBehavior();
    
    enhanceTableInteraction();
    
    initializeBootstrapComponents();
});

function enhanceFormValidation() {
    const form = document.querySelector('form');
    
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        form.classList.add('was-validated');
    });
    
    const minBurst = document.getElementById('min_burst');
    const maxBurst = document.getElementById('max_burst');
    const minArrival = document.getElementById('min_arrival');
    const maxArrival = document.getElementById('max_arrival');
    const minPriority = document.getElementById('min_priority');
    const maxPriority = document.getElementById('max_priority');
    
    if (minBurst && maxBurst) {
        validateMinMaxPair(minBurst, maxBurst);
    }
    
    if (minArrival && maxArrival) {
        validateMinMaxPair(minArrival, maxArrival);
    }
    
    if (minPriority && maxPriority) {
        validateMinMaxPair(minPriority, maxPriority);
    }
}


function validateMinMaxPair(minInput, maxInput) {
    const validateValues = () => {
        const minVal = parseInt(minInput.value, 10);
        const maxVal = parseInt(maxInput.value, 10);
        
        if (minVal > maxVal) {
            maxInput.setCustomValidity('Maximum value must be greater than or equal to minimum value');
        } else {
            maxInput.setCustomValidity('');
        }
    };
    
    minInput.addEventListener('change', validateValues);
    maxInput.addEventListener('change', validateValues);
}


function setupDynamicFormBehavior() {
    const algorithmSelect = document.getElementById('algorithm');
    const quantumField = document.getElementById('quantum');
    
    if (algorithmSelect && quantumField) {
        const quantumFormGroup = quantumField.closest('.form-group').parentElement;
        
        algorithmSelect.addEventListener('change', function() {
            const algorithm = this.value;
            if (algorithm === 'rr' || algorithm === 'priority_rr' || algorithm === 'all') {
                quantumFormGroup.style.display = 'block';
            } else {
                quantumFormGroup.style.display = 'none';
            }
        });
        
        const algorithm = algorithmSelect.value;
        if (algorithm === 'rr' || algorithm === 'priority_rr' || algorithm === 'all') {
            quantumFormGroup.style.display = 'block';
        } else {
            quantumFormGroup.style.display = 'none';
        }
    }
    
    const fileInput = document.querySelector('input[type="file"]');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileNameElement = document.querySelector('.custom-file-label');
            
            if (fileNameElement) {
                if (this.files.length > 0) {
                    fileNameElement.textContent = this.files[0].name;
                } else {
                    fileNameElement.textContent = 'Choose file...';
                }
            }
        });
    }
}

function enhanceTableInteraction() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        if (table.classList.contains('sortable')) {
            const headers = table.querySelectorAll('th');
            
            headers.forEach(header => {
                if (!header.classList.contains('no-sort')) {
                    header.addEventListener('click', function() {
                        sortTable(table, Array.from(headers).indexOf(this));
                    });
                    header.style.cursor = 'pointer';
                    header.title = 'Click to sort';
                }
            });
        }
    });
}


function sortTable(table, colIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const direction = table.getAttribute('data-sort-dir') === 'asc' ? -1 : 1;

    rows.sort((a, b) => {
        const aValue = a.cells[colIndex].textContent.trim();
        const bValue = b.cells[colIndex].textContent.trim();
        
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction * (aNum - bNum);
        }
        
        return direction * aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => row.remove());

    rows.forEach(row => tbody.appendChild(row));

    table.setAttribute('data-sort-dir', direction === 1 ? 'asc' : 'desc');
}


function initializeBootstrapComponents() {
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
    
    const popovers = document.querySelectorAll('[data-toggle="popover"]');
    popovers.forEach(popover => {
        new bootstrap.Popover(popover);
    });
}