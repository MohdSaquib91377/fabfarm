

async function createorder(url, data = {}){

    var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU1OTk2OTc4LCJpYXQiOjE2NTU5OTMzNzgsImp0aSI6ImYzZGJlMWZmN2Q4YTQ4OTA5N2RjODA1Y2YyNDQ3YWM4IiwidXNlcl9pZCI6Mn0.Kc28LQ2iSTxLklkRQVhF42XYA9W6_mhnJWNF2VCytio"
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
                "key": "rzp_test_dDKHklaSWC4N3X", // Enter the Key ID generated from the Dashboard
                "amount": `${data.amount}`, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Acme Corp",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                "order_id": `${data.razorpay_order_id}`, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){

                    window.localStorage.setItem("razorpay_payment_id",response.razorpay_payment_id);
                    window.localStorage.setItem("razorpay_order_id",response.razorpay_order_id);
                    window.localStorage.setItem("razorpay_signature",response.razorpay_signature);
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
            window.sessionStorage.setItem("error_code",response.error.code);
            window.sessionStorage.setItem("error_description",response.error.description);
            window.sessionStorage.setItem("error_source",response.error.source);
            window.sessionStorage.setItem("error_step",response.error.step);
            window.sessionStorage.setItem("error_reason",response.error.reason);
            window.sessionStorage.setItem("error_order_id",response.error.metadata.order_id);
            window.sessionStorage.setItem("error_payment_id",response.error.metadata.payment_id);

            
            });


        }


    }).catch(function(error){
        alert(error)
    })
   
}
       
 


