document.getElementById('brand-select').addEventListener('change', function () {
    const brandValue = this.value;
    const modelSelect = document.getElementById('model-select');

    modelSelect.innerHTML = '<option disabled selected>Виберіть марку</option>';

    fetch(`/ajax/get-models/?brand_value=${brandValue}`)
        .then(response => response.json())
        .then(models => {
            
            models.forEach(model => {
                const option = document.createElement('option');
                option.textContent = model.value;
                modelSelect.appendChild(option);
            });
            modelSelect.disabled = false;
        });
});

const input = document.getElementById('file_input');
const previewContainer = document.getElementById('file-preview-container');
const textArea = document.querySelector('.file-text-area');

input.addEventListener('change', function () {
    textArea.style.display = 'none';
    previewContainer.style.display = 'flex';
    
    const photo = document.getElementById('add_photo');
    if(photo){
        photo.remove();
    }

    const addPhotoDiv = document.createElement('div');
    const spanText = document.createElement("span");
    const svg = document.createElement("img");
    addPhotoDiv.id = 'add_photo';
    addPhotoDiv.className = "preview-div add-photo";
    spanText.textContent = "Додати фото"
    svg.src = "{% static 'advert/icons/add-photo.png' %}";

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
            removeImg.src = "{% static 'advert/icons/remove.svg' %}";
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