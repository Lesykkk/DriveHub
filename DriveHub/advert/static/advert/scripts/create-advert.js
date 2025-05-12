document.getElementById('brand-select').addEventListener('change', function (e) {
    const modelSelect = document.getElementById('model-select');
    
    if (e.detail.isDefaultSelected) {
        modelSelect.setAttribute('disabled', '');
        modelSelect.clearOptions();
        return;
    }
    
    const brandId = e.detail.id;
    // console.log(brandId);
    modelSelect.clearOptions();
    modelSelect.reset();

    fetch(`/ajax/get-models/?brand_id=${brandId}`)
        .then(response => response.json())
        .then(models => {
            models.forEach(model => {
                modelSelect.appendOption(model.id, model.value);
            });
            modelSelect.removeAttribute('disabled');
        });
});

const input = document.getElementById('file_input');
const previewContainer = document.getElementById('file-preview-container');
const textArea = document.querySelector('.file-text-area');
const addPhotoSrc = document.getElementById('add-photo-img').src;

input.addEventListener('change', function () {
    textArea.style.display = 'none';
    previewContainer.style.display = 'flex';
    
    const photo = document.getElementById('add_photo');
    if (photo) {
        photo.remove();
    }

    const addPhotoDiv = document.createElement('div');
    const spanText = document.createElement("span");
    const svg = document.createElement("img");
    addPhotoDiv.id = 'add_photo';
    addPhotoDiv.className = "preview-div add-photo";
    spanText.textContent = "Додати фото"
    svg.src = addPhotoSrc;

    previewContainer.appendChild(addPhotoDiv);
    addPhotoDiv.appendChild(svg);
    addPhotoDiv.appendChild(spanText)
    
    let files = Array.from(this.files);
    files.forEach(file => {
        if (!file.type.startsWith('image/')) return;
        
        const reader = new FileReader();
        reader.onload = function (e) {
            const removePhotoDiv = document.createElement('div');
            const removeImg = document.createElement('img');
            const removeSrc = textArea.dataset.logoUrl;
            removeImg.src = removeSrc;
            removePhotoDiv.className = "remove-photo-div";
            removePhotoDiv.appendChild(removeImg);
            
            const previewDiv = document.createElement('div');
            previewDiv.className = "preview-div";
            
            const img = document.createElement('img');
            img.src = e.target.result;
            previewDiv.appendChild(img);
            
            previewDiv.appendChild(removePhotoDiv);

            previewContainer.appendChild(previewDiv);
            previewContainer.appendChild(addPhotoDiv);

            removePhotoDiv.addEventListener('click', function(){
                previewDiv.remove();
                input.value = '';
                if(document.querySelectorAll('.preview-div').length === 1){
                    files = files.filter(f => f !== file);
                    textArea.style.display = 'flex';
                    previewContainer.style.display = 'none';
                }
            })
    };
    reader.readAsDataURL(file);
    });
});