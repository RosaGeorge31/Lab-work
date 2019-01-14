var images = ['nitk1.png','nitk2.jpg','nitk3.jpg'];
var index = 0;
var the_image = document.getElementById("main-image");

function show_image(direction)
{
  if (direction == "left")
  {
    index--;
  }
  else
  {
    index++;
    index %= images.length;
  }
  
  if (index < 0)
  {
    index = images.length - 1;
  }
  document.getElementById("main-image").src= images[index];
}