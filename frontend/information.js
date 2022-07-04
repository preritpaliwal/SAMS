let userDatainfo = JSON.parse(localStorage.getItem('user'));
$('#manager').hide();
$('#sales').hide();
$('#clerk').hide();
if (userDatainfo.type == 'manager') {
    $('#manager').show();
    let form = document.getElementById('showcreateform');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let formdata = new FormData(form);
        formdata.append('token', localStorage.getItem('token'));
        let url = 'http://localhost:8000/addshow/';
        axios.post(url, formdata).then((res) => {
            console.log(res);
            alert('show created successfully');
            window.location.reload();
        }).catch((err) => {
            console.log(err);
            alert(err?.responser?.data?.message);
        })

    });
    let createform = document.getElementById('createsalesperson');
    createform.addEventListener('submit', (e) => {
        e.preventDefault();
        let formdata = new FormData(createform);
        formdata.append('token', localStorage.getItem('token'));
        let pass = formdata.getAll('password')[0]
        if (pass.length < 8) {
            alert('password must be atleast 8 characters long')
            return;
        }

        let url = 'http://localhost:8000/addsalesperson/';
        axios.post(url, formdata).then((res) => {
            console.log(res);
            alert('Sales Person created successfully');
            window.location.reload();
        }).catch((err) => {
            console.log(err);
            alert(err?.responser?.data?.message);

        })
    });


}
if (userDatainfo.type == 'clerk') {
    let token = localStorage.getItem('token');


    axios.get('http://localhost:8000/clerk/', { headers: { "Authorization": `${token}` } }).then((res) => {
        console.log(res.data);
        let data = res.data;
        $('#amount').text(`Total Amount Collected: ${data.amount}`);
        $('#ticketcount').text(`Total Tickets Sold: ${data.ticketcount}`);
        $('#showcount').text(`Total Shows : ${data.showcount}`);
    }).catch((err) => { console.log(err); });
    $('#clerk').show();

    let form = document.getElementById('expenditureform');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let formdata = new FormData(form);
        formdata.append('token', localStorage.getItem('token'));
        let url = 'http://localhost:8000/expenditure/';
        axios.post(url, formdata).then((res) => {
            console.log(res);
            alert('Expenditure Added successfully');
            window.location.reload();
        }).catch((err) => {
            console.log(err);
            alert(err?.responser?.data?.message);
        })

    });

}


if (userDatainfo.type == 'sales') {
    $('#sales').show();

    axios.get('http://localhost:8000/sales/', { headers: { "Authorization": `${localStorage.getItem('token')}` } }).then((res) => {
        console.log(res.data);
        let data = res.data;
        $('#commission_percent').text(`Commission : ${data.percent_commission}%`);
        $('#totalticket').text(`Total Tickets Sold: ${data.ticket_count}`);
        $('#totalcommission').text(`Total Commission : ${data.total_commission} Rs`);
        $('#totalamount').text(`Total Amount Collected: ${data.amount_collected}`);

    }).catch((err) => {
        console.log(err);
        alert(err?.response?.data?.message);
    });
}