document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.form-tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.form-tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // Remove active class from all content
            document.querySelectorAll('.form-tab-content').forEach(c => {
                c.classList.remove('active');
            });
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const target = tab.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });
    
    // Activate first tab by default
    if (tabs.length > 0) {
        tabs[0].click();
    }
});

function updateRemoveButtonsVisibility(section) {
    const forms = document.querySelectorAll(`.${section}-form`);
    const removeButtons = document.querySelectorAll(`.remove-${section}-btn`);
    const shouldHide = forms.length <= 1;

    removeButtons.forEach(btn => {
        btn.style.display = shouldHide ? 'none' : 'block';
    });
}

function setupAddFormEvent(name) {
    const selectorClass = `.add-${name}-btn`;
    const containerClass = `.form-${name}-container`;
    const formClass = `.${name}-form`;

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelector(selectorClass)?.addEventListener('click', function () {
        const container = document.querySelector(containerClass);
            const newForm = container?.querySelector(formClass)?.cloneNode(true);

            if (newForm instanceof HTMLElement) {
                newForm.querySelectorAll('input, textarea').forEach(field => field.value = '');
                container?.appendChild(newForm);
                updateRemoveButtonsVisibility(name);
            }
        });
    });
}

function setupRemoveFormEvent(name) {
    const selectorClass = `remove-${name}-btn`;
    const formClass = `.${name}-form`;

    // Remove form
    document.addEventListener('click', function (e) {
        const target = e.target;
        if (target.classList.contains(selectorClass)) {
            const form = target.closest(formClass);
            const allForms = document.querySelectorAll(formClass);

            if (allForms.length > 1 && form) {
            form.remove();
                updateRemoveButtonsVisibility(name);
        }
        }
    });
}

const sections = ['problems', 'challenges'];

for (const section of sections) {
    setupAddFormEvent(section);
    setupRemoveFormEvent(section);
}

document.addEventListener('DOMContentLoaded', function () {
    sections.forEach(section => {
        updateRemoveButtonsVisibility(section);
    });
});
