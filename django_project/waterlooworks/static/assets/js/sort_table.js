$(document).ready(function(){
    $('#job_table').DataTable();

    var select = $("select");
    var input = $("input")
    select.addClass("form-control");
    select.addClass("form-select");
    input.addClass("form-control");
    input.addClass("form-input");
    input.attr("placeholder", "Filter");
    var select_container = $("#job_table_length")
    var input_container = $("#job_table_filter")
    select_container.append(select);
    select_container.append("<p id='select_description'>Entries Per Page</p>");
    input_container.append(input);
    input_container.after($("#job_table_paginate"));
    $("label").remove();
});