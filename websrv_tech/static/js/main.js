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

function showEventModal(id){
  retrieveEvent(id);
  // $('#modalEvent').modal('show');
}


// Recupera lista de eventos do server via ajax
function retrieveEvent(id){
  url = "/api/get-event-by-id/" + id;
  myEvent = {
    "event":{
      "id":id
    }
  }
  $.post({
      type: 'post',
      url: url,
      data: myEvent,
      contentType: "application/json; charset=utf-8",
      success: function (data) {
          console.log(data);
      }
  });

}

function deleteEvent(uuid){
  window.location = '/evento/' + uuid + '/excluir';

}
