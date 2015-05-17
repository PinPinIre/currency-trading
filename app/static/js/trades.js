function ConvertFormToJSON(form){
    // SOURCE: http://www.developerdrive.com/2013/04/turning-a-form-element-into-json-and-submiting-it-via-jquery/
    var array = jQuery(form).serializeArray();
    var json = {};

    jQuery.each(array, function() {
        json[this.name] = this.value || '';
    });

    return json;
}

$(document).ready( function() {
    var form = $('#trade_form');
    form.find(':button').click( function() {
        // Update the Value of each input field
        $("input").each(function() {
                $(this).attr('value', $(this).val());
        });
        $('#requestModal').modal('show')
        // Send ajax request and convert form to json
        $.ajax( {
          type: "POST",
          url: "/trade",
          contentType: "application/json;charset=UTF-8",
          data: JSON.stringify(ConvertFormToJSON(form)),
          success: function( response ) {
            console.log( response )
            $('#requestModal').modal('show')
            $("#requestMessage").text("Transaction successful")
          },
          error: function( response ) {
              console.log( response );
              $('#requestModal').modal('show')
              $("#requestMessage").text("Request failed: Response " + response.status)
          }
        } );
    } );

} );
