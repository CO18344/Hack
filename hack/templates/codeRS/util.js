$(function() {
    $("#item").click(function() {
        $("#submenu").slideToggle(500);
    });
}); 

$(function() {
    $(".myItem").click(function() {
        $(".mySubmenu").slideToggle(500);
        
    });
}); 
$("form").on("submit", function (e) {
    $('#result').html('<div style="margin:auto; display:flex;"><span>Loading Testcases</span> &nbsp <div class="spinner-border" role="status"></div></div>');
    $('#rt').animate({
    scrollTop: $('#rt').get(0).scrollHeight
}, 1500);
    var dataString = $(this).serialize();
     
    $.ajax({
      type: "POST",
      url: '/dashboard/problems/code/?id={{problem.id}}',
      data: dataString,
      success: function (response) {
        // Display message back to the user here
        $('#result').html(response);
        $('#rt').animate({
    scrollTop: $('#rt').get(0).scrollHeight
}, 1500);
        
        $.ajax({
          type: "POST",
          url: '/dashboard/problems/code/update/?id={{problem.id}}&running=True',
          data:{
            csrfmiddlewaretoken: '{{ csrf_token }}'
            },
          success: function(response){
            console.log(response);
          }
        });
      }
    });
 
    e.preventDefault();
});