document.addEventListener('DOMContentLoaded', function() {

document.addEventListener('click', event=> {
    let element = event.target;
    if (element.id=='edit') {
    edit_bio(element)
    }  
}) 
})

function edit_bio(element) {
    element.style.display='none'
    container=document.querySelector('#bio')
    content=container.querySelector('#bio_content')
    content.style.display='none'
    let placeholder=content.innerHTML
    const edit = document.createElement('div');
    let left= (250-content.innerText.length)
    edit.innerHTML = `<div class="form-group">
    <textarea class="form-control" name="bio" id="bio_edited" rows="3" maxlength="250">${placeholder}</textarea>
    </div>
        <div><small id="count">Characters left: ${left}</small></div>
        <input class="btn btn-primary" id="save" type="submit">
        <input class="btn btn-primary" id="cancel" type="submit" value="cancel">`
    container.append(edit);
    container.querySelector('#bio_edited').onkeyup = function () {
        container.querySelector('#count').innerHTML = "Characters left: " + (250 - this.value.length);
      };
    container.querySelector('#cancel').addEventListener('click',()=>{
        content.style.display = 'block'
        element.style.display='block'
        edit.remove()
    })
    container.querySelector('#save').addEventListener('click', ()=>{
        const edited = container.querySelector('#bio_edited').value;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        console.log(csrftoken)
        fetch(`/edit_bio`, {
            method: 'PUT',
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                bio: edited,
            }) 
        })
        .then(()=>{
            edit.style.display = 'none'
            content.style.display = 'block'
            location.reload()
        })    
    })
}