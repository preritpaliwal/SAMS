
window.jsPDF = window.jspdf.jsPDF
let show = () => {


    url = 'http://localhost:8000/getshow/';
    // $('.allshow').html('loading....');
    axios.get(url).then(res => {
        console.log(res.data);
        if (res.data.length == 0) {
            $('.allshow').html('no data found');
            return;
        }

        let row = document.querySelector('.allshow');
        res.data.map(data => {
            let html = `

<div class="col-lg-4" >
    <div class="card mb-5 mb-lg-0">
        <div class="card-body">
            <h5 class="card-title text-muted text-uppercase text-center" style="font-weight:bolder">
                ${data.name}
            </h5>
            <h6 class="card-price text-center"></h6>${data.desc}</h6>

            <hr />
            <ul class="fa-ul">
                <li>
                    <span class="fa-li"><i class="fa fa-check"></i></span>Ticket left :
                    ${data.available_bal + data.available_ord}
                </li>
                <li>
                <span class="fa-li"><i class="fa fa-check"></i></span>Start time :
                ${data.start_time.split('T')[1].slice(0,-1)}  ${data.start_time.split('T')[0]} 
            </li>
            <li>
            <span class="fa-li"><i class="fa fa-check"></i></span>End time :
        ${data.end_time.split('T')[1].slice(0,-1)}  ${data.end_time.split('T')[0]} 
        </li>

            </ul>
            <hr />
            <div class="text-center">
                <button type="button" onclick="eventbuyclick(this)" class="btn" data-showid=${data.id} data-showname=${data.name} data-available_ord=${data.available_ord} data-available_bal=${data.available_bal} data-price_bal=${data.price_bal} data-price_ord=${data.price_ord} >
                    Know More ...
                </button>
            </div>
        </div>
    </div>
</div>




`
            row.innerHTML += html;
        })




    }).catch(err => {
        console.log(err.message)
        ; alert(err.message)
            ;
    })

}


function eventbuyclick(e) {

    $('#speakers').hide();
    $('#buy-tickets').show();
    $('#ordprice').html(e.getAttribute("data-price_ord") + " Rs");
    $('#balprice').html(e.getAttribute("data-price_bal") + " Rs");
    $('#ordleft').html("Available Ticket: " + e.getAttribute("data-available_ord"));
    $('#balleft').html("Available Ticket: " + e.getAttribute("data-available_bal"));
    $('#showname').html("Buy Ticket For " + e.getAttribute("data-showname"));
    document.getElementById('ordinarybutton').setAttribute("data-price_ord", e.getAttribute("data-price_ord"));
    document.getElementById('ordinarybutton').setAttribute("data-showid", e.getAttribute("data-showid"));
    document.getElementById('ordinarybutton').setAttribute("data-available_ord", e.getAttribute("data-available_ord"));
    document.getElementById('balconybutton').setAttribute("data-price_bal", e.getAttribute("data-price_bal"));
    document.getElementById('balconybutton').setAttribute("data-showid", e.getAttribute("data-showid"));
    document.getElementById('balconybutton').setAttribute("data-available_bal", e.getAttribute("data-available_bal"));


}
function back() {
    $('#speakers').show();
    $('#buy-tickets').hide();
    $('#ordprice').html('')
    $('#balprice').html('')
    $('#ordleft').html('')
    $('#balleft').html('')
    $('#showname').html('')
    document.getElementById('ordinarybutton').setAttribute("data-showid", '');
    document.getElementById('balconybutton').setAttribute("data-showid", '');


}


function ticketmodalopen(e) {
    if (localStorage.getItem('token') == null || localStorage.getItem('user') == null) {
        alert('please login first');
        window.open('login.html', '_self');
        return;

    }
    localStorage.setItem('showid', e.getAttribute("data-showid"));
    if (e.getAttribute('data-price_bal')) localStorage.setItem('showprice', e.getAttribute("data-price_bal"));
    else localStorage.setItem('showprice', e.getAttribute("data-price_ord"));
    localStorage.setItem('type', e.getAttribute("data-type"));
    if (e.getAttribute('data-available_bal')) localStorage.setItem('available', e.getAttribute("data-available_bal"));
    else localStorage.setItem('available', e.getAttribute("data-available_ord"));

}

function priceindicator(e) {
    if (parseFloat(localStorage.getItem('available')) < parseFloat(e.value)) {
        alert('not enought seats available');
    }
    let price = parseFloat(localStorage.getItem('showprice'));
    price = price * parseInt(e.value);
    $('#priceindicator').html(price + " Rs To be paid to Salesperson");
}
// import { jsPDF } from "jspdf";

document.getElementById('ticketbookform').addEventListener('submit', (e) => {
    e.preventDefault();
    let formdata = new FormData(document.getElementById('ticketbookform'));
    formdata.append('type', localStorage.getItem('type'));
    formdata.append('show', localStorage.getItem('showid'));
    formdata.append('token', localStorage.getItem('token'));
    console.log(formdata);
    let url = 'http://localhost:8000/ticket/';
    axios.post(url, formdata).then(res => {
        // console.log(res.data);
        const data = res.data.data;
        let seatarray = data.map(item => {
            return item.seat;

        })
        console.log(seatarray);
        const doc = new jsPDF({
            orientation: "landscape",
            unit: "in",
            format: [8, 5]
        });
        doc.setFontSize(20);
        doc.text('Booked Ticket', 3, 0.5);
        doc.text(`name: ${data[0].name}`, 1, 1)
        doc.text(`email: ${data[0].email}`, 1, 1.5);
        doc.text(`price: ${data[0].price* seatarray.length} Rs Paid to SalesPerson`, 1, 2);
        doc.text(`total seats: ${seatarray.length}`, 1, 2.5);
        doc.text(`seat numbers: ${seatarray.join(', ')}`, 1, 3);
        doc.text(`showname: ${data[0].show.name}`, 1, 3.5);
        doc.text(`showtime: ${data[0].show.start_time.split('T')[0]} ${ data[0].show.start_time.split('T')[1]}`, 1, 4);
        doc.text(`type: ${data[0].type}`, 1, 4.5);

        doc.save("ticket.pdf");


        alert('ticket booked successfully. Click OK to Download Ticket');
        window.open('index.html', '_self');
        document.getElementById('ticketbookform').reset();

    }).catch(err => {
        console.log(err)
        ; alert(err?.response?.data?.message)
            ;
            document.getElementById('ticketbookform').reset();

    })




});


show();