import {getToken} from "./csrftoken.js";
import {getCookie} from "./cookie.js"

// elements
const cartLink = document.querySelector('#cart-link')

let cart = JSON.parse(getCookie('cart')) // Converts a JavaScript Object Notation (JSON) string into an object.
console.log('cart',cart);
if(!cart){
  cart = {}
  console.log('Cart was created!')
  document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/" // Converts a JavaScript value to a JavaScript Object Notation (JSON) string.
}
// 1. Add event listener to common parent element
// 2. Determine what element originated the event
document.querySelector('.product-group').addEventListener('click',function(e){
  // Matching strategy
  const allClass = e.target.classList
  if(allClass.contains('update-cart') ){
    console.log('click');
    const productId = e.target.dataset.product
    const action = e.target.dataset.action
    if(user=='AnonymousUser'){
      addCookieItem(productId,action)
    }else{
      updateUserOrder(productId,action)
    }
  }
})

function addCookieItem(productId,action){
  console.log('Cart Cookie');
  console.log('productId',productId)
  console.log('action',action)
  if(action == 'add'){
    // ตรวจสอบว่ามีสินค้าในตะกร้าไหม ถ้าไม่มีให้สรา้ง ถ้ามีให้อัพเดท
    if(!cart[productId]){
      cart[productId] = {'quantity':1}
    }else{
      cart[productId]['quantity']+=1
    }
  }else{
    let quantity = cart[productId]['quantity']-=1
    if(!quantity){
      console.log("remove Item");
      document.querySelector(`[data-block-product='${productId}']`).remove()
      delete cart[productId]
    }
  }
  console.log('Cart:',cart);
  document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
  const items = Object.keys(cart).reduce((value,key)=>value+cart[key].quantity,0)
  cartLink.dataset.totalItems = items
  const cartTotal = Object.keys(cart).reduce((value,key)=>value+=(cart[key].quantity*(+document.querySelector(`#price-${productId}`).dataset.price)),0)
  cartLink.dataset.totalItems = items
  if(document.querySelector('.quantity')){
  document.querySelector(`[data-quantity='${productId}']`).innerText = cart[productId]['quantity']
  document.querySelector(`[data-total='${productId}']`).innerText = (cart[productId]['quantity'] * +document.querySelector(`#price-${productId}`).dataset.price).toLocaleString()
  document.querySelector(`#summary-quantity`).innerText = items
  document.querySelector(`#summary-price`).innerText =cartTotal.toLocaleString(2)
  }
}

function updateUserOrder(productId,action){
  console.log('User is logged in, sending data...');
  console.log(productId,action);
  const csrftoken = getToken('csrftoken')
  const url = '/update_items/'
  const request = new Request(
    url,
    {
      method:'POST',
      headers:{
        'X-CSRFToken': csrftoken,
        'Content-Type':'application/json'},
      body:JSON.stringify({
        'productId': productId,
        'action': action,
      }),
      mode: 'same-origin'
    },
  )
  
  fetch(request)
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    console.log('data',data);
    cartLink.dataset.totalItems = data['cartItems']
    if(document.querySelector('.quantity')){
      document.querySelector(`[data-quantity='${productId}']`).innerText = data['quantity']
      document.querySelector(`[data-total='${productId}']`).innerText = data['totalPriceItem']
      document.querySelector(`#summary-quantity`).innerText = data['cartItems']
      document.querySelector(`#summary-price`).innerText = data['cartTotal']
      if(!data['quantity']){
        document.querySelector(`[data-block-product='${productId}']`).remove()
      }
    }
  })
}