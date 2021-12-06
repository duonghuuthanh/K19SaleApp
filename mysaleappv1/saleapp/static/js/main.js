function addToCart(id, name, price) {
    fetch('/api/add-to-cart', {
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
        return res.json()
    }).then(function(data) {
        let info = document.getElementsByClassName('cart-info')
        for (let i = 0; i < info.length; i++)
            info[i].innerText = data.total_quantity
    })
}

function updateCart(id, obj) {
   fetch('/api/update-cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        let info = document.getElementsByClassName('cart-info')
        for (let i = 0; i < info.length; i++)
            info[i].innerText = data.total_quantity

        let amount = document.getElementById('amountId')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    }).catch(function(err) {
        console.error(err)
    })
}

function deleteCart(productId) {
    if (confirm("Ban chac chan xoa mat hang khong?") == true) {
        fetch('/api/cart/' + productId, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            let info = document.getElementsByClassName('cart-info')
            for (let i = 0; i < info.length; i++)
                info[i].innerText = data.total_quantity

            let amount = document.getElementById('amountId')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let p = document.getElementById('product' + productId)
            p.style.display = 'none'
        }).catch(function(err) {
            console.error(err)
        })
    }

}

function pay() {
    if (confirm("Ban chac chan thanh toan khong?") == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            console.info(data)
            if (data.code == 200)
                location.reload()
        }).catch(function(err) {
            console.info(err)
        })
    }

}