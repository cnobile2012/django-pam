/*
 * django-pam
 *
 * by Carl J. Nobile
 *
 * Requires: jQuery, bootstrap, js.cookie, and inheritance
 */

"use strict";


Function.prototype.bind = function(object) {
  var method = this;

  var temp = function () {
    return method.apply(object, arguments);
  };

  return temp;
};


var _BaseModal = Class.extend({

  _csrfSafeMethod: function(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  _setHeader: function() {
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if (!this._csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }.bind(this)
    });
  },

  setDefault: function(obj, key, value) {
    if(key in obj) {
      return obj[key];
    } else {
      obj[key] = value;
      return obj[key];
    }
  },

  mimicDjangoErrors: function(data) {
    // Mimic Django error messages.
    var ul = '<ul class="errorlist"></ul>';
    var li = '<li></li>';
    var $li = null;
    var $errorUl = null;
    var $errorLi = null;

    for(var key in data) {
      $li = $('select[name=' + key +
        '], input[name=' + key + '], textarea[name=' + key + ']').parent();
      $errorUl = $(ul);

      for(var i = 0; i < data[key].length; i++) {
        $errorLi = $(li);
        $errorLi.html(data[key][i]);
        $errorLi.appendTo($errorUl);
      }

      $errorUl.appendTo($li);
    }
  }
});


var ModalAuthenticate = _BaseModal.extend({
  BASE_URL: '/',

  init: function() {
    var $login = $('#login');
    var $logout = $('#logout');

    if($login) {
      $('#modal-login').on('click', {$login: $login}, this._setupLogin);
      $('div.form-buttons button[name=ajax-submit]').on('click', {self: this},
        this._loginRequest);
    } else if($logout) {
      $('#modal-logout').on('click', {$login: $login}, this._logoutRequest);
      $('div.form-buttons button[name=ajax-submit]').on('click', {self: this},
        this._logoutRequest);
    }
  },

  _setupLogin: function(event) {
    event.data.$login.modal({backdrop: 'static'});
  },

  _loginRequest: function(event) {
    var self = event.data.self;

  },




  _logoutRequest: function() {
    var self = event.data.self;
    var $logout = event.data.$logout;

    $logout.modal({backdrop: 'static'});

  }



});


$(document).ready(function() {
  new ModalAuthenticate();
});
