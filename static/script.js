/**
 * AI Car Price Predictor - Premium Interactive JavaScript
 * Handles form submissions, API calls, animations, toast notifications, and UI interactions
 */

// Global variables
let priceChart = null;
let dealChart = null;
let priceTrendsChart = null;
let statusDistributionChart = null;
let featureImportanceChart = null;
let uploadedImageUrl = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeNavigation();
    initializeForms();
    initializeDropdowns();
    initializeImageUpload();
    loadPredictionHistory();
    initializeCharts();
    initializeDashboard();
    initializeAnimatedCounters();
});

// Toast Notification System
function showToast(type, title, message, duration = 5000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `
        <div class="toast-icon">
            <i class="fas ${icons[type] || icons.info}"></i>
        </div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    // Close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    });

    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('removing');
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// Image Upload Functionality
function initializeImageUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const uploadContent = document.getElementById('uploadContent');
    const uploadPreview = document.getElementById('uploadPreview');
    const previewImage = document.getElementById('previewImage');
    const removeImage = document.getElementById('removeImage');

    if (!uploadArea) return;

    // Click to upload
    uploadArea.addEventListener('click', () => {
        imageInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageUpload(files[0]);
        }
    });

    // File input change
    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageUpload(e.target.files[0]);
        }
    });

    // Remove image
    removeImage.addEventListener('click', (e) => {
        e.stopPropagation();
        uploadedImageUrl = null;
        uploadContent.classList.remove('hidden');
        uploadPreview.classList.add('hidden');
        imageInput.value = '';
    });

    function handleImageUpload(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            showToast('error', 'Invalid File', 'Please upload a valid image file (JPEG, PNG, GIF, WebP)');
            return;
        }

        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
            showToast('error', 'File Too Large', 'Please upload an image smaller than 5MB');
            return;
        }

        // Preview image
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            uploadContent.classList.add('hidden');
            uploadPreview.classList.remove('hidden');
            uploadedImageUrl = e.target.result;
            showToast('success', 'Image Uploaded', 'Car image has been uploaded successfully');
        };
        reader.readAsDataURL(file);
    }
}

// Theme Toggle
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        updateThemeIcon(savedTheme);
    }
    
    themeToggle.addEventListener('click', function() {
        body.classList.toggle('light-mode');
        const currentTheme = body.classList.contains('light-mode') ? 'light-mode' : 'dark-mode';
        localStorage.setItem('theme', currentTheme);
        updateThemeIcon(currentTheme);
    });
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    const icon = themeToggle.querySelector('i');
    
    if (theme === 'light-mode') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// Navigation
function initializeNavigation() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    mobileMenuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });
    
    // Smooth scrolling for nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu
                navMenu.classList.remove('active');
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Update active link on scroll
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section');
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
}

// Initialize Forms
function initializeForms() {
    // Prediction form
    const predictionForm = document.getElementById('predictionForm');
    predictionForm.addEventListener('submit', handlePrediction);
    
    // Compare forms
    const compareButton = document.getElementById('compareButton');
    compareButton.addEventListener('click', handleComparison);
    
    // Clear history button
    const clearHistoryButton = document.getElementById('clearHistory');
    clearHistoryButton.addEventListener('click', clearHistory);
    
    // Download PDF button
    const downloadPdfButton = document.getElementById('downloadPdf');
    downloadPdfButton.addEventListener('click', downloadPDF);
}

// Initialize Dropdowns
function initializeDropdowns() {
    // Populate year dropdown
    const yearSelect = document.getElementById('year');
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 2000; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }
    
    // Populate compare year dropdowns
    const compareYearSelects = document.querySelectorAll('.compare-year');
    compareYearSelects.forEach(select => {
        for (let year = currentYear; year >= 2000; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select.appendChild(option);
        }
    });
    
    // Load companies and other dropdowns
    loadDropdownData();
    
    // Company change event for prediction form
    const companySelect = document.getElementById('company');
    companySelect.addEventListener('change', function() {
        loadModelsForCompany(this.value, 'model');
    });
    
    // Company change events for compare forms
    const compareCompanySelects = document.querySelectorAll('.compare-company');
    compareCompanySelects.forEach((select, index) => {
        select.addEventListener('change', function() {
            const modelSelect = document.querySelectorAll('.compare-model')[index];
            loadModelsForCompany(this.value, null, modelSelect);
        });
    });
}

// Load dropdown data from API
async function loadDropdownData() {
    try {
        // Load companies
        const companiesResponse = await fetch('/api/companies');
        const companiesData = await companiesResponse.json();
        populateDropdown('company', companiesData.companies);
        
        const compareCompanySelects = document.querySelectorAll('.compare-company');
        compareCompanySelects.forEach(select => {
            populateDropdown(null, companiesData.companies, select);
        });
        
        // Load fuel types
        const fuelResponse = await fetch('/api/fuel-types');
        const fuelData = await fuelResponse.json();
        populateDropdown('fuel_type', fuelData.fuel_types);
        
        const compareFuelSelects = document.querySelectorAll('.compare-fuel');
        compareFuelSelects.forEach(select => {
            populateDropdown(null, fuelData.fuel_types, select);
        });
        
        // Load transmission types
        const transmissionResponse = await fetch('/api/transmission-types');
        const transmissionData = await transmissionResponse.json();
        populateDropdown('transmission', transmissionData.transmission_types);
        
        const compareTransmissionSelects = document.querySelectorAll('.compare-transmission');
        compareTransmissionSelects.forEach(select => {
            populateDropdown(null, transmissionData.transmission_types, select);
        });
        
        // Load owner types
        const ownerResponse = await fetch('/api/owner-types');
        const ownerData = await ownerResponse.json();
        populateDropdown('owner_type', ownerData.owner_types);
        
        const compareOwnerSelects = document.querySelectorAll('.compare-owner');
        compareOwnerSelects.forEach(select => {
            populateDropdown(null, ownerData.owner_types, select);
        });
        
    } catch (error) {
        console.error('Error loading dropdown data:', error);
        // Fallback to hardcoded values
        populateDropdown('company', ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Mahindra', 'Tata', 'Ford', 'Volkswagen', 'Skoda', 'Renault', 'Nissan', 'Kia', 'MG', 'Jeep']);
        populateDropdown('fuel_type', ['Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid', 'LPG']);
        populateDropdown('transmission', ['Manual', 'Automatic']);
        populateDropdown('owner_type', ['First', 'Second', 'Third', 'Fourth & Above']);
    }
}

// Populate dropdown with options
function populateDropdown(elementId, options, customSelect = null) {
    const select = customSelect || document.getElementById(elementId);
    if (!select) return;
    
    // Clear existing options (except the first one)
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        select.appendChild(opt);
    });
}

// Load models for a specific company
async function loadModelsForCompany(company, modelElementId, customSelect = null) {
    if (!company) return;
    
    try {
        const response = await fetch(`/api/car-models/${company}`);
        const data = await response.json();
        
        const modelSelect = customSelect || document.getElementById(modelElementId);
        if (modelSelect) {
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
            modelSelect.disabled = false;
        }
    } catch (error) {
        console.error('Error loading models:', error);
        // Fallback models
        const fallbackModels = ['Swift', 'i20', 'City', 'Innova', 'Creta'];
        const modelSelect = customSelect || document.getElementById(modelElementId);
        if (modelSelect) {
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            fallbackModels.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
            modelSelect.disabled = false;
        }
    }
}

// Handle Prediction with Validation
async function handlePrediction(e) {
    e.preventDefault();
    
    // Validate form
    if (!validatePredictionForm()) {
        return;
    }
    
    const loadingOverlay = document.getElementById('loadingOverlay');
    const buttonLoader = document.getElementById('buttonLoader');
    const submitButton = document.querySelector('#predictionForm button[type="submit"]');
    
    loadingOverlay.classList.remove('hidden');
    buttonLoader.classList.remove('hidden');
    submitButton.disabled = true;
    
    const formData = {
        company: document.getElementById('company').value,
        model: document.getElementById('model').value,
        year: parseInt(document.getElementById('year').value),
        fuel_type: document.getElementById('fuel_type').value,
        transmission: document.getElementById('transmission').value,
        kilometers_driven: parseFloat(document.getElementById('kilometers_driven').value),
        owner_type: document.getElementById('owner_type').value,
        mileage: parseFloat(document.getElementById('mileage').value),
        engine_capacity: parseFloat(document.getElementById('engine_capacity').value)
    };
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayPredictionResult(data, formData);
            loadPredictionHistory();
            updateCharts();
            updateDashboard();
            showToast('success', 'Prediction Complete', `Estimated price: ₹${data.predicted_price.toLocaleString('en-IN')}`);
        } else {
            showToast('error', 'Prediction Failed', data.error);
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showToast('error', 'Network Error', 'An error occurred during prediction. Please try again.');
    } finally {
        loadingOverlay.classList.add('hidden');
        buttonLoader.classList.add('hidden');
        submitButton.disabled = false;
    }
}

// Form Validation
function validatePredictionForm() {
    let isValid = true;
    
    // Company
    const company = document.getElementById('company');
    const companyError = document.getElementById('companyError');
    if (!company.value) {
        companyError.textContent = 'Please select a company';
        companyError.classList.add('visible');
        company.parentElement.classList.add('error');
        isValid = false;
    } else {
        companyError.classList.remove('visible');
        company.parentElement.classList.remove('error');
    }
    
    // Model
    const model = document.getElementById('model');
    const modelError = document.getElementById('modelError');
    if (!model.value) {
        modelError.textContent = 'Please select a model';
        modelError.classList.add('visible');
        model.parentElement.classList.add('error');
        isValid = false;
    } else {
        modelError.classList.remove('visible');
        model.parentElement.classList.remove('error');
    }
    
    // Year
    const year = document.getElementById('year');
    const yearError = document.getElementById('yearError');
    if (!year.value) {
        yearError.textContent = 'Please select a year';
        yearError.classList.add('visible');
        year.parentElement.classList.add('error');
        isValid = false;
    } else {
        yearError.classList.remove('visible');
        year.parentElement.classList.remove('error');
    }
    
    // Kilometers Driven
    const km = document.getElementById('kilometers_driven');
    const kmError = document.getElementById('kmError');
    if (!km.value || km.value < 0 || km.value > 500000) {
        kmError.textContent = 'Please enter valid kilometers (0-500000)';
        kmError.classList.add('visible');
        km.parentElement.classList.add('error');
        isValid = false;
    } else {
        kmError.classList.remove('visible');
        km.parentElement.classList.remove('error');
    }
    
    // Mileage
    const mileage = document.getElementById('mileage');
    const mileageError = document.getElementById('mileageError');
    if (!mileage.value || mileage.value < 0 || mileage.value > 50) {
        mileageError.textContent = 'Please enter valid mileage (0-50 km/l)';
        mileageError.classList.add('visible');
        mileage.parentElement.classList.add('error');
        isValid = false;
    } else {
        mileageError.classList.remove('visible');
        mileage.parentElement.classList.remove('error');
    }
    
    // Engine Capacity
    const engine = document.getElementById('engine_capacity');
    const engineError = document.getElementById('engineError');
    if (!engine.value || engine.value < 500 || engine.value > 6000) {
        engineError.textContent = 'Please enter valid engine capacity (500-6000 CC)';
        engineError.classList.add('visible');
        engine.parentElement.classList.add('error');
        isValid = false;
    } else {
        engineError.classList.remove('visible');
        engine.parentElement.classList.remove('error');
    }
    
    // Fuel Type
    const fuelType = document.getElementById('fuel_type');
    const fuelTypeError = document.getElementById('fuelTypeError');
    if (!fuelType.value) {
        fuelTypeError.textContent = 'Please select a fuel type';
        fuelTypeError.classList.add('visible');
        fuelType.parentElement.classList.add('error');
        isValid = false;
    } else {
        fuelTypeError.classList.remove('visible');
        fuelType.parentElement.classList.remove('error');
    }
    
    // Transmission
    const transmission = document.getElementById('transmission');
    const transmissionError = document.getElementById('transmissionError');
    if (!transmission.value) {
        transmissionError.textContent = 'Please select a transmission type';
        transmissionError.classList.add('visible');
        transmission.parentElement.classList.add('error');
        isValid = false;
    } else {
        transmissionError.classList.remove('visible');
        transmission.parentElement.classList.remove('error');
    }
    
    // Owner Type
    const ownerType = document.getElementById('owner_type');
    const ownerTypeError = document.getElementById('ownerTypeError');
    if (!ownerType.value) {
        ownerTypeError.textContent = 'Please select an owner type';
        ownerTypeError.classList.add('visible');
        ownerType.parentElement.classList.add('error');
        isValid = false;
    } else {
        ownerTypeError.classList.remove('visible');
        ownerType.parentElement.classList.remove('error');
    }
    
    if (!isValid) {
        showToast('warning', 'Validation Error', 'Please fix the highlighted fields');
    }
    
    return isValid;
}

// Display Prediction Result with AI Analysis
function displayPredictionResult(data, formData) {
    const resultCard = document.getElementById('resultCard');
    const resultPlaceholder = resultCard.querySelector('.result-placeholder');
    const resultContent = resultCard.querySelector('.result-content');
    
    // Hide placeholder and show content
    resultPlaceholder.classList.add('hidden');
    resultContent.classList.remove('hidden');
    
    // Update main price with animation
    animateValue('predictedPrice', 0, data.predicted_price, 1500);
    
    // Update confidence
    document.getElementById('confidence').textContent = data.confidence + '%';
    
    // Update AI Analysis
    document.getElementById('marketPrice').textContent = '₹' + data.expected_market_price.toLocaleString('en-IN');
    document.getElementById('resaleValue').textContent = '₹' + data.expected_resale_value.toLocaleString('en-IN');
    document.getElementById('depreciation').textContent = data.depreciation_percentage + '%';
    
    // Update price status badge
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = data.price_status;
    statusBadge.className = 'status-badge ' + data.price_status_color;
    
    // Update recommendation
    const recommendationElement = document.getElementById('recommendationText');
    if (recommendationElement) {
        recommendationElement.textContent = data.recommendation;
    }
    
    // Update car preview
    document.getElementById('carName').textContent = `${formData.company} ${formData.model}`;
    document.getElementById('carSpecs').textContent = `${formData.year} • ${formData.fuel_type} • ${formData.transmission} • ${formData.kilometers_driven.toLocaleString()} km`;
    document.getElementById('carAge').textContent = `Age: ${data.car_age} years`;
    
    // Update car image if uploaded
    if (uploadedImageUrl) {
        const carImageDisplay = document.getElementById('carImageDisplay');
        if (carImageDisplay) {
            carImageDisplay.innerHTML = `<img src="${uploadedImageUrl}" alt="Car" style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;">`;
        }
    }
}

