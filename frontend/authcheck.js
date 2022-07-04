window.onload = () => {
    let token = localStorage.getItem('token');
    console.log(token);
    if (token) {
        console.log('token found');
        console.log(token);
        let url = 'http://localhost:8000/check_token/';
        let data = { token };
        axios.get(url, { headers: { "Authorization": `${token}` } }).then(res => {
            console.log(res.data, 'asfd0', location.href.split("/").slice(-1));
            if (location.href.split("/").slice(-1) == 'login.html')
                window.open('index.html', '_self');
            return;
        }).catch(err => {
            window.open('login.html', '_self');
            console.log(err);
        });

    }
    else {
        if (location.href.split("/").slice(-1) != 'login.html' && location.href.split("/").slice(-1) != 'index.html')
            window.open('login.html', '_self');

            
    }

}