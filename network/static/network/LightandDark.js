document.addEventListener('DOMContentLoaded', function(){
    // Add event listeners to radio buttons
    let lightRadio = document.querySelector('.switch-right');
    let darkRadio = document.querySelector('.switch-left');

    lightRadio.addEventListener('click', function() {
        setTheme('light');
    });

    darkRadio.addEventListener('click', function() {
        setTheme('dark');
    });

    // Function to set the theme
    function setTheme(theme) {
        let cards = document.querySelectorAll('.card');
        cards.forEach(function(card){
            if (theme === 'light') {
                card.style.backgroundColor = '#fff';
            } else if (theme === 'dark') {
                card.style.backgroundColor = '#ebd5d5';
            }
        })

        // Add logic to change the theme
        if (theme === 'light') {
            // Apply light theme styles
            document.querySelector('body').style.backgroundColor = '#fff';
            document.querySelector('.navbar').style.backgroundColor = '#f8f9fa';
            document.querySelectorAll('.navbar .nav-item .nav-link').forEach((navLink) => {
                navLink.style.color = 'rgba(0,0,0,.5)';
            });
        } else if (theme === 'dark') {
            // Apply dark theme styles
            document.querySelector('body').style.backgroundColor = '#f95959';
            document.querySelector('.navbar').style.backgroundColor = '#ea8a8a';
            document.querySelectorAll('.navbar .nav-item .nav-link').forEach((navLink) => {
                navLink.style.color = '#f2f2f2';
            });
        }
    }
});


