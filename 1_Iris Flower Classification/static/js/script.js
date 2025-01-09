
document.addEventListener('DOMContentLoaded', () => {
    const predictBtn = document.getElementById('predictBtn');
    const resultSection = document.getElementById('resultSection');
    const flowerNameElem = document.getElementById('flowerName');
    const flowerImageElem = document.getElementById('flowerImage');

    // Event listener for the predict button
    predictBtn.addEventListener('click', () => {
        // Get the input values
        const sepalLength = document.getElementById('sepalLength').value;
        const sepalWidth = document.getElementById('sepalWidth').value;
        const petalLength = document.getElementById('petalLength').value;
        const petalWidth = document.getElementById('petalWidth').value;

        // Check if inputs are valid
        if (!sepalLength || !sepalWidth || !petalLength || !petalWidth) {
            alert("Please fill in all the fields.");
            return;
        }

        // Create an object with the input data
        const inputData = {
            input: [parseFloat(sepalLength), parseFloat(sepalWidth), parseFloat(petalLength), parseFloat(petalWidth)]
        };

        // Send the input data to the Flask API
        fetch('http://localhost:5000/get_flower_name', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputData)
        })
        .then(response => response.json())
        .then(data => {
            // Display the predicted flower name
            const flowerName = data.flower_name;
            flowerNameElem.textContent = flowerName;

            // Set the flower image source based on the flower name
            flowerImageElem.src = `/static/img/${flowerName}.jpg`;

            // Show the result section
            resultSection.style.display = 'block';
        })
        .catch(error => {
            alert("Error: Could not fetch prediction.");
        });
    });
});
