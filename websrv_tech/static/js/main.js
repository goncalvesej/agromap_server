var user_id = '';

function goToEvents(id) {
  window.location = '/inspecao/' + id +'/eventos';
}

function formatDate(e, elem, field){
  // var digits = input_text.replace(/[/_]/g,'');
  if(e.keyCode == 8)
    return true;

  var new_digits = removeInvalidChars(elem.value);

  var date_formated = new_digits.substr(0,2) + '/' + new_digits.substr(2,2) + '/' + new_digits.substr(4,4);
  elem.value = date_formated;

  var elem_new_value = new_digits.substr(4,4) + '-' + new_digits.substr(2,2) + '-' + new_digits.substr(0,2);

  if(field == 'start_at'){
    elem_new_value += 'T00:00:00-00';
  }else{
    elem_new_value += 'T23:59:59-00';
  }
  document.getElementById(field).value = elem_new_value;
}

function removeInvalidChars(text){
  var new_text ='';
  for (var i = 0; i < text.length; i++) {
    if(text.charCodeAt(i) <= 57 && text.charCodeAt(i) >= 48){
      new_text += text[i];
    }
  }
  return new_text;
}


function showEventModal(id){
  retrieveEvent(id);
  $('#modalEvent').modal('show');
}

function submitForm(){
  var start_date = removeInvalidChars(document.getElementById('input_start').value);
  var end_date = removeInvalidChars(document.getElementById('input_end').value);
  var btn = document.getElementById('btn-submit');
  btn.setAttribute('disabled','disabled');
  btn.innerHTML = 'Aguarde...';

  var name = document.getElementById('name').value;
  if(name.length < 3 ){
    showAlert('Nome precisa ter mais que 3 caracteres!');
    btn.removeAttribute('disabled');
    btn.innerHTML = 'Salvar';
    return false;
  }

  if(!isValidDate(start_date)){
    showAlert('Data de início não é válida!');
    btn.removeAttribute('disabled');
    btn.innerHTML = 'Salvar';
    return false;
  }
  if(!isValidDate(end_date)){
    showAlert('Data de término não é válida!');
    btn.removeAttribute('disabled');
    btn.innerHTML = 'Salvar';
    return false;
  }
  if(!compareDates(getCurrentDay(), start_date)){
      showAlert('Data de início não pode ser anterior a hoje!');
      btn.removeAttribute('disabled');
      btn.innerHTML = 'Salvar';
      return false;
  }
  if(!compareDates(start_date, end_date)){
    showAlert('Data de início não pode ser posterior a data de término');
    btn.removeAttribute('disabled');
    btn.innerHTML = 'Salvar';
    return false;
  }
  document.getElementById('form-inspection').submit(); //Envia formulario
}

function getCurrentDay(){
  var date = new Date();
  var day = date.getDate();
  if(day <10)
    day = '0' + day;
  var month = date.getMonth()+1;
  var year = date.getFullYear();
  // var current = year + '' + month + day ;
  var current = day + '' + month + '' + year ;
  console.log("current: " + current);
  return current;
}

function showAlert(text){
  var div_msg = document.getElementById('div_msg');
  if(div_msg == null){ //Cria elemento

    var span = document.createElement('span');
    span.setAttribute('aria-hidden', 'true');
    span.innerHTML = '&times;';

    var button = document.createElement('button');
    button.setAttribute('type', 'button');
    button.setAttribute('class', 'close');
    button.setAttribute('data-dismiss', 'alert');
    button.setAttribute('aria-label', 'Close');
    button.appendChild(span);

    var span_content = document.createElement('span');
    span_content.setAttribute('aria-hidden', 'true');
    // text += 'A data de início não pode ser posterior a data de término.<br>';
    span_content.innerHTML = text;
    span_content.setAttribute('id', 'msg_content');

    var div_alert = document.createElement('div');
    div_alert.setAttribute('class', 'alert alert-warning');
    div_alert.setAttribute('id', 'div_msg');
    div_alert.setAttribute('role', 'alert');
    div_alert.appendChild(button);
    div_alert.appendChild(span_content);

    var div_col = document.createElement('div');
    div_col.setAttribute('class', 'col-md-8 col-align-self-center text-center');
    div_col.appendChild(div_alert);

    var div_row = document.createElement('div');
    div_row.setAttribute('class', 'row justify-content-center distance');
    div_row.appendChild(div_col);

    var container = document.getElementsByClassName('container-fluid')[0];
    container.insertBefore(div_row, container.firstChild);

  }else{ // Elemento já existe
    div_msg.setAttribute('class', 'alert alert-warning');
    var msg_content = document.getElementById('msg_content');
    msg_content.innerHTML = text;
    $(".alert").alert()
  }
}

function compareDates(start, end){
  console.log("start" + start);
  console.log("end" + end);
  var fStart = start.substr(4,4) + start.substr(2,2) + start.substr(0,2);
  var fEnd = end.substr(4,4) + end.substr(2,2) + end.substr(0,2);
  if(fStart<=fEnd){
    return true;
  }else{
    return false;
  }
}

function validStartDate(start, end){
  var fStart = start.substr(4,4) + start.substr(2,2) + start.substr(0,2);
  var fEnd = end.substr(4,4) + end.substr(2,2) + end.substr(0,2);
  if(fStart<=fEnd){
    return true;
  }else{
    return false;
  }
}

function isValidDate(date){
  var day = date.substr(0,2);
  var month = date.substr(2,2);
  var year = date.substr(4,4);
  if(day > 0 && day <= 31 && month > 0 && month <= 12 && year > 2016){
    return true;
  }else{
    return false;
  }

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

function disableMe(elem) {
  elem.setAttribute('disabled', 'disabled');
  elem.innerHTML = 'Aguarde...';
}

function changeUserLevel(userID, userName, userLevel){
  user_id = userID;
  var level ='';
  var text = '';
  if(userLevel == 0){
    level = 'Administrador';
    text = 'Se você fizer essa alteração ele <string>NÃO</string> poderá:';
    text +='<br><ul><li>Gerenciar usuários</li><li>Gerenciar inspeções</li></ul><br>';
    text +='Se este for o único usuário Administrador a operação não será realizada.';
  }else{
    level = 'Padrão';
    text = 'Se você fizer essa alteração ele <string>PODERÁ</string>:<br>';
    text += '<ul><li>Gerenciar usuários</li><li>Gerenciar inspeções</li></ul>';
  }
  var span = document.getElementById('span_user_level');
  span.innerHTML = level;
  var content = document.getElementById('content_user_level');
  content.innerHTML = text;

  $('#modalUserLevel').modal('show');
}

function performChangeUserLevel(){
  window.location = '/usuario/' + user_id +'/altera-nivel';
}
