const formButtons = document.querySelectorAll('.form-button');

document.getElementById('brand-select').addEventListener('change', function (e) {
    const modelSelect = document.getElementById('model-select');
    
    if (e.detail.isDefaultSelected) {
        modelSelect.setAttribute('disabled', '');
        modelSelect.clearOptions();
        return;
    }
    
    const brandValue = e.detail.textContent.trim();
    modelSelect.clearOptions();
    modelSelect.reset();

    fetch(`/ajax/get-models/?brand_value=${brandValue}`)
        .then(response => response.json())
        .then(models => {
            models.forEach(model => {
                modelSelect.appendOption(model.value);
            });
            modelSelect.removeAttribute('disabled');
        });
});

formButtons.forEach(formButton => {
    formButton.addEventListener('click', e => {
        clearSelected();
        formButton.classList.toggle("selected");
        
    })
})

function clearSelected(){
    formButtons.forEach(formButton => {
        formButton.classList.remove("selected");
    })
}