// Animate number value
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    
    const timer = setInterval(() => {
        current += increment * Math.ceil(range / 100);
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = '₹' + Math.floor(current).toLocaleString('en-IN');
    }, Math.max(stepTime, 10));
}

// Dashboard Initialization
function initializeDashboard() {
    updateDashboard();
}

// Update Dashboard Statistics
async function updateDashboard() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update stat cards with animation
        animateValue('totalPredictions', 0, data.total_predictions, 1000);
        animateValue('avgPrice', 0, data.avg_price, 1000);
        document.getElementById('topBrand').textContent = data.most_predicted_company || '-';
        
        // Calculate good deals from status distribution
        const goodDeals = data.status_distribution['Underpriced'] || data.status_distribution['Good Deal'] || 0;
        document.getElementById('goodDeals').textContent = goodDeals;
        
        // Update history stats
        document.getElementById('historyTotal').textContent = data.total_predictions;
        document.getElementById('historyAvg').textContent = '₹' + data.avg_price.toLocaleString('en-IN');
        document.getElementById('historyTop').textContent = data.most_predicted_company || '-';
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// Animated Counters
function initializeAnimatedCounters() {
    // Observe stat cards for animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statValue = entry.target.querySelector('.stat-value');
                if (statValue) {
                    const value = parseFloat(statValue.textContent.replace(/[₹,]/g, ''));
                    if (!isNaN(value)) {
                        animateValue(statValue.id, 0, value, 1500);
                    }
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.stat-card').forEach(card => {
        observer.observe(card);
    });
}

