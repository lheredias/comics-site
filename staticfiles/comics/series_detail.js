document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event=> {
        let element = event.target;
        if (element.id=='edit_about') {
        edit_about(element)
        }  
    }) 
    })
    
    function edit_about(element) {
        element.style.display='none'
        container=document.querySelector('#about')
        content=container.querySelector('#about_content')
        content.style.display='none'
        let placeholder=content.innerHTML
        const edit = document.createElement('div');
        let left= (1000-content.innerText.length)
        edit.innerHTML = `<div class="form-group">
        <textarea class="form-control" name="about" id="about_edited" rows="5" maxlength="1000">${placeholder}</textarea>
        </div>
            <div><small id="count">Characters left: ${left}</small></div>
            <input class="btn btn-primary" id="save" type="submit">
            <input class="btn btn-primary" id="cancel" type="submit" value="cancel">`
        container.append(edit);
        container.querySelector('#about_edited').onkeyup = function () {
            container.querySelector('#count').innerHTML = "Characters left: " + (1000 - this.value.length);
          };
        container.querySelector('#cancel').addEventListener('click',()=>{
            content.style.display = 'block'
            element.style.display='block'
            edit.remove()
        })
        container.querySelector('#save').addEventListener('click', ()=>{
            const edited = container.querySelector('#about_edited').value;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            console.log(csrftoken)
            fetch(`/edit_about`, {
                method: 'PUT',
                headers: { "X-CSRFToken": csrftoken },
                body: JSON.stringify({
                    about: edited,
                    series: element.value
                }) 
            })
            .then(()=>{
                edit.style.display = 'none'
                content.style.display = 'block'
                location.reload()
            })    
        })
    }