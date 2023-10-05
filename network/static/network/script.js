function saveChanges(id) {
    let oldContent = document.querySelector(`#og_${id}`)
    let editInfo = document.querySelector(`#editedStatus_${id}`)
    let csrfToken = Cookies.get('csrftoken');
    let editedContent = document.querySelector(`#edit_post_${id}`).value;

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
        oldContent.innerHTML = result.data
        editInfo.innerHTML = result.message
    });
}