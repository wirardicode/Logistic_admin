//script untuk menghubungan backend
document.getElementById('myForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Mencegah submit form secara default

    const formData = new FormData(event.target);

    // Kirim data ke endpoint /surat-tugas
    let response = await fetch('http://127.0.0.1:8000/surat-tugas', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'surat_tugas.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Kirim data ke endpoint /simpanFirestore
    response = await fetch('http://127.0.0.1:8000/simpanFirestore', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        alert('Data saved successfully to Firestore');
    } else {
        alert('Failed to save data to Firestore');
    }
});