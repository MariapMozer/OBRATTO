// Toast notification system
function showToast(message, type = 'error', timeout = 5000) {
    // Remove any existing toasts first
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());

    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type} fade-in`;
    
    // Create icon based on type
    const icon = document.createElement('i');
    switch(type) {
        case 'success':
            icon.className = 'bi bi-check-circle-fill';
            break;
        case 'error':
            icon.className = 'bi bi-x-circle-fill';
            break;
        case 'warning':
            icon.className = 'bi bi-exclamation-circle-fill';
            break;
        case 'info':
            icon.className = 'bi bi-info-circle-fill';
            break;
    }
    
    // Create message element
    const messageEl = document.createElement('span');
    messageEl.textContent = message;
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = () => toast.remove();
    
    // Assemble toast
    toast.appendChild(icon);
    toast.appendChild(messageEl);
    toast.appendChild(closeBtn);
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Remove after timeout
    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, timeout);
}