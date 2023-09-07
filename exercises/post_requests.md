<!--- yes, this is an html page basically, but we want this to be embeded in our theme -->

<style>
#center {
    left: 50%;
    transform: translate(-50%, 0);
    position: absolute;
}
.novis {
    opacity: 0;
}
</style>

<div id="center">
    <iframe class="resizable" src="https://docs.google.com/presentation/d/e/2PACX-1vSDxcZLUiMhrbxYcIeYr22rcgT5JKE9CHeG5xf7Y6yaTIp1VcLFph4oBby3sEh9dw/embed?start=false&loop=false&delayms=60000" frameborder="0" width="1024px" height="576px" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
</div>
<div class="resizable nowidth novis" style="width: 1px; height: 576px;"></div> 

<script>
function resizer() {
    const LENGTH_RATIO = 9.0/16.0;
    let width = document.body.clientWidth;
    let height = 576;

    if (width < 1024) {
        height = Math.round(width * LENGTH_RATIO);
    } else {
        width = 1024;
    }

    const collection = document.getElementsByClassName("resizable");
    for (let i = 0; i < collection.length; i++) {
        if (!collection[i].className.includes("nowidth")) {
            collection[i].style.width = width + "px";
        }
        collection[i].style.height = height + "px";
    }
}

window.addEventListener("resize", resizer);
resizer()
</script>