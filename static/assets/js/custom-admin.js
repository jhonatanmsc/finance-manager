document.addEventListener('DOMContentLoaded', function () {
    const starRating = document.querySelector('.field-avaliacao');
    if (starRating) {
        const inputs = starRating.querySelectorAll('input[type="radio"]');
        const labels = starRating.querySelectorAll('label');

        labels.forEach((label, index) => {
            label.addEventListener('mouseover', () => {
                const value = inputs[index].value;
                label.title = `${value} estrelas`; // Exibe o valor no hover
            });
        });
    }
});
