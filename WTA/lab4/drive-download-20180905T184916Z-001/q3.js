function validateForm() 
{
 myForm=document.getElementById('myform')
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(myForm.email.value))
  {
    return (true)
  }
  	document.getElementById('invalid').innerHTML="Invalid email id"
    return (false)
}
