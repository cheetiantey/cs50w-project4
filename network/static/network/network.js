document.addEventListener('DOMContentLoaded', function() {

    
    document.querySelectorAll('.edit').forEach(b => {
        console.log(b);
        b.onclick = function() {
            if (this.innerHTML !== 'Edit') {
                var form = new FormData();
                form.append('content', this.parentElement.childNodes[3].value);
                form.append('post_id', this.id.slice(4));
                
                fetch("/edit", {
                    method: 'POST',
                    body: form,
                })
                .then(() => {
                    var original_content = this.parentElement.childNodes[3];
                    var new_content = document.createElement('p');
                    new_content.innerHTML = original_content.value;
                    new_content.className = 'card-text';
                    original_content.parentNode.replaceChild(new_content, original_content);
                    
                    this.innerHTML = 'Edit';
                })

            } else {
                var old_content = this.parentElement.childNodes[3];
                var new_content = document.createElement("textarea");
                new_content.innerHTML = old_content.innerHTML;
                new_content.className = 'form-control';
                old_content.parentNode.replaceChild(new_content, old_content);
                
                this.innerHTML = 'Submit';
                
            }
        };
    });
    
    document.querySelectorAll('.like').forEach(b => {
        console.log(b);
        b.onclick = function() {
            const post = this.dataset.post
            const likes = document.querySelector(`#span${post}`);

            fetch(`/like/${post}`)
            .then(() => {
                const current_likes = parseInt(likes.innerHTML)
                if (this.innerHTML === 'Like') {
                    this.innerHTML = 'Unlike';
                    likes.innerHTML =  current_likes + 1;
                } else {
                    this.innerHTML = 'Like';
                    likes.innerHTML = current_likes - 1;
                }
            });
        };
    });

    document.querySelector('#follow').onclick = () => {
        const b = document.querySelector('#follow');
        const followers = document.querySelector('#followers');
        
        fetch(`/follow/${b.dataset.id}`)
        .then(() => {
            const current_followers = parseInt(followers.innerHTML);
            if (b.innerHTML !== 'Follow') {
                followers.innerHTML = current_followers - 1;
                b.innerHTML = 'Follow';
                
            } else {
                followers.innerHTML = current_followers + 1;
                b.innerHTML = 'Unfollow';
            }
        });
    };


  });