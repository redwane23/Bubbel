function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(";");
        for (let i= 0;i<cookies.length;i++){
            const cookie=cookies[i].trim();
            if(cookie.substring(0,name.length + 1) ===  (name+ '=' )){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken=getCookie("csrftoken")
window.onload = function(){
    fetchCartItems()
    fetchWisistItems()
    getpricetopay(CartId)
}


function changequantity(itemId,action){
    const quantityElementId ='quantity-' + itemId ;
    const total_item_priceEelementId ='total_item_price-' + itemId;
    const itemElementId='item-' + itemId

    const quantityElement=document.getElementById(quantityElementId);
    let quantity = parseInt(quantityElement.innerText,10);

fetch("/api/update-quantity/",{ 
    method:'POST',
    headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({ 
        id : itemId,
        action:action,
    })
    })
    .then(responce => responce.json())
    .then( data => {
        document.getElementById(quantityElementId).innerText=data.new_quantity;
        document.getElementById(total_item_priceEelementId).innerText=data.new_total_item_price;
        document.getElementById('price_to_pay').innerText=data.new_price_to_pay;
        if(action=='Remove'){
                            document.getElementById(itemElementId).remove()
        }
        if(data.new_quantity==0){
            document.getElementById(itemElementId).remove()
        }
    })
}

function fetchWisistItems(){
    fetch("/api/getWishlistItem/", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            let wishList = document.getElementsByClassName('wishlist_list')[0];
            wishList.innerHTML = ''; 

            let P = document.createElement('p');
            P.textContent="Wish List"
            P.className='ItemP'
            wishList.appendChild(P);
            data.itemsdata.forEach(item => {

                const itemDiv = document.createElement('div');
                itemDiv.className = 'item';
                itemDiv.id = `item-${item.id}`;
                
                itemDiv.innerHTML = `
                <p class="item-name">${item.product}</p>
                <button style="color: red ; border: 1px solid red; border-radius: 10px;" onclick="DeletWishListItem(${item.id})">Remove</button>
                `;
                wishList.appendChild(itemDiv);
            });
        } else {
            console.error("Failed to fetch items:", data.message);
        }
    })
    .catch(error => {
        console.error("Error fetching cart items:", error);
    })
}

function DeletWishListItem(itemId){
    fetch("/api/DeletWishListItem/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({
            itemid:itemId,
        })
    })
    fetchWisistItems()
}

function ordered(){
    fetch("/api/ordered/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
    })
    location.reload()
    fetchCartItems();
    getpricetopay(CartId);
}