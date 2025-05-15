const brandSelect = document.getElementById('brand-select');

brandSelect.addEventListener('change', function (e) {
    console.log("Івент на БРЕНД спрацював");
    const modelSelect = document.getElementById('model-select');
    
    if (e.detail.isDefaultSelected) {
        modelSelect.setAttribute('disabled', '');
        modelSelect.clearOptions();
        return;
    }
    
    const brandId = e.detail.id;
    const previouslySelectedModel = modelSelect.querySelector('.hidden-input').value;
    modelSelect.clearOptions();

    fetch(`/ajax/get-models/?brand_id=${brandId}`)
        .then(response => response.json())
        .then(models => {
            models.forEach(model => {
                modelSelect.appendOption(model.id, model.value);
            });
            modelSelect.removeAttribute('disabled');
        });
});

brandSelect.triggerChangeEvent();