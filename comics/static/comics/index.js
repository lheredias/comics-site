document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelector('#latest_chapters').addEventListener('click', latest_view)
    document.querySelector('#popular_series').addEventListener('click', series_view)

    let dropdown=document.querySelector('#popular_chapters')
    dropdown.addEventListener('click', event=> {
    let element = event.target;
    console.log(element.id)
    chapters_view(element.id)
    
    })
    latest_view()

    document.querySelector('#how_to').addEventListener('click', how_to)
    document.querySelector('#got_it').addEventListener('click', latest_view)

})

function how_to() {
    document.querySelector('#how_to_view').style.display = 'block';
    document.querySelector('#latest_view').style.display = 'none';
    document.querySelector('#series_view').style.display = 'none';
    document.querySelector('#chapters_view').style.display = 'none';
    document.querySelector('#jumbo').style.display = 'none';
}

window.onscroll = () => {
    if (window.innerHeight + window.scrollY == document.body.offsetHeight && 
        document.querySelector('#latest_view').style.display=='block') {
        latest_view();
    } else if (window.innerHeight + window.scrollY == document.body.offsetHeight && 
        document.querySelector('#series_view').style.display=='block') {
        series_view()
        }
}
function chapters_view(days) {
    document.querySelector('#how_to_view').style.display = 'none';
    document.querySelector('#latest_view').style.display = 'none';
    document.querySelector('#series_view').style.display = 'none';
    document.querySelector('#chapters_view').style.display = 'block';
    document.querySelector('#jumbo').style.display = 'none';


    let container=document.querySelector('#chapters_view')
    let title=container.querySelector('#title')
    title.innerHTML=''
    if (days=="1") {
        title.innerHTML=`<h3>Most popular chapters from the last 24 hours</h3>`
    } else if (days=="2") {
        title.innerHTML=`<h3>Most popular chapters from the last 48 hours</h3>`
    } else {
        title.innerHTML=`<h3>Most popular chapters from the last week</h3>`
    }
    title.className="text-center"
    container.querySelector('#chapters_view_content').innerHTML=''
    fetch(`/popular_updates?days=${days}`)
    .then(response => response.json())
    .then(data=>{
        console.log(data)
        if (data.length===0) { 
            container.querySelector('#chapters_view_content').innerHTML+="<div>No chapters found.</div>"
        } else {
        data.forEach(element=> {
            container.querySelector('#chapters_view_content').innerHTML+=
            `<div class="d-flex flex-column p-2 m-2">
            <div>
            <a href="/series/${element.title}"><img id="thumbnail" src=${element.cover} width=200 height=300 alt=""></a>
            </div>
            <div class="text-wrap mt-2" style="width: 10rem;">
                <h5>${element.title}</h5>
            </div>
            <div>
            Author: <a href="/authors/${element.author}">${element.author}</a>
            </div>
            <div>
            <small>Views: ${element.views}</small>
            </div>
            <div>
            <small>Added ${element.timestamp}</small>
            </div>
            <div>
            <a href="/series/${element.title}/${element.chap}" class="list-group-item list-group-item-action list-group-item-primary flex-column align-items-start">
                <div class="d-flex w-100 justify-content-between">
                Chapter ${element.chap}
                </div>
            </a>
            </div>
            </div>`
        })}
    })
}


let counter_latest = 0;
let counter_popular = 0;
const quantity = 9;

function latest_view() {

    const start = counter_latest;
    const end = start + quantity - 1;
    counter_latest = end + 1;

    document.querySelector('#how_to_view').style.display = 'none';
    document.querySelector('#latest_view').style.display = 'block';
    document.querySelector('#series_view').style.display = 'none';
    document.querySelector('#chapters_view').style.display = 'none';
    document.querySelector('#jumbo').style.display = 'block';


    /* document.querySelector('#latest_view').innerHTML = `<h3>HEY THEREEE</h3>`; */
    console.log('CALL')
    let container=document.querySelector('#latest_view')
    /* if (counter==1) {
        container.innerHTML+=`<h3>Latest Chapters</h3>`
    } */

    fetch(`/latest_chapters?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data=>{
        console.log(data)
        data.forEach(element=> {
            container.querySelector('#latest_view_content').innerHTML+=
            `<div class="d-flex flex-column p-2 m-2">
            <div>
            <a href="/series/${element.title}"><img id="thumbnail" src=${element.cover} width=200 height=300 alt=""></a>
            </div>
            <div class="text-wrap mt-2" style="width: 10rem;">
                <h5>${element.title}</h5>
            </div>
            <div>
            Author: <a href="/authors/${element.author}">${element.author}</a>
            </div>
            <div>
            <small>Added ${element.timestamp}</small>
            </div>
            <div>
            <a href="/series/${element.title}/${element.chap}" class="list-group-item list-group-item-action list-group-item-primary flex-column align-items-start">
                <div class="d-flex w-100 justify-content-between">
                Chapter ${element.chap}
                </div>
            </a>
            </div>
            </div>`
        })
        /* document.querySelector('#latest_view').innerHTML = 
        `<img src=${data.author} width=auto height="500" alt="">`; */

    })    
    

}

function series_view() {

    const start = counter_popular;
    const end = start + quantity - 1;
    counter_popular = end + 1;

    document.querySelector('#how_to_view').style.display = 'none';
    document.querySelector('#latest_view').style.display = 'none';
    document.querySelector('#series_view').style.display = 'block';
    document.querySelector('#chapters_view').style.display = 'none';
    document.querySelector('#jumbo').style.display = 'none';


    /* document.querySelector('#latest_view').innerHTML = `<h3>HEY THEREEE</h3>`; */
    console.log('series_view')
    let container=document.querySelector('#series_view')
    /* if (counter==1) {
        container.innerHTML+=`<h3>Latest Chapters</h3>`
    } */

    fetch(`/popular_series?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data=>{
        console.log(data)
        data.forEach(element=> {
            container.querySelector('#series_view_content').innerHTML+=
            `<div class="d-flex flex-column p-2 m-2">
            <div>
            <a href="/series/${element.title}"><img id="thumbnail" src=${element.cover} width=200 height=300 alt=""></a>
            </div>
            <div class="text-wrap mt-2" style="width: 10rem;">
                <h5>${element.title}</h5>
            </div>
            <div>
            Favorited by: ${element.favs} people
            </div>
            <div>
            Author: <a href="/authors/${element.author}">${element.author}</a>
            </div>
            
            
            </div>`
        })
        /* document.querySelector('#latest_view').innerHTML = 
        `<img src=${data.author} width=auto height="500" alt="">`; */

    })    
    

}