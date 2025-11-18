document.addEventListener("DOMContentLoaded", () => {
    // --- Get DOM Elements ---
    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const fileNameSpan = document.getElementById("file-name-span");
    const loadingSpinner = document.getElementById("loading-spinner");
    const resultsContainer = document.getElementById("results-container");
    const resultsGrid = document.querySelector(".results-grid");
    const errorMessage = document.getElementById("error-message");

    // --- Event Listener for File Input ---
    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            fileNameSpan.textContent = fileInput.files[0].name;
            fileNameSpan.style.fontStyle = "normal";
        } else {
            fileNameSpan.textContent = "Click to select a document...";
            fileNameSpan.style.fontStyle = "italic";
        }
    });

    // --- Event Listener for Form Submission ---
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Stop the form from submitting normally

        const file = fileInput.files[0];
        if (!file) {
            showError("Please select a file to analyze.");
            return;
        }

        // --- Start loading ---
        hideAllMessages();
        loadingSpinner.classList.remove("hidden");

        const formData = new FormData();
        formData.append("file", file);

        try {
            // --- Send file to Flask backend API ---
            const response = await fetch("/analyze", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            // --- Stop loading ---
            loadingSpinner.classList.add("hidden");

            if (!response.ok) {
                // Show error from server
                showError(data.error || "An unknown error occurred.");
            } else {
                // --- Show results ---
                displayResults(data);
                resultsContainer.classList.remove("hidden");
            }

        } catch (error) {
            loadingSpinner.classList.add("hidden");
            showError("Failed to connect to the server. Please check your connection and try again.");
            console.error("Fetch Error:", error);
        }
    });

    function displayResults(data) {
        // Clear old results
        resultsGrid.innerHTML = "";

        // Format data for display
        const displayData = [
            { title: "File Name", value: data.file },
            { title: "Sentiment", value: data.sentiment },
            { title: "Categories", value: data.categories.split(',').join('<br>') },
            { title: "Entities", value: data.entities.split(',').join('<br>') },
            { title: "Keywords", value: data.keywords.split(', ').join(', ') }
        ];

        // Create new result items
        displayData.forEach(item => {
            const itemElement = document.createElement("div");
            itemElement.classList.add("result-item");
            
            // Use textContent for plain text and innerHTML for HTML-formatted text
            const valueSpan = document.createElement("span");
            if (item.title === "Categories" || item.title === "Entities") {
                valueSpan.innerHTML = item.value || "N/A";
            } else {
                valueSpan.textContent = item.value || "N/A";
            }

            itemElement.innerHTML = `<strong>${item.title}</strong>`;
            itemElement.appendChild(valueSpan);
            resultsGrid.appendChild(itemElement);
        });
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove("hidden");
    }

    function hideAllMessages() {
        errorMessage.classList.add("hidden");
        resultsContainer.classList.add("hidden");
    }
});