// Handle Comparison
async function handleComparison() {
    console.log('[DEBUG] Starting comparison...');
    
    // Validate forms before proceeding
    const car1Form = document.getElementById('compareForm1');
    const car2Form = document.getElementById('compareForm2');
    
    if (!validateCompareForm(car1Form, 'Car 1') || !validateCompareForm(car2Form, 'Car 2')) {
        return;
    }
    
    const loadingOverlay = document.getElementById('loadingOverlay');
    const compareLoader = document.getElementById('compareLoader');
    const compareButton = document.getElementById('compareButton');
    
    loadingOverlay.classList.remove('hidden');
    compareLoader.classList.remove('hidden');
    compareButton.disabled = true;
    
    // Get car 1 data
    const car1Data = {
        company: car1Form.querySelector('.compare-company').value,
        model: car1Form.querySelector('.compare-model').value,
        year: parseInt(car1Form.querySelector('.compare-year').value),
        fuel_type: car1Form.querySelector('.compare-fuel').value,
        transmission: car1Form.querySelector('.compare-transmission').value,
        kilometers_driven: parseFloat(car1Form.querySelector('.compare-km').value),
        owner_type: car1Form.querySelector('.compare-owner').value,
        mileage: parseFloat(car1Form.querySelector('.compare-mileage').value),
        engine_capacity: parseFloat(car1Form.querySelector('.compare-engine').value)
    };
    
    // Get car 2 data
    const car2Data = {
        company: car2Form.querySelector('.compare-company').value,
        model: car2Form.querySelector('.compare-model').value,
        year: parseInt(car2Form.querySelector('.compare-year').value),
        fuel_type: car2Form.querySelector('.compare-fuel').value,
        transmission: car2Form.querySelector('.compare-transmission').value,
        kilometers_driven: parseFloat(car2Form.querySelector('.compare-km').value),
        owner_type: car2Form.querySelector('.compare-owner').value,
        mileage: parseFloat(car2Form.querySelector('.compare-mileage').value),
        engine_capacity: parseFloat(car2Form.querySelector('.compare-engine').value)
    };
    
    console.log('[DEBUG] Car 1 data:', car1Data);
    console.log('[DEBUG] Car 2 data:', car2Data);
    
    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                car1: car1Data,
                car2: car2Data
            })
        });
        
        const data = await response.json();
        console.log('[DEBUG] Comparison response:', data);
        
        if (data.success) {
            // Update individual car prices
            document.querySelector('#compareResult1 .result-price').textContent = '₹' + data.car1_price.toLocaleString('en-IN');
            document.querySelector('#compareResult2 .result-price').textContent = '₹' + data.car2_price.toLocaleString('en-IN');
            
            // Show comparison result
            const comparisonResult = document.getElementById('comparisonResult');
            comparisonResult.classList.remove('hidden');
            
            // Access nested comparison object
            const comp = data.comparison;
            document.getElementById('priceDifference').textContent = '₹' + comp.price_difference.toLocaleString('en-IN');
            document.getElementById('betterDeal').textContent = comp.better_deal;
            document.getElementById('savings').textContent = '₹' + comp.savings.toLocaleString('en-IN');
            document.getElementById('valuePerYear').textContent = '₹' + Math.max(comp.value_per_year.car1, comp.value_per_year.car2).toLocaleString('en-IN') + '/year';
            
            // Update recommendation
            const recommendationElement = document.getElementById('comparisonRecommendation');
            if (recommendationElement) {
                recommendationElement.innerHTML = `<i class="fas fa-lightbulb"></i><span>${comp.recommendation}</span>`;
            }
            
            showToast('success', 'Comparison Complete', 'Car comparison completed successfully');
        } else {
            console.error('[ERROR] Comparison failed:', data.error);
            showToast('error', 'Comparison Failed', data.error);
        }
    } catch (error) {
        console.error('[ERROR] Comparison error:', error);
        showToast('error', 'Network Error', 'An error occurred during comparison. Please try again.');
    } finally {
        loadingOverlay.classList.add('hidden');
        compareLoader.classList.add('hidden');
        compareButton.disabled = false;
    }
}

