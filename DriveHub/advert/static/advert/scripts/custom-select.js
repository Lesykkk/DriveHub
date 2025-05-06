const allCustomSelectContainer = document.querySelectorAll('.custom-select-container');

allCustomSelectContainer.forEach(customSelectContainer =>{
    customSelectContainer.addEventListener("click", () =>{
        customSelectContainer.classList.toggle("opened");
    })
})

document.addEventListener("click", e => {
    allCustomSelectContainer.forEach(customSelectContainer =>{
        if (!customSelectContainer.contains(e.target)) {
            customSelectContainer.classList.remove("opened");
        }
    })
});

allCustomSelectContainer.forEach(customSelectContainer =>{
    const customOptionList = customSelectContainer.querySelector('.custom-option-list')
    customOptionList.addEventListener("click", (e) => {
        const clickedOption = e.target.closest('.custom-option');
        const selectedOption = customSelectContainer.querySelector('.custom-selected-option');
        const placeholder = customSelectContainer.querySelector('.custom-select-placeholder');

        customOptionList.querySelectorAll(".custom-option").forEach(opt => {
            opt.removeAttribute('selected');
        });

        if (clickedOption.classList.contains("custom-option") && !clickedOption.classList.contains("default-option")) {
            placeholder.style.display = 'none';
            selectedOption.style.display = 'flex';
            selectedOption.textContent = clickedOption.textContent;
            clickedOption.setAttribute('selected', '');
            
            const changeEvent = new CustomEvent('change', {
                detail: { 
                    isDefaultSelected: false,
                    textContent: clickedOption.textContent,
                },
                bubbles: false
            });
            customSelectContainer.dispatchEvent(changeEvent);

        } else if (clickedOption.classList.contains("default-option")) {
            placeholder.style.display = 'flex';
            selectedOption.style.display = 'none';
            selectedOption.textContent = null;

            const changeEvent = new CustomEvent('change', {
                detail: { 
                    isDefaultSelected: true,
                    textContent: null,
                },
                bubbles: false
            });
            customSelectContainer.dispatchEvent(changeEvent);
        }
    });
})

function enhanceCustomSelect(customSelectContainer) {
    const scrollContainer = customSelectContainer.querySelector('.custom-option-scroll');
    customSelectContainer._scrollContainer = scrollContainer;
    
    customSelectContainer.appendOption = function (value) {
        const option = document.createElement('div');
        option.classList.add('custom-option');
        option.innerHTML = `
            <div class="img-container">
                <img src="${customSelectContainer.getAttribute('data-icon-url')}">
            </div>
            <p class="custom-option-value">${value}</p>
        `;
        customSelectContainer._scrollContainer.appendChild(option);
    };
  
    customSelectContainer.clearOptions = function () {
        customSelectContainer._scrollContainer.innerHTML = '';
    };

    customSelectContainer.reset = function () {
        const _placeholder = customSelectContainer.querySelector('.custom-select-placeholder');
        const _selectedOption = customSelectContainer.querySelector('.custom-selected-option');
        
        _placeholder.style.display = 'flex';
        _selectedOption.style.display = 'none';
        _selectedOption.textContent = null;
    };
}

document.querySelectorAll('.custom-select-container').forEach(customSelectContainer => {
    enhanceCustomSelect(customSelectContainer);

    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'disabled') {
                mutation.target.reset();
            }
        });
    });

    observer.observe(customSelectContainer, {
        attributes: true,
        attributeFilter: ['disabled']
    });
});