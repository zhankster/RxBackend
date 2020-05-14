function checkVal(num, numCompare) {
    if (parseFloat(num)) {

        if (parseFloat(num) < 1) {
            return "Quantity must be greater than zero";
        }
        if (parseFloat(num) > parseFloat(numCompare)) {
            return "Quantity entered is greater than the fill quanity";
        }

        return "Valid";
    }
    return "Not a valid numeric value";
}

function confirmDialog(head, msg, id, qty, cb){
    bootbox.confirm({
            title: head,
            message: msg, 
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-primary'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-default'
                }
            },
            callback: function(result) { 
                console.log('This was logged in the callback: ' + result);
                cb(id, qty, result);
            }
        });
}

function msgTemplate(head, msg, foot){
    bootbox.alert({
        title : head,
        message: msg + foot
    });
}

function checkIntVal(num, numCompare) {
    if (Number.isInteger(parseInt(num, 10))) {
        if (!Number.isInteger(Number(num))){
            return "Value must an be integer (non-decimal)";
        }

        if (parseInt(num, 10) < 1) {
            return "Quantity must be greater than zero";
        }

        if (parseInt(num, 10) > parseInt(numCompare, 10)) {
            return "Quantity entered is greater than the fill quanity";
        }
        return "Valid";
    }
    return "Not a valid numeric value";
}

function removeTextAreaWhiteSpace(el) {
    var lines = $("textarea[name="+ el +"]").val().split(/\n/);      
    var texts = [];    
    for (var i=0; i < lines.length; i++) {    
      if (/\S/.test(lines[i])) {    
        texts.push($.trim(lines[i]));    
      }    
    }    
    var n = texts.toString().split(",").join("\n");    
    $("textarea[name="+ el +"]") .val(n);
  }



  function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }

