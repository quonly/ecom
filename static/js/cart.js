// 1. Add event listener to common parent element
// 2. Determine what element originated the event
document.querySelector('.product-group').addEventListener('click',function(e){
  // Matching strategy
  if(e.target.classList.contains('update-cart')){
    const productId = e.target.dataset.product
    const action = e.target.dataset.action
    if(user=='AnonymousUser'){
      console.log('AnonymousUser');
    }else{
      updateUserOrder(productId,action)
    }
  }
})

function updateUserOrder(productId,action){
  console.log('User is logged in, sending data...');
  console.log(productId,action);
  const url = '/update_items/'

  const request = new Request(
    url,
    {
      method:'POST',
      headers:{
        'X-CSRFToken': csrftoken,
        'Content-Type':'application/json'},
        mode: 'same-origin'
    }
  )
  
  fetch(request)
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    console.log('data',data);
  })
}