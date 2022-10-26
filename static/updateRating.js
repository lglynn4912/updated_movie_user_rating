const formInputs = {
    movieId: document.querySelector('#movie-id').value,
    userId: document.querySelector('#user_id').value,
    score: document.querySelector('#new-rate').value
};


document.querySelector('#new-rate-input').addEventListener('submit', (evt) => {
    evt.preventDefault();

    fetch(`/updaterating/${movieId}`,{ 
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers:{'Content-Type': 'application/json'},
    }).then((response) => response.json())
        .then((result) => {
            document.querySelector('#current-score').innerText = result.score
    });
});