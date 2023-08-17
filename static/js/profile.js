
    // Get the copy button and phone number elements
    const copyButton = document.getElementById('copy-phone');
    const phoneNumber = document.getElementById('phone-number');

    // Add a click event listener to the copy button
    copyButton.addEventListener('click', () => {
        // Select the phone number text
        phoneNumber.select();
        phoneNumber.setSelectionRange(0, 99999); // For mobile devices

        // Copy the text to the clipboard
        document.execCommand('copy');

        // Show the "Copied" signal for 2 seconds
        const signal = document.createElement('span');
        signal.textContent = 'Copied';
        signal.classList.add('text-success', 'ms-2');
        copyButton.parentElement.appendChild(signal);
        setTimeout(() => signal.remove(), 2000);
    });