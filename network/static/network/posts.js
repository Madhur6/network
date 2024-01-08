function deletePost(postNode){
    let deleteButton = postNode.querySelector(".delete-modal .modal-footer .modal-delete");
    if (deleteButton !== null){
        deleteButton.addEventListener("click", () => {
            let csrftoken = getCookie("csrftoken");
            // Split("_")[1] part is splitting the id string into an array of substrings, divided by the underscore character ("_"). The [1] is then accessing the second element of this array.
            let PostId = postNode.id.split("_")[1]; //postNode.id.substr(5)

            // console.log(PostId);

            fetch(`/new_post_comment/post`, {
                method: "DELETE",
                body: JSON.stringify({
                    id: PostId
                }),
                headers: {"X-CSRFToken": csrftoken}
            })
            .then(async (response) => {
                if(response.status === 204){
                    console.log(`post id: ${PostId} deleted successfully`);
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

    editPost(postNode);
}

function editPost(postNode){
    let modalDialog = postNode.querySelector(".edit-modal");

    if (modalDialog !== null){
        $(modalDialog).on("show.bs.modal", () => {
            //Get save button and modal body
            let saveButton = modalDialog.querySelector(".modal-footer > .btn-primary");
            let modalBody = modalDialog.querySelector(".modal-body");

            //Get post id
            const PostId = postNode.id.split("_")[1];

            //Get content of post to be edited
            let contentNode = postNode.querySelector("div.post-content");
            const contentInnerText = contentNode.textContent.trim();

            modalBody.innerHTML = `<textarea class="new-content form-control">${contentInnerText}</textarea>`;

            //update after saving
            saveButton.addEventListener("click", () => {
                const submittedContent = modalBody.querySelector("textarea.new-content").value.trim();

                let csrftoken = getCookie("csrftoken");

                //hide modal
                $(modalDialog).modal("hide");

                //Send PUT request
                fetch(`/new_post_comment/post`, {
                    method: "PUT",
                    body: JSON.stringify({
                        id: PostId,
                        content: submittedContent,
                    }),
                    headers: {"X-CSRFToken": csrftoken}
                })

                .then(async (response) => {
                    //if success - update post's data
                    if(response.status === 201){
                        console.log(`post id: ${PostId} edited successfully`);
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


function showMore(postNode){
    const shortContent = postNode.querySelector(".post-content");
    const showMoreButton = postNode.querySelector(".show-more-button");


    //Check if the elements exist on the page
    if (!shortContent || !showMoreButton) {
        return;
    }

    showMoreButton.addEventListener('click', function(){
        console.log('clicked');
        let para = this.previousElementSibling;
        para.classList.toggle("collapsed");

        if (para.classList.contains("collapsed")){
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