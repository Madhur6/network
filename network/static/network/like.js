document.addEventListener('DOMContentLoaded', function(){
    const postNodes = document.querySelectorAll("div.post");

    postNodes.forEach((postNode) => {
        likePost(postNode);
    });

    //for comments
    const commentNodes = document.querySelectorAll("div.comment");

    commentNodes.forEach((commentNode) => {
        likeComment(commentNode);
    });
});

function likePost(postNode){
    let PostId = postNode.id.split("_")[1];

    fetch(`/like_post/${PostId}`)
    .then(response => response.json())
    .then(post => {
        let csrftoken = getCookie('csrftoken');

        const btn = document.createElement('button');

        function updateButtonContent(){
            btn.className = post.liked ? "btn btn-danger btn-sm" : "btn btn-success btn-sm";
            btn.textContent = post.liked ? "unlike" : "like";
        }

        updateButtonContent();

        btn.addEventListener('click', function(){
            fetch(`/like_post/${PostId}`, {
                method: "PUT",
                body: JSON.stringify({
                    liked: !post.liked //client-side JavaScript doesn't directly change the server's database. It sends a request to the server, and then the server changes its own database.
                }),
                headers: {"X-CSRFToken": csrftoken }
            })
            .then(response => response.json())
            .then(updatedPost => {
                post = updatedPost; // Update the 'post' variable here with the new data
                updateButtonContent();
        
                console.log(post);
        
                const likeCountElement = postNode.querySelector('.like-count');
                if (likeCountElement) {
                    likeCountElement.textContent = updatedPost.likes;
                }
            })
            .catch(error => {
                alert(error);
                location.reload();
            });
        });

        postNode.querySelector('.like-btn').innerHTML = '';
        postNode.querySelector('.like-btn').appendChild(btn);
    })
    .catch(error => {
        alert(error);
        location.reload();
    });
}



//for comments
function likeComment(commentNode){
    let commentId = commentNode.id.split("_")[1];

    fetch(`/like_comment/${commentId}`)
    .then(response => response.json())
    .then(comment => {
        let csrftoken = getCookie('csrftoken');

        const btn = document.createElement('button');

        function updateButtonContent(){
            btn.className = comment.liked ? "btn btn-danger btn-sm" : "btn btn-success btn-sm";
            btn.textContent = comment.liked ? "unlike" : "like";
        }

        updateButtonContent();

        btn.addEventListener('click', function(){
            fetch(`/like_comment/${commentId}`, {
                method: "PUT",
                body: JSON.stringify({
                    liked: !comment.liked //client-side JavaScript doesn't directly change the server's database. It sends a request to the server, and then the server changes its own database.
                }),
                headers: {"X-CSRFToken": csrftoken }
            })
            .then(response => response.json())
            .then(updatedcomment => {
                comment = updatedcomment; // Update the 'comment' variable here with the new data
                updateButtonContent();
        
                console.log(comment);
        
                const likeCountElement = commentNode.querySelector('.like-count');
                if (likeCountElement) {
                    likeCountElement.textContent = updatedcomment.likes;
                }
            })
            .catch(error => {
                alert(error);
                location.reload();
            });
        });

        commentNode.querySelector('.like-btn').innerHTML = '';
        commentNode.querySelector('.like-btn').appendChild(btn);
    })
    .catch(error => {
        alert(error);
        location.reload();
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
