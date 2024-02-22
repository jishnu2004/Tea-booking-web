document.getElementById('loadData').addEventListener('click', function() {
    fetch('https://jsonplaceholder.typicode.com/posts/1') // Sample API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('apiResult').innerHTML = `
                <h2>${data.title}</h2>
                <p>${data.body}</p>
            `;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            document.getElementById('apiResult').innerHTML = 'Error fetching data.';
        });
});
