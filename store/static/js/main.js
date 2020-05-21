$(function(){


    $("option[value='']").attr("disabled", "");

    $("#name").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_name').parent().removeClass("other");
            $('#other_name').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_name').parent().addClass("other");
            $('#other_name').removeAttr('required');
        }
    });
    $("#company").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_company').parent().removeClass("other");
            $('#other_company').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_company').parent().addClass("other");
            $('#other_company').removeAttr('required');
        }
    });
    $("#country").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_country').parent().removeClass("other");
            $('#other_country').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_country').parent().addClass("other");
            $('#other_country').removeAttr('required');
        }
    });
    $("#distributer").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_distributer').parent().removeClass("other");
            $('#other_distributer').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_distributer').parent().addClass("other");
            $('#other_distributer').removeAttr('required');
        }
    });
    $("#family").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_family').parent().removeClass("other");
            $('#other_family').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_family').parent().addClass("other");
            $('#other_family').removeAttr('required');
        }
    });
    $("#place").change(function(){
        if ($(this).val() == "other")
        {
            $(this).parent().addClass("col-3");
            $(this).parent().removeClass("col-6");
            $('#other_place').parent().removeClass("other");
            $('#other_place').attr('required', '');
        }
        else {
            $(this).parent().addClass("col-6");
            $(this).parent().removeClass("col-3");
            $('#other_place').parent().addClass("other");
            $('#other_place').removeAttr('required');
        }
    });


    $("#quantity").change(function(){
        var total = Number($(this).val()) * Number($('#get_price').text());
        $('#paid_price').val(total);
    });


});