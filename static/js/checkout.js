import {getToken} from "./csrftoken.js";
console.log(user);
const paymentInfo = document.querySelector('#payment-info')
if(shipping == 'False'){
  document.getElementById('shipping-info').innerHTML = ''
}

if(user!='AnonymousUser'){
  document.getElementById('user-info').innerHTML = ''
}

if (shipping == 'False' && user != 'AnonymousUser'){
  // Hide entire form if user is logged in and shipping is false
  document.getElementById('form-wrapper').classList.add('hidden')
  // Show payment if logged in user wants to buy an items that does not requires shipping
  paymentInfo.classList.remove('hidden')
}

const form = document.querySelector('#form')
form.addEventListener('submit',(e)=>{
  e.preventDefault()
  console.log('Form submitted...')
  document.querySelector('#form-button').classList.add('hidden')
  paymentInfo.classList.remove('hidden')
})

document.querySelector('.make-payment').addEventListener('click',submitFormData)

function submitFormData(){
  console.log('Payment button clicked')

  const userFormData = {
    'name':null,
    'email':null,
    'total':total,
  }

  const shippingInfo = {
    'address':null,
    'city':null,
    'state':total,
    'zipcode':total,
  }
  
  if(shipping != 'False'){
    shippingInfo.address = form.address.value
    shippingInfo.city = form.city.value
    shippingInfo.state = form.state.value
    shippingInfo.zipcode = form.zipcode.value
  }
  
  if(user == 'AnonymousUser'){
    userFormData.name = form.name.value
    userFormData.email = form.email.value
  }

  const url = '/process_order/'
  const csrftoken = getToken('csrftoken')
  const request = new Request(
    url,{
      method:'POST',
      headers:{
        'X-CSRFToken': csrftoken,
        'Content-Type':'application/json',
      },
      body:JSON.stringify({
        'form':userFormData,
        'shipping':shippingInfo
      }),
      mode:'same-origin',
    }
  )
  
  fetch(request)
  .then(res=>res.json())
  .then(data=>{
    console.log(data);
    window.location.href = redirectUri
  })
  
}
