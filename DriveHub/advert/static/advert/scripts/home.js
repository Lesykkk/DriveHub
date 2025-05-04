const allcustomSelectContainer = document.querySelectorAll('.custom-select-container');

        allcustomSelectContainer.forEach(customSelectContainer =>{
            customSelectContainer.addEventListener("click", () =>{
                customSelectContainer.classList.toggle("opened");
            })
        })

        document.addEventListener("click", e => {
            allcustomSelectContainer.forEach(customSelectContainer =>{
                if (!customSelectContainer.contains(e.target)) {
                    customSelectContainer.classList.remove("opened");
                }
            })
        });
        
        allcustomSelectContainer.forEach(customSelectContainer =>{
            const customOptionList = customSelectContainer.querySelector('.custom-option-list')
            customOptionList.addEventListener("click", (e) => {
                const clickedOption = e.target.closest('.custom-option');
                const selectedOption = customSelectContainer.querySelector('.custom-selected-option');
                const defaultPlaceholder = customSelectContainer.querySelector('.custom-select-placeholder');
    
                customOptionList.querySelectorAll(".custom-option").forEach(opt => {
                    opt.classList.remove("selected");
                  });
    
                if (clickedOption.classList.contains("custom-option") && !clickedOption.classList.contains("default-option")) {
                    defaultPlaceholder.style.display = 'none';
                    selectedOption.style.display = 'flex';
    
                    selectedOption.textContent = clickedOption.textContent;
    
                    clickedOption.classList.add("selected");
    
                }
                else if(clickedOption.classList.contains("default-option")){
                    defaultPlaceholder.style.display = 'flex';
                    selectedOption.style.display = 'none';
                }
                
            });
        })