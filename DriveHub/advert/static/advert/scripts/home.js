document.getElementById('brand-select').addEventListener('change', function (e) {
    const modelSelect = document.getElementById('model-select');
    
    if (e.detail.isDefaultSelected) {
        modelSelect.setAttribute('disabled', '');
        modelSelect.clearOptions();
        return;
    }
    
    const brandId = e.detail.id;
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