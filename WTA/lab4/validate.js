function validate()
{   
    if(document.myform.fn.value=="")
    {
        alert("Enter proper first name!");
        document.myform.fn.focus();
        return false;
    }
    if(document.myform.ln.value=="")
    {
        alert("Enter proper last name!");
        document.myform.ln.focus();
        return false;
    }
    var email=document.myform.e.value;
    at=email.indexOf('@');
    dot=email.lastIndexOf('.');
    if(at<1||(dot-at<2))
    {
        alert("Enter valid email!");
        document.myform.e.focus;
        return false;
    }
    var radioVals=document.getElementsByName("gender");
    var i=0,selected=false;
    while(!selected&&i<radioVals.length)
    {
        if(radioVals[i].checked)selected=true;
        i++;
    }
    if(!selected)
    {
        alert("Enter some gender!");
    }
    if(selected)
    {
        alert('success');
    }
    return selected;
}
