document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        //initialize new request
        const request = new XMLHttpRequest();
        const review = document.querySelector('#review').value;
        const rating = document.querySelector('#rating').value;
        
        request.open('POST', '/review');

    
        //callback function for when request completes
        request.onload = () => {

            const data = JSON.parse(request.responseText);

            if (data.success) {

            }
            else {
                
            }

        };

    };
        
});