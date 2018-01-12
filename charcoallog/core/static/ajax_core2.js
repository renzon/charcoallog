$(function() {
  // Edit money
  $('.money-edit').on('click', function() {
    let obj = $(this).closest('tr').children('td')

    // get the length of array (obj)
    let totalLen = obj.length

    obj.each(function(i, e) {
      var item_v = $(this).text()
      if (i < totalLen - 1) {
        $(this).empty()
        // If is description the width is large
        if (i == 2) {
          console.log(i, item_v);
          $(this).append('<input type="text" style="width: 20em;" value="' + item_v + '" />')
        } else {
          $(this).append('<input type="text" style="width: 6em;" value="' + item_v + '" />')
        }
      }
    });
  });

  // Delete money
  $('.money-delete').on('click', function() {
    let url = $(this).data('url')
    let $this = $(this)
    $.get(url, function(data) {
      $this.parent().parent().remove()
    });
  });
});