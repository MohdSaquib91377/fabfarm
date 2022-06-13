

async function createorder(url, data = {}){

    var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU1MTI1OTc4LCJpYXQiOjE2NTUxMjIzNzgsImp0aSI6IjliNDMyOTZjNDRhNDQ5NGQ5YjMyMjhhMmZkYjhhYTFkIiwidXNlcl9pZCI6MX0._rI8uOoobJj-QmJXabtiHxE6wlplU2_DrvkNTtPRI40"
    const response = await fetch(url,{
    method: 'post',
    headers: {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer '+token,
    },

    body: JSON.stringify(data),

    });
    return response.json()

}




document.getElementById('rzp-btn').onclick = function(e){
    e.preventDefault();
    let url = "http://localhost:8000/api/v1/order/place-order/"
    var data = {
        address: "dhsdjdsfbhjsfhjs",
        alternate_number: "123456788",
        city: "Mumbai",
        country: "India",
        landmark:"Meer Apartment",
        full_name: "mohd saquib",
        locality: "meer apartment",
        pincode: "4129",
        state: "Maharastra",
        full_name:"Mohd Saquib",
        payment_mode:"razor_pay",
    }
    createorder(url,data).then(function(data){
        if(data.status == "200"){
            var options = {
                "key": "rzp_test_5nmqymdWIq7XjJ", // Enter the Key ID generated from the Dashboard
                "amount": `${data.amount}`, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Acme Corp",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                "order_id": `${data.razorpay_order_id}`, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
                alert(JSON.stringify(response));

                    alert(response.razorpay_payment_id);
                    alert(response.razorpay_order_id);
                    alert(response.razorpay_signature);
                },
                "prefill": {
                    "name": "Gaurav Kumar",
                    "email": "gaurav.kumar@example.com",
                    "contact": "9999999999"
                },
                "notes": {
                    "address": "Razorpay Corporate Office"
                },
                "theme": {
                    "color": "#3399cc"
                }

                
            };
            var rzp1 = new Razorpay(options);
            rzp1.open()
            rzp1.on('payment.failed', function (response){
            alert(response.error.code);
            alert(response.error.description);
            alert(response.error.source);
            alert(response.error.step);
            alert(response.error.reason);
            alert(response.error.metadata.order_id);
            alert(response.error.metadata.payment_id);
            });


        }


    }).catch(function(error){
        alert(error)
    })
   
}
       
 


