function update() {
    ckb = $("#checkbox1").is(':checked');
    $.getJSON('/update_prof_availability/', {
        prof_email: email,
        state: ckb
    }, function(data) {
        console.log('successful update');
    });
}