// Validate comparison form
function validateCompareForm(form, carName) {
    let isValid = true;
    
    const company = form.querySelector('.compare-company');
    const model = form.querySelector('.compare-model');
    const year = form.querySelector('.compare-year');
    const fuel = form.querySelector('.compare-fuel');
    const transmission = form.querySelector('.compare-transmission');
    const owner = form.querySelector('.compare-owner');
    const km = form.querySelector('.compare-km');
    const mileage = form.querySelector('.compare-mileage');
    const engine = form.querySelector('.compare-engine');
    
    if (!company.value) {
        showToast('error', 'Validation Error', `${carName}: Please select a company`);
        return false;
    }
    if (!model.value) {
        showToast('error', 'Validation Error', `${carName}: Please select a model`);
        return false;
    }
    if (!year.value) {
        showToast('error', 'Validation Error', `${carName}: Please select a year`);
        return false;
    }
    if (!fuel.value) {
        showToast('error', 'Validation Error', `${carName}: Please select a fuel type`);
        return false;
    }
    if (!transmission.value) {
        showToast('error', 'Validation Error', `${carName}: Please select a transmission`);
        return false;
    }
    if (!owner.value) {
        showToast('error', 'Validation Error', `${carName}: Please select an owner type`);
        return false;
    }
    if (!km.value || km.value < 0 || km.value > 500000) {
        showToast('error', 'Validation Error', `${carName}: Please enter valid kilometers (0-500000)`);
        return false;
    }
    if (!mileage.value || mileage.value < 0 || mileage.value > 50) {
        showToast('error', 'Validation Error', `${carName}: Please enter valid mileage (0-50 km/l)`);
        return false;
    }
    if (!engine.value || engine.value < 500 || engine.value > 6000) {
        showToast('error', 'Validation Error', `${carName}: Please enter valid engine capacity (500-6000 CC)`);
        return false;
    }
    
    return isValid;
}

