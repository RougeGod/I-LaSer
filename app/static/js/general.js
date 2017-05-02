//perform certain tasks based on users click and changes
$(function() {
    $('#automata_load').hide()
    $('#integers_input').hide()
    $('#reset').click(function() {
        location.reload();
    });
});

function setRadio() {
    var radios = document.getElementsByName('choice');
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            if (radios[i].value == 1) {
                document.getElementById('EDChoice').disabled = false;
                document.getElementById('LevenshteinChoice').disabled = false;
            } else {
                document.getElementById('EDChoice').disabled = true;
                document.getElementById('LevenshteinChoice').disabled = true;
            }
        }
    }
}


function setMaximality() {
    switch (document.form1.que.value) {
        case "":
            hide('divsat');
            hide('automata_load')
            hide('integers_input')
        break;
        case "1":
        case "2":
            show('divsat');
            show('automata_load');
            hide('integers_input');
            $('#divsat_select').find('[value=4]').show();
            $('#divsat_select').selectpicker('refresh');
        break;
        case "3":
            show('divsat');
            hide('automata_load')
            $('#divsat_select').find('[value=4]').hide();
            $('#divsat_select').selectpicker('refresh');
            show('integers_input')
        break;
    }
}

function setFixedProperty() {
    switch (document.form1.prv.value) {
        case "" :
            hide('div1');
            hide('div2');
            hide('div3');
        break;
        case "1" :
            show('div1');
            hide('div2');
            hide('div3');
        break;
        case "2" :
            hide('div1');
            hide('div2');
            show('div3');
        break;
        case "3" :
            hide('div1');
            show('div2');
            hide('div3');
        break;
        case "4" :
            hide('div1');
            show('div2');
            hide('div3');
        break;
    }
}

function setFixedProperty1() {
    switch (document.form1.prv1.value) {
        case "" :
            hide('div1');
            hide('div2');
            hide('div3');
        break;
        case "1" :
            show('div1');
            hide('div2');
            hide('div3');
        break;
        case "2" :
            hide('div1');
            hide('div2');
            show('div3');
        break;
        case "3" :
            hide('div1');
            show('div2');
            hide('div3');
        break;
        case "4" :
            hide('div1');
            show('div2');
            hide('div3');
        break;
    }
}

window.onload = function() {
    for(var i = 0; i < document.form1.prv.options.length; i++)
    {
        if (document.form1.prv.options[i].value=="")
            document.form1.prv.selectedIndex = i;
    }
    for(var i = 0; i < document.form1.que.options.length; i++)
    {
        if (document.form1.que.options[i].value=="")
            document.form1.que.selectedIndex = i;
    }
    setFixedProperty();
}

function hide(id) {
    document.getElementById(id).style.display="none";
}

function show(id) {
    document.getElementById(id).style.display="";
}


