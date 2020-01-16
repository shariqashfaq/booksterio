document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        //initialize new request
        const request = new XMLHttpRequest();
        const review = document.querySelector('#review').value;
        const title = document.querySelector('#title').value;
        request.open('POST', '/review');

    };

});