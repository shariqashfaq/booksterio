alert("js working");

document.addEventListener('DOMContentLoaded', () => {
    alert("js working");

    document.querySelector('#form').onsubmit = () => {
        alert("executing form submit");

        //initialize new request
        const request = new XMLHttpRequest();
        const review = document.querySelector('#review').value;
        const rating = document.querySelector('#rating').value;
        
        request.open('POST', '/review');

    
        //callback function for when request completes
        request.onload = () => {

            const data = JSON.parse(request.responseText);

            if (data.success) {
                const contents = data.review 'by' data.username ;
                const li = document.createElement('li');
                li.innerHTML = contents;

                //add to unordered list
                document.querySelector('#reviews').append(li);

                //clear input field
                document.querySelector("review").value = '';
            }
            else {
                alert("You have already submitted a review for this book.");
            }

        };

        //add form data to send with request
        const data = new FormData;
        data.append('review', review);
        data.append('rating', rating);

        //send request
        request.send(data);
        return false;

    
    };
        
});