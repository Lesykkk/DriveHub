const allcustomSelectContainer = document.querySelectorAll('.custom-select-container');
const template = document.getElementById("model-template");


allcustomSelectContainer.forEach(customSelectContainer => {
    customSelectContainer.addEventListener("click", () => {
        customSelectContainer.classList.toggle("opened");
    })
})

document.addEventListener("click", e => {
    allcustomSelectContainer.forEach(customSelectContainer => {
        if (!customSelectContainer.contains(e.target)) {
            customSelectContainer.classList.remove("opened");
        }
    })
});

allcustomSelectContainer.forEach(customSelectContainer => {
    const customOptionList = customSelectContainer.querySelector('.custom-option-list')

    customOptionList.addEventListener("click", (e) => {
        const clickedOption = e.target.closest('.custom-option');
        const selectedOption = customSelectContainer.querySelector('.custom-selected-option');
        const defaultPlaceholder = customSelectContainer.querySelector('.custom-select-placeholder');

        const modelSelectContainer = document.getElementById('model-select');
        const modelSelect = modelSelectContainer.querySelector('.custom-option-list');
        const modelSelectList = modelSelect.querySelector('.custom-option-scroll');
        const defaultModelPlaceholder = modelSelectContainer.querySelector('.custom-select-placeholder');
        const selectedModelOption = modelSelectContainer.querySelector('.custom-selected-option');

        customOptionList.querySelectorAll(".custom-option").forEach(opt => {
            opt.classList.remove("selected");
        });

        if (clickedOption.classList.contains("custom-option") && !clickedOption.classList.contains("default-option")) {
            defaultPlaceholder.style.display = 'none';
            selectedOption.style.display = 'flex';

            selectedOption.textContent = clickedOption.textContent;

            clickedOption.classList.add("selected");

            if (customSelectContainer.id === "brand-select") {

                const brandValue = clickedOption.textContent.trim();
                fetch(`/ajax/get-models/?brand_value=${brandValue}`)
                    .then(response => response.json())
                    .then(models => {
                        modelSelectList.innerHTML = '';
                        defaultModelPlaceholder.style.display = 'flex';
                        if (selectedModelOption) {
                            selectedModelOption.style.display = 'none';
                        }

                        models.forEach(model => {
                            const clone = template.content.cloneNode(true);

                            // Вставляємо значення в <p>
                            const p = clone.querySelector(".custom-option-value");
                            p.textContent = model.value;

                            // Додаємо до контейнера
                            modelSelectList.appendChild(clone);
                        });
                    });
            }

        }
        else if (clickedOption.classList.contains("default-option")) {
            defaultPlaceholder.style.display = 'flex';
            selectedOption.style.display = 'none';

            if (customSelectContainer.id === "brand-select") {
                modelSelectList.innerHTML = '';
                defaultModelPlaceholder.style.display = 'flex';
                if (selectedModelOption) {
                    selectedModelOption.style.display = 'none';
                }
            }

        }

    });


})

