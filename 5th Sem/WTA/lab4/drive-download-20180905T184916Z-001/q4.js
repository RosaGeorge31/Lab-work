function sum(){
	var x=document.getElementsByName("item1");
	var y=document.getElementsByName("item2");
	var z=document.getElementsByName("item3");
	var total=parseInt(x[0].value,10)+parseInt(y[0].value,10)+parseInt(z[0].value,10)
	document.getElementById("total").value=total;
}