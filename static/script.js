document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('/filter_loadouts', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            resultDiv.innerHTML = data; // Update the result section with the filtered loadouts
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});