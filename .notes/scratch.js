$("#tbAddress").find('tr').each(function (rowIndex, r) {
    let cols = [];
    cols.push($(this).attr("id")); 
    // $(this).find('td').each(function (colIndex, c) {
    //     cols.push($(this).attr("rel"));  
    // });
    data.push(cols);
});

function openDialog(id, err){
    if (err != ""){
        err = "<br />" + err;
    }

    var med = "[" + $("#" + id + "_drgdname").val() + " - " + $("#" + id + "_drgstrength").val() + "]";
    var iou_qty = $("#" + id + "_iouqty").val();
    var iou_comp = $("#" + id + "_ioucomp").val();
    var rem_qty = Number(iou_qty) - Number(iou_comp);
    var qty = "<br />Total IOU Quantity: " + iou_qty + " with " + iou_comp + " Filled</br /></br />";
    qty += "Quantity to Fill: <input style='text-align: right' size='6' type='text' value='" + rem_qty + "' id='fillVal' />";
    qty += " (A partial qty will keep the IOU open)";
    qty +="<br /><br />Close without completing <input  type='checkbox' id='cbIOU' name='cbIOU' value=''/>";
    qty +="<p style='color:red; font-weight:bold'>" + err + "</p>"
    //var fill_qty = $("#fillVal").val();

    confirmDialog("Close IOU", "Do you want to close the IOU for " + med + qty, id, $("#fillVal").val(), submit);
}