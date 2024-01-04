document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', editPost);
    });

});

function editPost(event) {
    let button = event.currentTarget;
    let postDiv = button.parentElement;
    let postContent = postDiv.querySelector('.post-content');
    let postId = postDiv.getAttribute('data-post-id');

    let textArea = document.createElement('textarea');
    textArea.value = postContent.textContent; 
    postContent.replaceWith(textArea);

    button.textContent = "Save";
    button.removeEventListener('click', editPost); 
    button.addEventListener('click', savePost); 

    function savePost() {
        let newContent = textArea.value;

        fetch(`/network/update_post/${postId}/`, {
            method: 'POST',
            body: JSON.stringify({
                content: newContent
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                postContent.textContent = newContent;
                textArea.replaceWith(postContent);
                button.textContent = "Edit";
                button.removeEventListener('click', savePost); 
                button.addEventListener('click', editPost); 
            } else {
                alert("Error updating the post.");
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');

            fetch(`/network/like_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')  
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                let likeCountSpan = document.getElementById(`like-count-${postId}`);
                likeCountSpan.innerHTML = `Likes: ${data.likes}`;
            
                if (button.innerHTML.trim() === "Like") {
                    button.innerHTML = "Unlike";
                } else {
                    button.innerHTML = "Like";
                }
            });
        })
    });
});

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('follow-button').addEventListener('click', function() {
        const username = document.getElementById('follow-button').getAttribute('data-username');
        fetch(`/network/profile/${username}/follow/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status == "followed") {
                document.getElementById('follow-button').textContent = "Unfollow";
            } else if (data.status == "unfollowed") {
                document.getElementById('follow-button').textContent = "Follow";
            }
            document.getElementById('followers-count').textContent = `Followers: ${data.followers_count}`;
            document.getElementById('following-count').textContent = `Following: ${data.following_count}`;
        });
    });
});