$(document).ready(function(){
    preview_panel = $(document.createElement("div"));
    $(".wmd-preview-title").after(preview_panel);
    $(".wmd-preview-title").remove();
    preview_panel.append('<div id="preview-title-self">HTML Preview (May Hold a Slight Difference)</div>');
    preview_panel.append($("#id_content_wmd_preview"));
    $("#id_content_wmd_preview").addClass("markdown-body");

    $("#id_content_wmd_button_bar").append('<input type="checkbox" class="update-latex" id="update-latex-button" checked><div class="update-latex">Update Latex</div></input>');

    $("textarea").keydown(function(e) {
        if(e.keyCode === 9) { // tab was pressed
            // get caret position/selection
            var start = this.selectionStart;
            var end = this.selectionEnd;

            var $this = $(this);
            var value = $this.val();

            // set textarea value to: text before caret + tab + text after caret
            $this.val(value.substring(0, start)
                        + "\t"
                        + value.substring(end));

            // put caret at right position again (add one for the tab)
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            e.preventDefault();
        }
    });
});