// Load Prediction History
async function loadPredictionHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        updateHistoryUI(data.history);
        updateHistoryStats();
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Update History UI with Enhanced Table
function updateHistoryUI(history) {
    const historyItems = document.getElementById('historyItems');
    const historyTableBody = document.getElementById('historyTableBody');
    
    if (!history || history.length === 0) {
        historyItems.innerHTML = `
            <div class="no-history">
                <i class="fas fa-history"></i>
                <p>No predictions yet</p>
            </div>
        `;
        historyTableBody.innerHTML = `
            <tr>
                <td colspan="7" class="no-data">No data available</td>
            </tr>
        `;
        return;
    }
    
    // Update history items list
    historyItems.innerHTML = '';
    const recentHistory = history.slice(-10).reverse();
    
    recentHistory.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div class="history-item-icon">
                <i class="fas fa-car"></i>
            </div>
            <div class="history-item-details">
                <div class="history-item-name">${item.company} ${item.model}</div>
                <div class="history-item-specs">${item.year} • ${item.fuel_type} • ${item.kilometers_driven.toLocaleString()} km</div>
                <div class="history-item-time">${item.timestamp}</div>
            </div>
            <div class="history-item-price">₹${item.predicted_price.toLocaleString('en-IN')}</div>
        `;
        historyItems.appendChild(historyItem);
    });
    
    // Update history table
    historyTableBody.innerHTML = '';
    history.slice().reverse().forEach(item => {
        const row = document.createElement('tr');
        const statusClass = item.price_status === 'Underpriced' ? 'green' : 
                          item.price_status === 'Overpriced' ? 'red' : 'yellow';
        
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.timestamp}</td>
            <td>${item.company} ${item.model}</td>
            <td>${item.year}</td>
            <td>₹${item.predicted_price.toLocaleString('en-IN')}</td>
            <td><span class="status-badge ${statusClass}">${item.price_status}</span></td>
            <td>
                <button class="action-btn" onclick="viewPrediction(${item.id})">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        `;
        historyTableBody.appendChild(row);
    });
}

