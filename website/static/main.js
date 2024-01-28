async function predict() {
    const fileInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const resultDiv = document.getElementById('result');

    const file = fileInput.files[0];

    if (file) {
        const imageUrl = URL.createObjectURL(file);
        imagePreview.innerHTML = `<img src="${imageUrl}" alt="Uploaded Image" style="max-width:100%">`;

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            resultDiv.innerText = `Prediction: ${result.prediction}`;
        } catch (error) {
            console.error('Error predicting:', error);
        }
    } else {
        alert('Please select an image.');
    }
}
