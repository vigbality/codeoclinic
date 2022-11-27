$("form").on("change", ".image", function(){ 
  $(this).parent(".image").attr("data-text",         $(this).val().replace(/.*(\/|\\)/, '') );
  document.getElementById("imageForm").submit();
});