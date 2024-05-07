//perform certain tasks based on users click and changes
$(function() {
    $('.selectpicker').on('loaded.bs.select', function() {
        setFields(); // I dunno why this is needed, but it is *shrugs*
    })

    $('#automata_load').hide()
    $('#integers_input').hide()
    $("#epsilon").hide()

    setFixedProperty();
    //this causes an error when loading the index file. don't worry about that
    //it is necessary when it comes to upload.html
    
    $('#automata_text').on('change keyup paste', handleChange);
    $('#transducer_text1').on('change keyup paste', handleChange)
    $('#transducer_text2').on('change keyup paste', handleChange)
});

function handleChange() {
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
}

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
        return /[01* +()a-zA-Z]/.test(str.split(/\n/)[0])
    } else if(count === 1) {
        if(!str.startsWith('@')) {
            var match = str.match(/^(.+)\n([\s\S]+)/)
            return /[01* +()]/.test(match[1]) && testFA(match[2]);
        } else if(CODES.indexOf(str.replace(/^(@\w+)[\s\S]+$/, "$1")) > -1) {
            return str.replace(/^.+\n([\s\S]+)/, "$1").split(/\n/).length == 1;
        } else if(str.startsWith('@Transducer')) {
            return testTrans(str);
        } else {
            return testFA(str);
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

function setFields() {
    var $select = $('#divsat_select')
    console.log("New function called")
    switch (document.form1.question.value) {
        case "0": //hide all input areas when no property selected
            hide('divsat'); //property selector for satisfaction, maximality, approx-maximality
            hide('automata_load'); //text box AND file upload space for automata input
            hide('integers_input'); //for Construction only: L, S, and N input boxes. 
            hide('epsilon');
            break;
        case "1":
            show('divsat');
            show('automata_load');
            hide('integers_input');
            hide('epsilon');
            $select.find('[value=4]').show();
            $select.find('[value=5]').show();
            $select.selectpicker('refresh');
            break;
        case "2":
            show('divsat');
            show('automata_load');
            hide('integers_input');
            hide('epsilon');
            $select.find('[value=4]').show();
            $select.find('[value=5]').hide();
            $select.selectpicker('refresh');
            break;
        case "3":
            show('divsat');
            hide('automata_load');
            hide('epsilon');
            $select.find('[value=4]').hide();
            $select.find('[value=5]').hide();
            $select.selectpicker('refresh');
            show('integers_input');
            break;
        case "4":
            console.log("I can finallydebug!!");
            show('divsat');
            show('automata_load');
            show('epsilon');
            hide('integers_input');
            $select.find('[value=4]').show();
            $select.find('[value=5]').show();
            $select.selectpicker('refresh');
            break;
    }
}

function setFixedProperty() {
    hide('div1');
    hide('div2');
    hide('div3');
    hide('div4');
    switch (document.getElementById('divsat_select').value) {
        case "1":
            show('div1');
            break;
        case "2":
            show('div3');
            break;
        case "3":
        case "4":
            show('div2');
            break;
        case "5":
            show('div2');
            show('div4');
        default:
            break;
    }
}

function hide(id) {
    document.getElementById(id).style.display = "none";
}

function show(id) {
    document.getElementById(id).style.display = "";
}
