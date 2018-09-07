function myFunction() {
    var x = document.getElementById("myform");
    var txt = "";
    var i;
    for (i = 0; i < x.length-1; i++) {
        if(i==2 || i==3)
        {
            if(x.elements[i].checked)
                txt = txt + x.elements[i].value + "<br>";
        }
        else
        {
                txt = txt + x.elements[i].value + "<br>";

        }
}
    document.getElementById("display").innerHTML = txt;
}

function nameFunction(){
    var txt=""
    var x=document.getElementsByName("Name");
    var y=document.getElementsByName("City");
    var z=document.getElementsByName("Comments");
    var g=document.getElementsByName("Gender");
    var gender;
    if(g[0].checked)
        gender=g[0].value;
    else
        gender=g[1].value;

    txt= txt + x[0].value +"<br>" + y[0].value + "<br>" + z[0].value +"<br>" + gender;
    document.getElementById("disp").innerHTML=txt;
}

function domfunc()
{
    var txt=""
    var x=myform.name.value;
    var y=myform.city.value;
    var z=myform.comments.value;
    var g=myform.Gender.value;
    
    txt= txt + x[0].value +"<br>" + y[0].value + "<br>" + z[0].value +"<br>" + gender;
     document.getElementById("disp").innerHTML=txt;
 }