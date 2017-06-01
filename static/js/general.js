//perform certain tasks based on users click and changes
$(function() {
    $('#automata_load').hide()
    $('#integers_input').hide()
    $('#reset').click(function() {
        location.reload();
    });

    $('#automata_text').on('change keyup paste', function() {
        var this_ = $(this);

        if(this_.val() !== '') {
            if(validate(this_.val())) {
                this_.removeClass('border-failure').addClass('border-success');
            } else {
                this_.removeClass('border-success').addClass('border-failure');
            }
        } else {
            this_.removeClass('border-success border-failure');
        }
    });

    $('#transducer_text1').on('change keyup paste', function() {
        var this_ = $(this);

        if(this_.val() !== '') {
            if(validate(this_.val(), true)) {
                this_.removeClass('border-failure').addClass('border-success');
            } else {
                this_.removeClass('border-success').addClass('border-failure');
            }
        } else {
            this_.removeClass('border-success border-failure');
        }
    })

    $('#transducer_text2').on('change keyup paste', function() {
        var this_ = $(this);

        if(this_.val() !== '') {
            if(validate(this_.val(), true)) {
                this_.removeClass('border-failure').addClass('border-success');
            } else {
                this_.removeClass('border-success').addClass('border-failure');
            }
        } else {
            this_.removeClass('border-success border-failure');
        }
    })
});

//     elif count == 3: # Transducer with type
//         res = re.search(r'@(.+)\n(@[\s\S]+)\n(@[\s\S]+)$', aut_str)
//         result['transducer_type'] = res.group(1)
//         result['transducer'] = res.group(2)
//         result['aut_str'] = res.group(3)
//         return result

//     result['aut_str'] = aut_str
//     return result

function validate(str) {
    var CODES = ['@PREFIX', '@SUFFIX', '@INFIX', '@OUTFIX', '@HYPERCODE', '@CODE'],
        TRANSDUCERS = ['@InputAltering', '@ErrorDetecting', '@ErrorCorrecting'];

    str = str.replace(/\r/, "").replace(/#.+\n/, "").trim();

    if(str.startsWith('(START)')) {
        return /\(START\) \|- \d+\n(\d+ \w \d+\n)+\d+ -\| \(FINAL\)/.test(str);
    }

    var count = 0;
    str.split(/\n/).forEach(function(line) {
        if(line.startsWith('@')) ++count;
    })

    if(count === 0) {
        return /[01* +()]/.test(str.split(/\n/)[0]) && str.split(/\n/).length == 2
    } else if(count === 1) {
        if(!str.startsWith('@')) {
            var match = str.match(/^(.+)\n([\s\S]+)/)
            return /[01* +()]/.test(match[1]) && testFA(match[2]);
        } else if(CODES.indexOf(str.replace(/^(@\w+)[\s\S]+$/, "$1")) > -1) {
            return str.replace(/^.+\n([\s\S]+)/, "$1").split(/\n/).length == 1;
        } else if(str.startsWith('@Transducer')) {
            return testTrans(str);
        }
    } else if(count === 2) {
        var match = str.match(/(@[\s\S]+)(@[\s\S]+)/);
        var first = match[1].trim();
        var second = match[2].trim();

        if(CODES.indexOf(first) > -1) {
            return testFA(second);
        } else if(TRANSDUCERS.indexOf(first) > -1) {
            return testTrans(second)
        } else {
            return /(@Transducer.+(\n\d+ ([\w\d]|@epsilon) ([\w\d]|@epsilon) \d+)+)$/.test(first) && testFA(second);
        }
    } else if(count === 3) {
        var match = str.match(/^(@[\s\S]+)(@[\s\S]+)(@[\s\S]+)$/);
        var first = match[1].trim();
        var second = match[2].trim();
        var third = match[3].trim();

        return TRANSDUCERS.indexOf(first) > -1 &&
            /(@Transducer.+(\n\d+ ([\w\d]|@epsilon) ([\w\d]|@epsilon) \d+)+)$/.test(second) &&
            testFA(third)
    }

    return false;
}

function testFA(aut) {
    return /^@[DN]FA \d+(\n\d+ \w \d+)+\n?$/.test(aut);
}

function testTrans(tran) {
    return /(@Transducer.+\n(\d+ ([\w\d]|@epsilon) ([\w\d]|@epsilon) \d+\n)+)(.+)$/.test(tran);
}

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
    hide('div1');
    hide('div2');
    hide('div3');
    switch (document.getElementById('divsat_select').value) {
        case "1" :
            show('div1');
            break;
        case "2" :
            show('div3');
            break;
        case "3" :
        case "4" :
            show('div2');
            break;
        default: break;
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
};

function hide(id) {
    document.getElementById(id).style.display="none";
}

function show(id) {
    document.getElementById(id).style.display="";
}
