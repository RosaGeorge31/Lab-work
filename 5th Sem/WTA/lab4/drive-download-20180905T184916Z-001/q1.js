function myFunction() {
    var x = document.getElementById("myform");
    var txt = "";
    var i;
    for (i = 0; i < x.length-1; i++) {
        txt = txt + x.elements[i].value + "<br>";
    }
    document.getElementById("display").innerHTML = txt;
}

function nameFunction(){
	var txt=""
	var x=document.getElementsByName("Name");
	var y=document.getElementsByName("City");
	var z=document.getElementsByName("Comments");
	var g=document.getElementsByName("Gender");
	txt= txt + x[0].value +"<br>" + y[0].value + "<br>" + z[0].value;
	document.getElementById("disp").innerHTML=txt;
}

