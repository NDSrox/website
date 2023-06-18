const coords = { x: 0, y: 0 };
const circles = document.querySelectorAll(".circle");
    //Copy-pasted from another website
//fire
//const colors = ["#ffb56b", "#fdaf69", "#f89d63", "#f59761", "#ef865e", "#ec805d", "#e36e5c", "#df685c", "#d5585c", "#d1525c", "#c5415d", "#c03b5d", "#b22c5e", "#ac265e", "#9c155f", "#950f5f", "#830060", "#7c0060", "#680060", "#60005f", "#48005f", "#3d005e"];

//ice
const colors = ["#0062ff", "#0067ff", "#006cff", "#0071ff", "#0076ff", "#007aff", "#007fff", "#0083ff", "#0087ff", "#008bff", "#008fff", "#0093ff", "#0097ff", "#009aff", "#009eff", "#00a2ff", "#00a5ff", "#00a9ff", "#00acff", "#00afff", "#00b3ff", "#00b6ff", "#00b9ff", "#00bcff", "#00bfff", "#00c3ff", "#00c6ff", "#00c9ff", "#00ccff", "#00cfff", "#00d1ff", "#00d4ff", "#00d7ff", "#00daff", "#00ddff", "#00dfff", "#00e2ff", "#00e5ff", "#00e7ff", "#00eaff"];

circles.forEach(function (circle, index) {
    circle.x = 0;
    circle.y = 0;
        //Changes the color of the circle. The index thingy makes sure it does not go out of range.
    circle.style.backgroundColor = colors[index % colors.length];
});

window.addEventListener("mousemove", function(e){
  coords.x = e.clientX;
  coords.y = e.clientY;
  console.log(coords);
});

function animateCircles() {
    let x = coords.x;
    let y = coords.y;
    circles.forEach(function (circle, index) {
    //Ofset the circels by -12px in both directions so that they are centered
    circle.style.left = x - 4 + "px";
    circle.style.top = y - 4 + "px";
    	//Makes the next circle a bit smaller
    circle.style.scale = (circles.length - index) / circles.length;
		
    circle.x = x;
    circle.y = y;
		//Ofsets the circles
    const nextCircle = circles[index + 1] || circles[0];
    x += (nextCircle.x - x) * 0.01;
    y += (nextCircle.y - y) * 0.01;
  });
	    //Makes sure that the circles do not get stuck ungrouped when you move the mouse off the page
    requestAnimationFrame(animateCircles);
}
animateCircles();
