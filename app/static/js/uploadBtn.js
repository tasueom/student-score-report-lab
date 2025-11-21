function toggleUpload(type) {
    const csvForm = document.getElementById('csv-upload-form');
    const jsonForm = document.getElementById('json-upload-form');
    const imgForm = document.getElementById('img-upload-form');
    
    if (type === 'csv') {
        if (csvForm.classList.contains('show')) {
            csvForm.classList.remove('show');
        } else {
            csvForm.classList.add('show');
            jsonForm.classList.remove('show');
            imgForm.classList.remove('show');
        }
    } else if (type === 'json') {
        if (jsonForm.classList.contains('show')) {
            jsonForm.classList.remove('show');
        } else {
            jsonForm.classList.add('show');
            csvForm.classList.remove('show');
            imgForm.classList.remove('show');
        }
    } else if (type === 'img') {
        if (imgForm.classList.contains('show')) {
            imgForm.classList.remove('show');
        } else {
            imgForm.classList.add('show');
            csvForm.classList.remove('show');
            jsonForm.classList.remove('show');
        }
    }
}

