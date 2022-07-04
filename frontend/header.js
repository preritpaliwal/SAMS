document.getElementById("header").innerHTML =
    `
<div class="container">

<div id="logo" class="pull-left">
    <!-- Uncomment below if you prefer to use a text logo -->
    <!-- <h1><a href="#main">C<span>o</span>nf</a></h1>-->
    <a href="#intro" class="scrollto"><img src="img/FormalLogo.png" alt="" title=""></a>
</div>

<nav id="nav-menu-container">
    <ul class="nav-menu">
        <li class="menu-active"><a href="index.html">Home</a></li>
        <li><a href="index.html#speakers">Book/View Tickets</a></li>
        <li id="cancel" style="display:none;" ><a href="cancel.html">Cancel Tickets</a></li>
        <li id="info" style="display:none; " ><a href="information.html" id="infochange" >Information</a></li>
        <li id="balance" style="display:none; " ><a href="balance.html" >Balance</a></li>
        <li id="personname" style="display:none; color:white;"></li>
        <li id="personposition" style="display:none ; color:white;"></li>
        <li class="buy-tickets" id='logoutstate'><a href="login.html">login</a></li>
        <li class="buy-tickets" id="loginstate" style="display:none;" onclick="logout()"><a>logout</a></li>
    </ul>
</nav><!-- #nav-menu-container -->
</div>
`

const userData = JSON.parse(localStorage.getItem('user'));

if (userData && localStorage.getItem('token')) {
    if (userData.type == 'manager') {
        $('#balance').show();
        $('#infochange').html('Add Show/Salesperson');
    }
    if (userData.type == 'clerk') {
        $('#infochange').html('Add Expenditure');

    }
    $('#cancel').show();
    $('#info').show();
    $('#personname').show();
    $('#personposition').show();
    $('#nav-menu li:nth-child(1)').addClass('menu-active');
    $('#nav-menu li:nth-child(2)').addClass('menu-active');
    $('#nav-menu li:nth-child(3)').addClass('menu-active');
    $('#nav-menu li:nth-child(4)').addClass('menu-active');

    if (window.location.href.split('/').slice(-1) == 'information.html') {

        $('#personname').html(userData.first_name + " " + userData.last_name + "");
        $('#personposition').html(userData.type);
    }
    $('#logoutstate').hide();
    $('#loginstate').show();
}


let logout = async () => {
    console.log('click');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    $('#logoutstate').show();
    $('#loginstate').hide();
    window.location.reload();
    alert('logout successfully');


}