// View specific prediction (placeholder function)
function viewPrediction(id) {
    showToast('info', 'View Prediction', `Viewing prediction #${id} - Feature coming soon`);
}

// Update History Stats
async function updateHistoryStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        document.getElementById('totalPredictions').textContent = data.total_predictions;
        document.getElementById('avgPrice').textContent = '₹' + data.avg_price.toLocaleString('en-IN');
        document.getElementById('topCompany').textContent = data.most_predicted_company || '-';
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Clear History
function clearHistory() {
    if (confirm('Are you sure you want to clear prediction history?')) {
        // This would need a backend endpoint to actually clear history
        // For now, just reload the history
        loadPredictionHistory();
    }
}

// Initialize Charts with Premium Visualizations
function initializeCharts() {
    // Price Trends Chart
    const priceTrendsCtx = document.getElementById('priceTrendsChart');
    if (priceTrendsCtx) {
        priceTrendsChart = new Chart(priceTrendsCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Predicted Price',
                        data: [],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3
                    },
                    {
                        label: 'Market Price',
                        data: [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#94a3b8',
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + (value / 100000).toFixed(1) + 'L';
                            },
                            color: '#94a3b8'
                        },
                        grid: {
                            color: 'rgba(148, 163, 184, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#94a3b8'
                        },
                        grid: {
                            color: 'rgba(148, 163, 184, 0.1)'
                        }
                    }
                }
            }
        });
    }

    // Status Distribution Chart
    const statusDistCtx = document.getElementById('statusDistributionChart');
    if (statusDistCtx) {
        statusDistributionChart = new Chart(statusDistCtx, {
            type: 'doughnut',
            data: {
                labels: ['Underpriced', 'Fair Price', 'Overpriced'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#94a3b8',
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }

    // Feature Importance Chart
    const featureImpCtx = document.getElementById('featureImportanceChart');
    if (featureImpCtx) {
        featureImportanceChart = new Chart(featureImpCtx, {
            type: 'bar',
            data: {
                labels: ['Transmission', 'Engine', 'Year', 'KM Driven', 'Model', 'Company', 'Mileage', 'Owner', 'Fuel'],
                datasets: [{
                    label: 'Importance',
                    data: [48, 21, 12, 12, 2, 1, 1, 0.8, 0.6],
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(6, 182, 212, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(249, 115, 22, 0.8)'
                    ],
                    borderRadius: 8,
                    borderWidth: 0
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            color: '#94a3b8'
                        },
                        grid: {
                            color: 'rgba(148, 163, 184, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#94a3b8'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

// Update Charts with Real Data
async function updateCharts() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            // Update price trends chart
            const recentHistory = data.history.slice(-10);
            const labels = recentHistory.map((item, index) => `#${index + 1}`);
            const predictedPrices = recentHistory.map(item => item.predicted_price);
            const marketPrices = recentHistory.map(item => item.expected_market_price || item.predicted_price * 1.1);
            
            if (priceTrendsChart) {
                priceTrendsChart.data.labels = labels;
                priceTrendsChart.data.datasets[0].data = predictedPrices;
                priceTrendsChart.data.datasets[1].data = marketPrices;
                priceTrendsChart.update();
            }
            
            // Update status distribution chart
            const statusCounts = {
                'Underpriced': 0,
                'Fair Price': 0,
                'Overpriced': 0
            };
            
            data.history.forEach(item => {
                const status = item.price_status || item.deal_status;
                if (statusCounts.hasOwnProperty(status)) {
                    statusCounts[status]++;
                } else if (status === 'Good Deal') {
                    statusCounts['Underpriced']++;
                }
            });
            
            if (statusDistributionChart) {
                statusDistributionChart.data.datasets[0].data = [
                    statusCounts['Underpriced'],
                    statusCounts['Fair Price'],
                    statusCounts['Overpriced']
                ];
                statusDistributionChart.update();
            }
        }
    } catch (error) {
        console.error('Error updating charts:', error);
    }
}

// Download PDF with Enhanced Formatting
function downloadPDF() {
    const resultCard = document.getElementById('resultCard');
    const resultContent = resultCard.querySelector('.resultContent');
    
    if (!resultContent || resultContent.classList.contains('hidden')) {
        showToast('warning', 'No Prediction', 'Please make a prediction first before downloading PDF');
        return;
    }
    
    const opt = {
        margin: 10,
        filename: `car-price-prediction-${new Date().toISOString().slice(0,10)}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };
    
    showToast('info', 'Generating PDF', 'Your PDF report is being generated...');
    
    html2pdf().set(opt).from(resultCard).save().then(() => {
        showToast('success', 'PDF Downloaded', 'Your prediction report has been downloaded successfully');
    }).catch(err => {
        showToast('error', 'PDF Generation Failed', 'An error occurred while generating the PDF');
        console.error(err);
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.glass-card, .stat-card, .about-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(card);
});
