

async function createorder(url, data = {}){

    var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MjUyNTE5LCJpYXQiOjE2NTQyNDg5MTksImp0aSI6IjQ2ZDgyZGE3NWJkMDQ4MWNhNjkyYzM2NjI5NDQ0OGY3IiwidXNlcl9pZCI6MX0.23s4QQzC_eFzgcv96XUAYseJ40Oaha5iA1dyWdnQfuo"
    const response = await fetch(url,{
    method: 'post',
    headers: {
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "Access-Control-Allow-Headers": "*",
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
        full_name: "mohd saquib",
        locality: "meer apartment",
        pincode: "4129",
        state: "Maharastra",
        full_name:"Mohd Saquib"
    }
    createorder(url,data).then(function(response){

        if(response.status == 200){
            var options = {
                "key": "rzp_test_TO3eDopEjDMO6e", // Enter the Key ID generated from the Dashboard
                "amount": response.amount, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Acme Corp",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                "order_id": "", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
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


    })
   
}
       

           


