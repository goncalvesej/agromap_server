function goToEvents(id) {
  window.location = '/inspecao/' + id +'/eventos';
}

function formatDate(elem, option){
  var date = elem.value;
  var new_date = date[3];
  new_date += date[4];
  new_date += "/";
  new_date += date[0];
  new_date += date[1];
  new_date += "/";
  for(i=6; i<10; i++){
    new_date += date[i];
  }
  elem.value = new_date;
  var formatedDate = new_date[6] + new_date[7] + new_date[8] + new_date[9] + '-';
  formatedDate = formatedDate + new_date[3]+ new_date[4] + '-';
  formatedDate = formatedDate + new_date[0]+ new_date[1];
  document.getElementById(option).value = formatedDate + 'T00:00:00-03';
}
