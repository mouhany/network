function saveChanges(id) {
    let oldContent = document.querySelector(`#og_${id}`);
    let editInfo = document.querySelector(`#editedStatus_${id}`);
    let editedContent = document.querySelector(`#edit_post_${id}`).value;
    let csrfToken = Cookies.get('csrftoken');

    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            content: editedContent
        })
    })
    .then(response => response.json())
    .then(result => {
        oldContent.innerHTML = result.data;
        editInfo.innerHTML = result.innerText;
    });
};


function likePost(id) {
    let likeButton = document.querySelector(`#likes_button_${id}`);
    let likeNumber = document.querySelector(`#likes_number_${id}`);
    let csrfToken = Cookies.get('csrftoken');

    fetch(`/like/${id}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
    })
    .then (response => response.json())
    .then(result => {
        if (result.is_liked) {
            likeButton.innerHTML = '<i class="fa-solid fa-heart text-danger"></i>';
            likeNumber.innerHTML = result.num_of_likes;
        } else {
            likeButton.innerHTML = '<i class="fa-regular fa-heart"></i>';
            likeNumber.innerHTML = result.num_of_likes;
        }
    });
};