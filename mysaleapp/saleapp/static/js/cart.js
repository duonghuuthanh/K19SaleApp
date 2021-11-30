function addToCart(id, name, price) {
    event.preventDefault()
    // promise
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById('cartCounter')
        counter.innerText = data.total_quantity
    }).catch(function(err) {
        console.error(err)
    })
}

function pay() {
    if (confirm('Ban chac chan muon thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        }).catch(err =>  console.error(err))
    }
}