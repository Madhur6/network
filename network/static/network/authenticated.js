document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('div.post').forEach((postNode) => {
        deletePost(postNode);
        editPost(postNode);
        showMore(postNode);
    });

    document.querySelectorAll('div.comment').forEach((commentNode) => {
        deleteComment(commentNode);
        editComment(commentNode);
        showMoreComment(commentNode);
    });
})