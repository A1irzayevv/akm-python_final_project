// const form = document.querySelector('form')


// form.addEventListener('submit', (e) => {
//     e.preventDefault()
//     const cve = document.querySelector('#input').value
//     const trackParagraph = document.querySelector('.track')
    
//     fetch('http://localhost:5000/', {
//         method: 'POST',
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ cve })
//     })
//     // .then((response) => {
//     //     if (!response.ok) {
//     //         throw new Error('Something went bad');
//     //     }
//     //     return response.json();
//     // }).then((data) => {
//     //     if (data.success) {
//     //         trackParagraph.textContent = data.message
//     //         trackParagraph.style.color = 'green'
//     //         trackParagraph.style.display = 'block'

//     //         window.location.href = `http://localhost:5000/fetch_cve/${cve}`
//     //     }
//     //     else {
//     //         trackParagraph.textContent = data.message
//     //         trackParagraph.style.color = 'red'
//     //         trackParagraph.style.display = 'block'
//     //     }
//     // })
// })