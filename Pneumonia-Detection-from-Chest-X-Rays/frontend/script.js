function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    document.getElementById("preview").src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            `${data.result} (Confidence: ${data.confidence}%)`;
    })
    .catch(err => console.error(err));
}
