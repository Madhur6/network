function deleteComment(commentNode){
    let deleteButton = commentNode.querySelector(".delete-modal .modal-footer .modal-delete");
    if (deleteButton !== null){
        deleteButton.addEventListener("click", () => {
            let csrftoken = getCookie("csrftoken");
            // Split("_")[1] part is splitting the id string into an array of substrings, divided by the underscore character ("_"). The [1] is then accessing the second element of this array.
            let commentId = commentNode.id.split("_")[1]; //commentNode.id.substr(5)

            // console.log(commentId);

            fetch(`/new_post_comment/comment`, {
                method: "DELETE",
                body: JSON.stringify({
                    id: commentId
                }),
                headers: {"X-CSRFToken": csrftoken}
            })
            .then(async (response) => {
                if(response.status === 204){
                    console.log(`comment id: ${commentId} deleted successfully`);
                    location.reload();
                }
                else{
                    let response_body = await response.json();
                    throw new Error(response_body.error);
                }
            })
            .catch(error => {
                alert(error);
                location.reload();
            });
        });
    }

    editComment(commentNode);
}

function editComment(commentNode){
    let modalDialog = commentNode.querySelector(".edit-modal");

    if (modalDialog !== null){
        $(modalDialog).on("show.bs.modal", () => {
            //Get save button and modal body
            let saveButton = modalDialog.querySelector(".modal-footer > .btn-primary");
            let modalBody = modalDialog.querySelector(".modal-body");

            //Get comment id
            const commentId = commentNode.id.split("_")[1];

            //Get content of comment to be edited
            let contentNode = commentNode.querySelector("div.comment-content");
            const contentInnerText = contentNode.textContent.trim();

            modalBody.innerHTML = `<textarea class="new-content form-control">${contentInnerText}</textarea>`;

            //update after saving
            saveButton.addEventListener("click", () => {
                const submittedContent = modalBody.querySelector("textarea.new-content").value.trim();

                let csrftoken = getCookie("csrftoken");

                //hide modal
                $(modalDialog).modal("hide");

                //Send PUT request
                fetch(`/new_post_comment/comment`, {
                    method: "PUT",
                    body: JSON.stringify({
                        id: commentId,
                        content: submittedContent,
                    }),
                    headers: {"X-CSRFToken": csrftoken}
                })

                .then(async (response) => {
                    //if success - update comment's data
                    if(response.status === 201){
                        console.log(`comment id: ${commentId} edited successfully`);
                        contentNode.innerHTML = submittedContent;
                    }
                    //if error - show alert
                    else{
                        let response_body = await response.json();
                        throw new Error(response_body.error);
                    }
                })
                .catch(error => {
                    alert(error);
                    location.reload();
                })
            });
        });
    }
}


function showMoreComment(commentNode){
    const shortContent = commentNode.querySelector(".comment-content");
    const showMoreButton = commentNode.querySelector(".show-more-button-comment");


    //Check if the elements exist on the page
    if (!shortContent || !showMoreButton) {
        return;
    }

    showMoreButton.addEventListener('click', function(){
        console.log('clicked');
        let para = this.previousElementSibling;
        para.classList.toggle("collapsed2");

        if (para.classList.contains("collapsed2")){
            this.innerText = 'show-less';
        }
        else{
            this.innerText = 'show-more';
        }
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}