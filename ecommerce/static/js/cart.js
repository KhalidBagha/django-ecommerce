console.log("Hello World")

  var update_btn = document.getElementsByClassName('updatecart')
  for(var i=0;i<update_btn.length;i++){
      update_btn[i].addEventListener("click",function(){
          var product_id = this.dataset.product;
          var action = this.dataset.action;
       
          if (user === 'AnonymousUser'){
            addCookieCartItem(product_id,action)
          }
          else{
                 updateUserOrder(product_id,action)    
          }   
         })

  }

function addCookieCartItem(p_id,action){
    console.log("From Func")
    if (action == "add"){
        if (cart[p_id] == undefined){
            cart[p_id] = {'quantity':1}
        }
        else{
            cart[p_id]['quantity'] += 1  
        }
        console.log(cart)
    }

    if (action == 'remove'){
        cart[p_id]['quantity'] -=1

        if (cart[p_id]['quantity'] <= 0){
            delete cart[p_id] 
        }
    }

    document.cookie = 'cart='+JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}



function updateUserOrder(p_id,action){
    console.log(p_id,action);
    var url = "/update_orderitem/"
    fetch (url,
        {
            method:"POST",
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body: JSON.stringify({'product_id':p_id,'action':action})
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            console.log('data:',data)
            location.reload()
        })
}