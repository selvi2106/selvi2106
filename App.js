App.js – Optional JavaScript Enhancements
javascript
Copy
Edit
// App.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("Dashboard loaded successfully");

    // Example: Scroll to predictions table
    const scrollBtn = document.getElementById("scroll-to-table");
    if (scrollBtn) {
        scrollBtn.addEventListener("click", function () {
            const tableSection = document.querySelector(".prediction-table");
            if (tableSection) {
                tableSection.scrollIntoView({ behavior: "smooth" });
            }
        });
    }

    // Example: Show alert if plot failed to load
    const img = document.querySelector(".prediction-plot img");
    if (img) {
        img.onerror = function () {
            alert("Failed to load prediction plot.");
        };
    }
});
How to Use It
Save this file as:

arduino
Copy
Edit
/static/js/App.js
Link it in your HTML (Htmlcode.html) before the closing </body> tag:

html
Copy
Edit
<script src="{{ url_for('static', filename='js/App.js') }}"></script>
